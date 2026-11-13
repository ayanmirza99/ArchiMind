from knowledge_base import RULES, RULES_BY_ID, MULTI_VALUE_SLOTS


def evaluate_condition(condition, facts):
    """Check one (fact, operator, value) condition; an unknown fact makes it False."""
    fact_name, operator, expected = condition
    actual = facts.get(fact_name)

    if actual is None:
        return False

    if operator == "==":
        return actual == expected
    if operator == "!=":
        return actual != expected
    if operator == "<":
        return actual < expected
    if operator == "<=":
        return actual <= expected
    if operator == ">":
        return actual > expected
    if operator == ">=":
        return actual >= expected
    if operator == "in":
        return actual in expected
    if operator == "contains":
        return expected in actual
    if operator == "not contains":
        return expected not in actual

    raise ValueError(f"Unknown operator '{operator}' in condition {condition}")


def rule_matches(rule, facts):
    return all(evaluate_condition(condition, facts) for condition in rule["if"])


def order_conflict_set(conflict_set):
    """Conflict resolution: highest priority first, then most conditions, then knowledge-base order."""
    return sorted(conflict_set, key=lambda rule: (-rule["priority"], -len(rule["if"])))


def fire_rule(rule, facts, support, owners, conflicts, trace_entry):
    """ACT: add the rule's conclusion to working memory and record the outcome in trace_entry."""
    slot, value = rule["then"]
    support.setdefault(slot, {})

    # Case 1: list slot -> keep every applicable value (no conflicts possible)
    if slot in MULTI_VALUE_SLOTS:
        facts.setdefault(slot, [])
        if value in facts[slot]:
            trace_entry["status"] = "supported"
            trace_entry["note"] = "Already concluded by another rule; this rule adds supporting evidence."
        else:
            facts[slot].append(value)
            trace_entry["status"] = "asserted"
            trace_entry["note"] = f"Added to {slot}."
        support[slot].setdefault(value, []).append(rule["id"])
        return

    current_value = facts.get(slot)

    # Case 2: empty single-value slot -> assert the fact
    if current_value is None:
        facts[slot] = value
        owners[slot] = trace_entry
        support[slot].setdefault(value, []).append(rule["id"])
        trace_entry["status"] = "asserted"
        trace_entry["note"] = f"{slot} = {value}"
        return

    # Case 3: same value already concluded -> extra supporting evidence
    if current_value == value:
        support[slot][value].append(rule["id"])
        trace_entry["status"] = "supported"
        trace_entry["note"] = "Agrees with the conclusion already in working memory."
        return

    # Case 4: conflict -> the higher-priority rule's conclusion wins
    previous_entry = owners[slot]
    previous_rule = previous_entry["rule"]

    if rule["priority"] > previous_rule["priority"]:
        facts[slot] = value
        owners[slot] = trace_entry
        del support[slot][current_value]
        support[slot].setdefault(value, []).append(rule["id"])
        previous_entry["status"] = "overridden"
        previous_entry["note"] = f"Replaced by {rule['id']} (higher priority {rule['priority']})."
        trace_entry["status"] = "asserted"
        trace_entry["note"] = f"{slot} = {value} (overrides {previous_rule['id']})"
        kept_rule, kept_value, dropped_rule, dropped_value = rule, value, previous_rule, current_value
    else:
        trace_entry["status"] = "rejected"
        trace_entry["note"] = (f"{slot} already = {current_value} from {previous_rule['id']} "
                               f"(priority {previous_rule['priority']} >= {rule['priority']}).")
        kept_rule, kept_value, dropped_rule, dropped_value = previous_rule, current_value, rule, value

    conflicts.append({
        "slot": slot,
        "kept_value": kept_value, "kept_rule": kept_rule["id"], "kept_priority": kept_rule["priority"],
        "dropped_value": dropped_value, "dropped_rule": dropped_rule["id"],
        "dropped_priority": dropped_rule["priority"],
    })


def run_inference(user_facts):
    """Forward chaining: repeat MATCH -> RESOLVE -> ACT until no rule can fire."""
    # Working memory starts as a copy of the user's facts
    facts = {name: (list(value) if isinstance(value, list) else value)
             for name, value in user_facts.items()}

    fired_rule_ids = set()   # refraction: each rule fires at most once
    trace = []
    support = {}
    owners = {}              # single-value slot -> trace entry of the rule that set it
    conflicts = []
    cycle = 0

    while True:
        # 1. MATCH: rules whose conditions are all true form the conflict set
        conflict_set = [rule for rule in RULES
                        if rule["id"] not in fired_rule_ids and rule_matches(rule, facts)]

        if not conflict_set:
            break   # nothing else can be concluded -> reasoning is complete

        # 2. RESOLVE: choose one rule
        agenda = order_conflict_set(conflict_set)
        rule = agenda[0]

        # 3. ACT: fire it
        cycle += 1
        fired_rule_ids.add(rule["id"])
        trace_entry = {
            "cycle": cycle,
            "rule": rule,
            "conflict_set": [r["id"] for r in agenda],
            # snapshot of the facts that made each condition true
            "matched": [(condition, _snapshot(facts.get(condition[0]))) for condition in rule["if"]],
            "status": "",
            "note": "",
        }
        fire_rule(rule, facts, support, owners, conflicts, trace_entry)
        trace.append(trace_entry)

    return {
        "initial_facts": dict(user_facts),
        "facts": facts,
        "trace": trace,
        "support": support,
        "conflicts": conflicts,
    }


def _snapshot(value):
    return list(value) if isinstance(value, list) else value


def format_value(value):
    if isinstance(value, bool):
        return "True" if value else "False"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, list):
        return ", ".join(value) if value else "(none)"
    return str(value)


def describe_condition(condition):
    fact_name, operator, expected = condition
    if operator == "in":
        return f"{fact_name} is one of [{', '.join(str(v) for v in expected)}]"
    if operator == "contains":
        return f"{fact_name} includes '{expected}'"
    if operator == "not contains":
        return f"{fact_name} does not include '{expected}'"
    if operator == "==":
        return f"{fact_name} = {format_value(expected)}"
    if operator == "!=":
        return f"{fact_name} ≠ {format_value(expected)}"
    symbols = {"<": "<", "<=": "≤", ">": ">", ">=": "≥"}
    return f"{fact_name} {symbols[operator]} {format_value(expected)}"


def describe_rule(rule):
    conditions = " AND ".join(describe_condition(c) for c in rule["if"])
    slot, value = rule["then"]
    return f"IF {conditions} THEN {slot} = {format_value(value)}"


def get_conclusions(result, slot):
    """Return [(value, [rule ids]), ...] for one recommendation slot."""
    value = result["facts"].get(slot)
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    return [(v, result["support"][slot][v]) for v in values]


def explain_how(result, fact_name, value, depth=0):
    """HOW-explanation: trace a conclusion back to the user's answers as (depth, text) lines."""
    rule_ids = result["support"].get(fact_name, {}).get(value, [])
    if not rule_ids or depth > 10:
        return []
    rule = RULES_BY_ID[rule_ids[0]]   # the rule that first concluded it

    lines = []
    for condition in rule["if"]:
        c_fact, operator, expected = condition
        if c_fact in result["initial_facts"]:
            actual = format_value(result["facts"][c_fact])
            lines.append((depth, f"{describe_condition(condition)}  —  user input: {actual}"))
        else:
            # Derived fact: explain recursively how it was concluded
            c_value = expected if operator == "contains" else result["facts"].get(c_fact)
            c_rules = result["support"].get(c_fact, {}).get(c_value, ["?"])
            lines.append((depth, f"{describe_condition(condition)}  —  concluded by rule {c_rules[0]}"))
            lines += explain_how(result, c_fact, c_value, depth + 1)
    return lines


# Command-line demo: python inference_engine.py
if __name__ == "__main__":
    demo_facts = {
        "app_type": "E-commerce", "expected_users": 500000, "concurrent_users": 25000,
        "complexity": "High", "budget": "High", "team_size": 20, "team_experience": "Expert",
        "realtime": "One-way updates", "media_storage": "Heavy", "data_structure": "Relational",
        "data_volume": "Large", "workload": "Read-heavy", "security": "High", "scalability": "High",
        "availability": "Mission-critical", "geo_distribution": "Multi-region",
        "api_requirements": ["Public API for third parties", "Mobile app clients"],
        "background_processing": "Heavy", "integrations": ["Payment gateway", "Email / SMS"],
        "deployment": "Cloud", "growth": "Rapid", "seo_important": True,
    }
    result = run_inference(demo_facts)

    print(f"Knowledge base: {len(RULES)} rules")
    print(f"Rules fired:    {len(result['trace'])} (cycles of forward chaining)\n")
    for entry in result["trace"]:
        rule = entry["rule"]
        print(f"Cycle {entry['cycle']:>3} | {rule['id']:<9} | {entry['status']:<10} | {entry['note']}")

    print("\nHOW was the architecture concluded?")
    architecture = result["facts"]["architecture"]
    print(f"architecture = {architecture}")
    for depth, text in explain_how(result, "architecture", architecture):
        print("    " * (depth + 1) + text)
