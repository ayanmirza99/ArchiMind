import streamlit as st

from knowledge_base import (
    RULES, RULES_BY_ID, INPUT_OPTIONS, INPUT_FACT_NAMES, SINGLE_VALUE_SLOTS,
    MULTI_VALUE_SLOTS, DERIVED_FACTS, ARCHITECTURE_PROFILES,
)
from inference_engine import (
    run_inference, get_conclusions, explain_how, describe_condition,
    describe_rule, format_value,
)

st.set_page_config(page_title="ArchiMind", layout="wide")


DASHBOARD = "Dashboard"
ASSESSMENT = "Project Assessment"
RECOMMENDATIONS = "Expert Recommendations"
REASONING = "Expert Reasoning"
SUMMARY = "Assessment Summary"
PAGES = [DASHBOARD, ASSESSMENT, RECOMMENDATIONS, REASONING, SUMMARY]

SLOT_LABELS = {
    "architecture": "Architecture",
    "backend": "Backend",
    "frontend": "Web frontend",
    "mobile": "Mobile app",
    "primary_database": "Primary database",
    "data_services": "Additional data services",
    "api_style": "API style",
    "realtime_protocol": "Real-time communication",
    "communication": "Integrations & service communication",
    "message_broker": "Message queue / broker",
    "caching": "Caching",
    "hosting": "Hosting platform",
    "infrastructure": "Cloud infrastructure",
    "storage": "File & media storage",
    "deployment_strategy": "Deployment strategy",
    "devops": "DevOps & operations",
    "security_measures": "Security",
    "scalability_measures": "Scalability",
    "performance": "Performance",
    "risks": "Risks",
}

# Longer drop-down labels; the stored fact keeps the short value
OPTION_HINTS = {
    "realtime": {"One-way updates": "One-way updates (live feeds, notifications, dashboards)",
                 "Bidirectional": "Bidirectional (chat, collaboration, multiplayer)"},
    "media_storage": {"Moderate": "Moderate (images, documents)",
                      "Heavy": "Heavy (video, large files)"},
    "background_processing": {"Light": "Light (emails, scheduled tasks)",
                              "Heavy": "Heavy (data pipelines, video or report processing)"},
    "security": {"Standard": "Standard (typical web app)",
                 "High": "High (sensitive personal data)",
                 "Critical": "Critical (regulated: HIPAA, PCI-DSS, GDPR...)"},
    "availability": {"Standard": "Standard (~99%, short outages acceptable)",
                     "High": "High (99.9%)",
                     "Mission-critical": "Mission-critical (99.99% or more)"},
    "data_volume": {"Small": "Small (< 10 GB)", "Medium": "Medium (10 GB - 1 TB)", "Large": "Large (> 1 TB)"},
    "data_structure": {"Relational": "Relational (tables with relationships)",
                       "Document-based": "Document-based (flexible JSON documents)",
                       "Mixed": "Mixed (both)"},
    "workload": {"Read-heavy": "Read-heavy (mostly browsing / reading)",
                 "Write-heavy": "Write-heavy (constant inserts, events, telemetry)"},
    "geo_distribution": {"Single region": "Single region (one country)",
                         "Multi-region": "Multi-region (several countries)",
                         "Global": "Global (worldwide users)"},
}

DEFAULT_FACTS = {
    "app_type": "SaaS", "expected_users": 20000, "concurrent_users": 500,
    "complexity": "Medium", "budget": "Medium", "team_size": 5, "team_experience": "Intermediate",
    "realtime": "None", "media_storage": "Moderate", "data_structure": "Relational",
    "data_volume": "Medium", "workload": "Balanced", "security": "Standard", "scalability": "Medium",
    "availability": "High", "geo_distribution": "Single region", "api_requirements": [],
    "background_processing": "Light", "integrations": ["Email / SMS"], "deployment": "Cloud",
    "growth": "Moderate", "seo_important": False,
}

SAMPLE_PROJECTS = {
    "Student blog (small and simple)": {
        "description": "A personal blog with articles and comments, built by two students.",
        "facts": {
            "app_type": "Content / Blog", "expected_users": 2000, "concurrent_users": 50,
            "complexity": "Low", "budget": "Low", "team_size": 2, "team_experience": "Beginner",
            "realtime": "None", "media_storage": "Moderate", "data_structure": "Relational",
            "data_volume": "Small", "workload": "Read-heavy", "security": "Standard", "scalability": "Low",
            "availability": "Standard", "geo_distribution": "Single region", "api_requirements": [],
            "background_processing": "None", "integrations": [], "deployment": "No preference",
            "growth": "Stable", "seo_important": True,
        },
    },
    "Startup MVP on a tight budget": {
        "description": "A note-taking SaaS MVP with social login and a flexible data model.",
        "facts": {
            "app_type": "SaaS", "expected_users": 1000, "concurrent_users": 100,
            "complexity": "Low", "budget": "Low", "team_size": 3, "team_experience": "Intermediate",
            "realtime": "None", "media_storage": "None", "data_structure": "Document-based",
            "data_volume": "Small", "workload": "Balanced", "security": "Standard", "scalability": "Medium",
            "availability": "Standard", "geo_distribution": "Single region",
            "api_requirements": ["Flexible client queries"], "background_processing": "Light",
            "integrations": ["Social login", "Email / SMS"], "deployment": "Cloud",
            "growth": "Rapid", "seo_important": False,
        },
    },
    "Hospital patient portal": {
        "description": "Patients book appointments, chat with doctors and download reports. Hosted in the hospital's own data centre.",
        "facts": {
            "app_type": "Healthcare", "expected_users": 50000, "concurrent_users": 2000,
            "complexity": "Medium", "budget": "Medium", "team_size": 8, "team_experience": "Intermediate",
            "realtime": "Bidirectional", "media_storage": "Moderate", "data_structure": "Relational",
            "data_volume": "Medium", "workload": "Balanced", "security": "Critical", "scalability": "Medium",
            "availability": "High", "geo_distribution": "Single region",
            "api_requirements": ["Mobile app clients"], "background_processing": "Light",
            "integrations": ["Email / SMS"], "deployment": "On-premises",
            "growth": "Moderate", "seo_important": False,
        },
    },
    "Global e-commerce marketplace": {
        "description": "A worldwide marketplace with mobile apps, public partner API and millions of shoppers.",
        "facts": {
            "app_type": "E-commerce", "expected_users": 2000000, "concurrent_users": 50000,
            "complexity": "High", "budget": "High", "team_size": 40, "team_experience": "Expert",
            "realtime": "One-way updates", "media_storage": "Heavy", "data_structure": "Relational",
            "data_volume": "Large", "workload": "Read-heavy", "security": "High", "scalability": "High",
            "availability": "Mission-critical", "geo_distribution": "Global",
            "api_requirements": ["Public API for third parties", "Mobile app clients",
                                 "Internal service-to-service"],
            "background_processing": "Heavy",
            "integrations": ["Payment gateway", "Email / SMS", "Social login", "Analytics"],
            "deployment": "Cloud", "growth": "Rapid", "seo_important": True,
        },
    },
    "IoT fleet tracking platform": {
        "description": "Tens of thousands of delivery vehicles stream GPS and sensor data every few seconds.",
        "facts": {
            "app_type": "IoT", "expected_users": 60000, "concurrent_users": 20000,
            "complexity": "High", "budget": "Medium", "team_size": 10, "team_experience": "Expert",
            "realtime": "One-way updates", "media_storage": "None", "data_structure": "Mixed",
            "data_volume": "Large", "workload": "Write-heavy", "security": "High", "scalability": "High",
            "availability": "High", "geo_distribution": "Multi-region",
            "api_requirements": ["Internal service-to-service"], "background_processing": "Heavy",
            "integrations": ["Maps / Location", "Analytics"], "deployment": "Cloud",
            "growth": "Rapid", "seo_important": False,
        },
    },
}

SYSTEM_LIMITATIONS = [
    "ArchiMind only knows what is written in its rules; technologies or situations not covered by the knowledge base are not considered.",
    "Recommendations are starting points for an architecture discussion, not a substitute for a proof of concept or load test.",
    "Inputs are simplified categories (e.g. Low / Medium / High); real projects sit between categories and change over time.",
    "Cost, licensing and the team's existing skills in specific languages are only partly modelled.",
]


def copy_facts(facts):
    return {k: (list(v) if isinstance(v, list) else v) for k, v in facts.items()}


def init_state():
    defaults = {
        "page": DASHBOARD,
        "facts": copy_facts(DEFAULT_FACTS),   # last submitted answers
        "project": {"name": "My Project", "description": ""},
        "result": None,                       # output of the inference engine
        "form_error": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_to(page):
    st.session_state.page = page


def fill_form(facts, project):
    """Write answers into the form widgets (each widget's key is its fact name)."""
    for name in INPUT_FACT_NAMES:
        value = facts[name]
        st.session_state[name] = list(value) if isinstance(value, list) else value
    st.session_state.project_name = project["name"]
    st.session_state.project_description = project["description"]


def load_sample():
    name = st.session_state.sample_choice
    sample = SAMPLE_PROJECTS[name]
    fill_form(sample["facts"], {"name": name, "description": sample["description"]})


def run_analysis():
    """Form-submit callback: collect the facts and run the inference engine."""
    # Each widget's key is its fact name, so the facts are read straight from session state
    facts = {name: st.session_state[name] for name in INPUT_FACT_NAMES}

    if facts["concurrent_users"] > facts["expected_users"]:
        st.session_state.form_error = ("Concurrent users cannot be higher than the expected total "
                                       "number of users. Please check these two values.")
        return

    st.session_state.form_error = None
    st.session_state.facts = facts
    st.session_state.project = {
        "name": st.session_state.project_name.strip() or "Untitled project",
        "description": st.session_state.project_description.strip(),
    }
    st.session_state.result = run_inference(facts)     # <-- the expert system runs here
    st.session_state.page = RECOMMENDATIONS


def hint(fact_name):
    """format_func for widgets: show a longer description for some options."""
    return lambda value: OPTION_HINTS.get(fact_name, {}).get(value, value)


def require_result():
    """Show a message if no analysis has been run yet. Returns the result or None."""
    result = st.session_state.result
    if result is None:
        st.info("No analysis yet. Complete the project assessment first.")
        st.button("Go to Project Assessment →", type="primary", on_click=go_to, args=(ASSESSMENT,))
    return result


def rejected_alternatives(result, slot):
    """Conclusions for this slot that lost during conflict resolution."""
    return [c for c in result["conflicts"] if c["slot"] == slot]


def show_rule(rule, prefix=""):
    st.markdown(f"{prefix}**`{rule['id']}`** · {rule['category']} · priority {rule['priority']}")
    st.code(describe_rule(rule), language=None, wrap_lines=True)
    st.caption(rule["because"])


def render_slot(result, slot):
    conclusions = get_conclusions(result, slot)
    with st.container(border=True):
        st.markdown(f"**{SLOT_LABELS[slot]}**")
        if not conclusions:
            st.caption("Not required: no rule concluded a recommendation for this project.")
            return

        if slot in SINGLE_VALUE_SLOTS:
            st.markdown(f"##### :blue[{conclusions[0][0]}]")
        else:
            st.markdown("\n".join(f"- {value}" for value, _ in conclusions))

        with st.expander("Why?"):
            for value, rule_ids in conclusions:
                if slot in MULTI_VALUE_SLOTS:
                    st.markdown(f"**{value}**")
                for rule_id in rule_ids:
                    rule = RULES_BY_ID[rule_id]
                    st.markdown(f"Rule **`{rule_id}`**: {rule['because']}")
            for conflict in rejected_alternatives(result, slot):
                st.caption(f"Also considered: *{conflict['dropped_value']}* ({conflict['dropped_rule']}, "
                           f"priority {conflict['dropped_priority']}); not chosen because "
                           f"{conflict['kept_rule']} has priority {conflict['kept_priority']}.")


def count_recommendations(result):
    total = 0
    for slot in SINGLE_VALUE_SLOTS + MULTI_VALUE_SLOTS:
        if slot != "risks":
            total += len(get_conclusions(result, slot))
    return total


def page_dashboard():
    st.title("ArchiMind")
    st.subheader("Software Architecture & Technology Stack Advisor", anchor=False)
    st.write(
        "ArchiMind is a **rule-based expert system** that behaves like an experienced software "
        "architect. Describe the application you want to build (its users, complexity, budget, "
        "data and quality requirements) and ArchiMind recommends an architecture, technology "
        "stack, database, communication protocols and deployment infrastructure, and explains "
        "every recommendation."
    )
    st.button("Start assessment", type="primary", on_click=go_to, args=(ASSESSMENT,))

    categories = sorted({rule["category"] for rule in RULES})
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rules in knowledge base", len(RULES))
    c2.metric("Rule categories", len(categories))
    c3.metric("Input facts", len(INPUT_FACT_NAMES))
    c4.metric("Recommendation areas", len(SINGLE_VALUE_SLOTS) + len(MULTI_VALUE_SLOTS))

    st.divider()
    st.subheader("How an expert system works", anchor=False)
    c1, c2, c3 = st.columns(3)
    with c1.container(border=True):
        st.markdown("##### Knowledge base")
        st.write("Hand-written **IF-THEN production rules** that capture an architect's expertise, "
                 "e.g. *IF data is relational AND ACID transactions are needed THEN recommend PostgreSQL*.")
    with c2.container(border=True):
        st.markdown("##### Inference engine")
        st.write("A **forward-chaining** engine: it matches rules against the known facts, picks one "
                 "rule by priority (conflict resolution), fires it, and repeats until no rule applies.")
    with c3.container(border=True):
        st.markdown("##### Explanation facility")
        st.write("Every conclusion records the rule that produced it, so ArchiMind can show **which "
                 "rules fired, which conditions matched**, and how one conclusion led to another.")

    st.subheader("The assessment process", anchor=False)
    st.markdown(
        "1. **Assessment**: answer structured questions about your project. Each answer becomes a *fact*.\n"
        "2. **Inference**: the engine derives intermediate facts (e.g. *traffic level = High*) and "
        "then recommendations, chaining rules together.\n"
        "3. **Recommendations**: review the proposed architecture and technology stack.\n"
        "4. **Reasoning**: inspect every rule that fired, the matched conditions and resolved conflicts.\n"
        "5. **Summary**: a consolidated stack, key advice, risks, and a downloadable report."
    )

    with st.expander("Rules per category in the knowledge base"):
        rows = []
        for category in categories:
            rules = [r for r in RULES if r["category"] == category]
            rows.append({"Category": category, "Rules": len(rules),
                         "Example rule": describe_rule(rules[0])})
        st.dataframe(rows, hide_index=True)


def page_assessment():
    st.title("Project Assessment")
    st.write("Answer the questions below. Every answer is stored as a **fact** in the expert "
             "system's working memory, and the rules reason over those facts.")

    # Streamlit forgets widget values on other pages, so refill the form with the last answers
    if "app_type" not in st.session_state:
        fill_form(st.session_state.facts, st.session_state.project)

    with st.expander("Load a sample project (useful for demonstrations)"):
        c1, c2 = st.columns([3, 1], vertical_alignment="bottom")
        c1.selectbox("Sample project", list(SAMPLE_PROJECTS), key="sample_choice")
        c2.button("Load into form", on_click=load_sample, width="stretch")

    if st.session_state.form_error:
        st.error(st.session_state.form_error)

    # Each widget's key is its fact name: key="complexity" -> facts["complexity"]
    with st.form("assessment_form", border=False):

        with st.container(border=True):
            st.subheader("1 · Project profile", anchor=False)
            c1, c2 = st.columns(2)
            with c1:
                st.text_input("Project name", key="project_name")
                st.selectbox("Application type", INPUT_OPTIONS["app_type"], key="app_type")
                st.radio("Application complexity", INPUT_OPTIONS["complexity"], key="complexity",
                         horizontal=True,
                         help="Low: CRUD screens. Medium: several modules and business rules. "
                              "High: many interacting domains, complex workflows.")
            with c2:
                st.text_area("Short description (optional)", key="project_description", height=106,
                             help="Used only in the report. The expert system reasons over the "
                                  "structured answers, not over free text.")
                st.select_slider("Expected application growth", INPUT_OPTIONS["growth"], key="growth")

        with st.container(border=True):
            st.subheader("2 · Users & traffic", anchor=False)
            c1, c2 = st.columns(2)
            with c1:
                st.number_input("Expected number of users (registered)", min_value=1,
                                max_value=1_000_000_000, step=1000, key="expected_users",
                                help="Total registered users. For IoT systems, count connected devices too.")
                st.number_input("Expected concurrent users (at peak)", min_value=1,
                                max_value=100_000_000, step=100, key="concurrent_users",
                                help="How many people (or devices) use the system at the same moment.")
            with c2:
                st.selectbox("Geographic distribution of users", INPUT_OPTIONS["geo_distribution"],
                             key="geo_distribution", format_func=hint("geo_distribution"))
                st.selectbox("Workload pattern", INPUT_OPTIONS["workload"], key="workload",
                             format_func=hint("workload"))

        with st.container(border=True):
            st.subheader("3 · Team, budget & deployment", anchor=False)
            c1, c2 = st.columns(2)
            with c1:
                st.slider("Development team size", min_value=1, max_value=100, key="team_size")
                st.select_slider("Team experience level", INPUT_OPTIONS["team_experience"],
                                 key="team_experience")
            with c2:
                st.radio("Project budget", INPUT_OPTIONS["budget"], key="budget", horizontal=True)
                st.radio("Deployment preference", INPUT_OPTIONS["deployment"], key="deployment",
                         horizontal=True)

        with st.container(border=True):
            st.subheader("4 · Data & storage", anchor=False)
            c1, c2, c3 = st.columns(3)
            c1.selectbox("Data structure", INPUT_OPTIONS["data_structure"], key="data_structure",
                         format_func=hint("data_structure"))
            c2.selectbox("Data volume", INPUT_OPTIONS["data_volume"], key="data_volume",
                         format_func=hint("data_volume"))
            c3.selectbox("File & media storage", INPUT_OPTIONS["media_storage"], key="media_storage",
                         format_func=hint("media_storage"))

        with st.container(border=True):
            st.subheader("5 · Functional requirements", anchor=False)
            c1, c2 = st.columns(2)
            with c1:
                st.selectbox("Real-time functionality", INPUT_OPTIONS["realtime"], key="realtime",
                             format_func=hint("realtime"))
                st.selectbox("Background processing", INPUT_OPTIONS["background_processing"],
                             key="background_processing", format_func=hint("background_processing"))
                st.checkbox("Search-engine visibility (SEO) is important", key="seo_important")
            with c2:
                st.multiselect("API requirements", INPUT_OPTIONS["api_requirements"],
                               key="api_requirements",
                               help="Leave empty if the API only serves your own web frontend.")
                st.multiselect("Third-party integrations", INPUT_OPTIONS["integrations"],
                               key="integrations")

        with st.container(border=True):
            st.subheader("6 · Quality requirements", anchor=False)
            c1, c2, c3 = st.columns(3)
            c1.selectbox("Security requirements", INPUT_OPTIONS["security"], key="security",
                         format_func=hint("security"))
            c2.radio("Scalability requirements", INPUT_OPTIONS["scalability"], key="scalability",
                     horizontal=True)
            c3.selectbox("Availability requirements", INPUT_OPTIONS["availability"],
                         key="availability", format_func=hint("availability"))

        st.form_submit_button("Run expert analysis", type="primary", on_click=run_analysis)


def page_recommendations():
    st.title("Expert Recommendations")
    result = require_result()
    if result is None:
        return
    facts = result["facts"]
    st.caption(f"Project: **{st.session_state.project['name']}** · {facts['app_type']}")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rules fired", len(result["trace"]))
    c2.metric("Facts derived", sum(1 for name in DERIVED_FACTS if name in facts))
    c3.metric("Recommendations", count_recommendations(result))
    c4.metric("Conflicts resolved", len(result["conflicts"]))

    architecture = facts.get("architecture")
    with st.container(border=True):
        st.caption("RECOMMENDED ARCHITECTURE")
        st.header(architecture, anchor=False)
        st.write(ARCHITECTURE_PROFILES[architecture]["summary"])
        with st.expander("Why this architecture?"):
            rule_id = result["support"]["architecture"][architecture][0]
            show_rule(RULES_BY_ID[rule_id])
            for conflict in rejected_alternatives(result, "architecture"):
                st.caption(f"Also considered: *{conflict['dropped_value']}* ({conflict['dropped_rule']}, "
                           f"priority {conflict['dropped_priority']}). Lower priority, so not chosen.")

    sections = [
        ("Application stack", ["backend", "frontend", "mobile", "primary_database", "data_services"]),
        ("Communication & messaging", ["api_style", "realtime_protocol", "message_broker",
                                         "caching", "communication"]),
        ("Infrastructure & deployment", ["hosting", "deployment_strategy", "storage",
                                           "infrastructure", "devops"]),
        ("Security, scalability & performance", ["security_measures", "scalability_measures",
                                                    "performance"]),
    ]
    for title, slots in sections:
        st.subheader(title, anchor=False)
        columns = st.columns(3)
        for i, slot in enumerate(slots):
            with columns[i % 3]:
                render_slot(result, slot)

    risks = get_conclusions(result, "risks")
    if risks:
        st.subheader("Risks detected", anchor=False)
        for value, rule_ids in risks:
            st.warning(f"{value}  \n*Rule {', '.join(rule_ids)}*")

    st.divider()
    c1, c2 = st.columns(2)
    c1.button("See the expert reasoning →", on_click=go_to, args=(REASONING,), width="stretch")
    c2.button("Open the assessment summary →", on_click=go_to, args=(SUMMARY,), width="stretch")


def page_reasoning():
    st.title("Expert Reasoning")
    result = require_result()
    if result is None:
        return
    facts, trace = result["facts"], result["trace"]

    st.write("ArchiMind reached its conclusions by **forward chaining**: starting from your answers, "
             "it repeatedly fired every rule whose conditions were all true, adding each conclusion "
             "to working memory so that further rules could use it.")
    with st.expander("How does one inference cycle work?"):
        st.markdown(
            "Each **recognise-act cycle** has three steps:\n"
            "1. **Match**: find all rules whose IF-conditions are true in working memory and that have "
            "not fired yet. These form the *conflict set*.\n"
            "2. **Resolve**: choose one rule: highest *priority* first, then the most *specific* rule "
            "(most conditions), then the rule listed first in the knowledge base.\n"
            "3. **Act**: fire the rule and add its THEN-part to working memory.\n\n"
            "The cycle repeats until the conflict set is empty. Each rule fires at most once "
            "(*refraction*), so reasoning always terminates.\n\n"
            "**Status of a fired rule:** *asserted* a new conclusion · *supported* an existing "
            "conclusion · *rejected* (a higher-priority rule already filled a single-choice slot) · "
            "*overridden* later by a higher-priority rule."
        )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Initial facts", len(result["initial_facts"]))
    c2.metric("Derived facts", sum(1 for name in DERIVED_FACTS if name in facts))
    c3.metric("Rules fired / in KB", f"{len(trace)} / {len(RULES)}")
    c4.metric("Conflicts resolved", len(result["conflicts"]))

    tab_how, tab_trace, tab_memory, tab_conflicts, tab_kb = st.tabs(
        ["How was it decided?", "Inference trace", "Working memory",
         "Conflict resolution", "Knowledge base"])

    with tab_how:
        st.write("Pick any conclusion to see the chain of rules and facts that led to it.")
        options = []
        for slot in SINGLE_VALUE_SLOTS + MULTI_VALUE_SLOTS:
            for value, _ in get_conclusions(result, slot):
                options.append((slot, value))
        slot, value = st.selectbox("Conclusion", options,
                                   format_func=lambda o: f"{SLOT_LABELS[o[0]]}: {o[1]}")
        rule_id = result["support"][slot][value][0]
        st.markdown(f"**{slot} = {value}** was concluded by rule **`{rule_id}`** because all of "
                    f"its conditions were true:")
        lines = explain_how(result, slot, value)
        st.markdown("\n".join("  " * depth + f"- {text}" for depth, text in lines))
        st.caption(RULES_BY_ID[rule_id]["because"])
        others = result["support"][slot][value][1:]
        if others:
            st.caption(f"The same conclusion was also supported by: {', '.join(others)}")

    with tab_trace:
        categories = sorted({entry["rule"]["category"] for entry in trace})
        chosen = st.multiselect("Filter by rule category", categories, placeholder="All categories")
        entries = [e for e in trace if not chosen or e["rule"]["category"] in chosen]

        st.dataframe(
            [{"Cycle": e["cycle"], "Rule": e["rule"]["id"], "Category": e["rule"]["category"],
              "Priority": e["rule"]["priority"],
              "Conclusion": f"{e['rule']['then'][0]} = {format_value(e['rule']['then'][1])}",
              "Status": e["status"],
              "Conflict set size": len(e["conflict_set"])} for e in entries],
            hide_index=True,
        )

        st.markdown("##### Rule-by-rule detail")
        for e in entries:
            rule = e["rule"]
            slot, value = rule["then"]
            label = (f"Cycle {e['cycle']} · {rule['id']} → {slot} = {format_value(value)}  "
                     f"({e['status']})")
            with st.expander(label):
                st.markdown("**IF** (all conditions matched):")
                for condition, actual in e["matched"]:
                    st.markdown(f"- `{describe_condition(condition)}` (actual value: "
                                f"**{format_value(actual)}**)")
                st.markdown(f"**THEN** `{slot} = {format_value(value)}`")
                st.caption(rule["because"])
                st.markdown(f"**Outcome:** {e['status']}. {e['note']}")
                others = e["conflict_set"][1:]
                st.caption(f"Conflict set in this cycle: {len(e['conflict_set'])} rule(s). {rule['id']} "
                           f"(priority {rule['priority']}) was selected first"
                           + (f"; still waiting: {', '.join(others[:8])}"
                              + (f" and {len(others) - 8} more." if len(others) > 8 else ".")
                              if others else "."))

    with tab_memory:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### Initial facts (from the user)")
            st.dataframe([{"Fact": name, "Value": format_value(value)}
                          for name, value in result["initial_facts"].items()], hide_index=True)
        with c2:
            st.markdown("##### Derived facts (intermediate conclusions)")
            derived = [{"Fact": name, "Value": format_value(facts[name]),
                        "Concluded by": ", ".join(result["support"][name][facts[name]])}
                       for name in DERIVED_FACTS if name in facts]
            st.dataframe(derived, hide_index=True)
            st.caption("Derived facts are not answers to questions: the engine inferred them, and "
                       "other rules then used them. This is what makes it *chaining*.")

        st.markdown("##### Final recommendations in working memory")
        rows = []
        for slot in SINGLE_VALUE_SLOTS + MULTI_VALUE_SLOTS:
            for value, rule_ids in get_conclusions(result, slot):
                rows.append({"Slot": slot, "Value": value, "Supported by": ", ".join(rule_ids)})
        st.dataframe(rows, hide_index=True)

    with tab_conflicts:
        st.write("Some recommendations can have only **one** value (one architecture, one primary "
                 "database...). When several rules propose different values, the engine keeps the "
                 "conclusion of the rule with the **highest priority**. Specialised rules are given "
                 "higher priority than general fallback rules.")
        if result["conflicts"]:
            st.dataframe(
                [{"Slot": c["slot"], "Kept": c["kept_value"],
                  "Kept rule": f"{c['kept_rule']} (priority {c['kept_priority']})",
                  "Discarded": c["dropped_value"],
                  "Discarded rule": f"{c['dropped_rule']} (priority {c['dropped_priority']})"}
                 for c in result["conflicts"]],
                hide_index=True,
            )
        else:
            st.success("No conflicts: no two rules proposed different values for the same slot.")

    with tab_kb:
        fired_status = {e["rule"]["id"]: e["status"] for e in trace}
        all_categories = sorted({rule["category"] for rule in RULES})
        chosen = st.multiselect("Filter by category", all_categories, placeholder="All categories",
                                key="kb_filter")
        st.dataframe(
            [{"Rule": r["id"], "Category": r["category"], "Priority": r["priority"],
              "IF": " AND ".join(describe_condition(c) for c in r["if"]),
              "THEN": f"{r['then'][0]} = {format_value(r['then'][1])}",
              "Fired?": fired_status.get(r["id"], "—")}
             for r in RULES if not chosen or r["category"] in chosen],
            hide_index=True,
        )
        st.caption(f"{len(fired_status)} of {len(RULES)} rules fired for this project. The others "
                   "did not fire because at least one of their conditions was false.")


def stack_rows(result):
    rows = []
    for slot in ["architecture", "frontend", "mobile", "backend", "api_style", "primary_database",
                 "data_services", "caching", "message_broker", "realtime_protocol", "storage",
                 "hosting", "infrastructure", "deployment_strategy"]:
        values = [value for value, _ in get_conclusions(result, slot)]
        if values:
            rows.append({"Layer": SLOT_LABELS[slot], "Technology": " · ".join(values)})
    return rows


def build_report(result, project):
    facts = result["facts"]
    architecture = facts["architecture"]
    profile = ARCHITECTURE_PROFILES[architecture]
    lines = [f"# ArchiMind assessment: {project['name']}", ""]
    if project["description"]:
        lines += [project["description"], ""]
    lines += ["## Requirements (input facts)", ""]
    lines += [f"- **{name}**: {format_value(value)}" for name, value in result["initial_facts"].items()]
    lines += ["", f"## Recommended architecture: {architecture}", "", profile["summary"], "",
              "**Strengths:** " + "; ".join(profile["strengths"]),
              "", "**Trade-offs:** " + "; ".join(profile["tradeoffs"]), "",
              "## Technology stack", "", "| Layer | Technology |", "|---|---|"]
    lines += [f"| {row['Layer']} | {row['Technology']} |" for row in stack_rows(result)]
    for slot in ["security_measures", "scalability_measures", "performance", "communication", "devops"]:
        conclusions = get_conclusions(result, slot)
        if conclusions:
            lines += ["", f"## {SLOT_LABELS[slot]}", ""]
            lines += [f"- {value} *(rule {', '.join(ids)})*" for value, ids in conclusions]
    lines += ["", "## Risks", ""]
    risks = get_conclusions(result, "risks")
    lines += [f"- {value}" for value, _ in risks] if risks else ["- No specific risks detected by the rules."]
    lines += ["", "## Limitations", ""] + [f"- {text}" for text in SYSTEM_LIMITATIONS]
    lines += ["", "## Rules fired", ""]
    lines += [f"{e['cycle']}. `{e['rule']['id']}` ({e['status']}): {describe_rule(e['rule'])}"
              for e in result["trace"]]
    return "\n".join(lines)


def page_summary():
    st.title("Assessment Summary")
    result = require_result()
    if result is None:
        return
    facts = result["facts"]
    project = st.session_state.project
    architecture = facts["architecture"]
    profile = ARCHITECTURE_PROFILES[architecture]

    st.subheader(project["name"], anchor=False)
    if project["description"]:
        st.write(project["description"])
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Application type", facts["app_type"])
    c2.metric("Traffic level", facts.get("traffic_level", "-"))
    c3.metric("Team scale", facts.get("team_scale", "-"))
    c4.metric("Rules fired", len(result["trace"]))

    with st.expander("Requirements at a glance (input facts)"):
        st.dataframe([{"Fact": name, "Value": format_value(value)}
                      for name, value in result["initial_facts"].items()], hide_index=True)

    st.subheader("Consolidated technology stack", anchor=False)
    st.table(stack_rows(result), hide_index=True)

    st.subheader(f"Architecture overview: {architecture}", anchor=False)
    st.write(profile["summary"])
    c1, c2 = st.columns(2)
    with c1.container(border=True):
        st.markdown("**Strengths**")
        st.markdown("\n".join(f"- {s}" for s in profile["strengths"]))
    with c2.container(border=True):
        st.markdown("**Trade-offs to manage**")
        st.markdown("\n".join(f"- {t}" for t in profile["tradeoffs"]))

    st.subheader("Key recommendations", anchor=False)
    c1, c2 = st.columns(2)
    for i, slot in enumerate(["security_measures", "scalability_measures", "performance", "devops"]):
        with (c1 if i % 2 == 0 else c2).container(border=True):
            st.markdown(f"**{SLOT_LABELS[slot]}**")
            conclusions = get_conclusions(result, slot)
            if conclusions:
                st.markdown("\n".join(f"- {value}" for value, _ in conclusions))
            else:
                st.caption("No specific advice needed for this project.")

    st.subheader("Potential risks and limitations", anchor=False)
    risks = get_conclusions(result, "risks")
    if risks:
        for value, rule_ids in risks:
            st.warning(f"{value}  \n*Detected by rule {', '.join(rule_ids)}*")
    else:
        st.success("The risk-assessment rules found no problematic combination in your requirements.")
    with st.container(border=True):
        st.markdown("**Limitations of this assessment**")
        st.markdown("\n".join(f"- {text}" for text in SYSTEM_LIMITATIONS))

    st.download_button("Download report (Markdown)", data=build_report(result, project),
                       file_name="archimind_report.md", mime="text/markdown", type="primary")


init_state()

with st.sidebar:
    st.title("ArchiMind")
    st.caption("Software Architecture & Technology Stack Advisor")
    st.radio("Navigation", PAGES, key="page", label_visibility="collapsed")
    st.divider()
    st.caption(f"Knowledge base: **{len(RULES)} rules**")
    if st.session_state.result is not None:
        st.caption(f"Last analysis: **{len(st.session_state.result['trace'])} rules fired** "
                   f"for *{st.session_state.project['name']}*")
    st.caption("Rule-based expert system · forward chaining · no machine learning, no LLM")

PAGE_FUNCTIONS = {
    DASHBOARD: page_dashboard,
    ASSESSMENT: page_assessment,
    RECOMMENDATIONS: page_recommendations,
    REASONING: page_reasoning,
    SUMMARY: page_summary,
}
PAGE_FUNCTIONS[st.session_state.page]()
