# Allowed values of every input fact; the Streamlit form is built from these lists
INPUT_OPTIONS = {
    "app_type": [
        "E-commerce", "Social Media", "SaaS", "Educational", "Healthcare",
        "Fintech", "Gaming", "Media Streaming", "IoT", "Content / Blog",
        "Internal Business Tool",
    ],
    "complexity": ["Low", "Medium", "High"],
    "budget": ["Low", "Medium", "High"],
    "team_experience": ["Beginner", "Intermediate", "Expert"],
    "realtime": ["None", "One-way updates", "Bidirectional"],
    "media_storage": ["None", "Moderate", "Heavy"],
    "data_structure": ["Relational", "Document-based", "Mixed"],
    "data_volume": ["Small", "Medium", "Large"],
    "workload": ["Read-heavy", "Balanced", "Write-heavy"],
    "security": ["Standard", "High", "Critical"],
    "scalability": ["Low", "Medium", "High"],
    "availability": ["Standard", "High", "Mission-critical"],
    "geo_distribution": ["Single region", "Multi-region", "Global"],
    "api_requirements": [
        "Public API for third parties", "Mobile app clients",
        "Flexible client queries", "Internal service-to-service",
    ],
    "background_processing": ["None", "Light", "Heavy"],
    "integrations": [
        "Payment gateway", "Email / SMS", "Social login",
        "Maps / Location", "Analytics", "ERP / CRM",
    ],
    "deployment": ["Cloud", "On-premises", "No preference"],
    "growth": ["Stable", "Moderate", "Rapid"],
}

NUMERIC_INPUTS = ["expected_users", "concurrent_users", "team_size"]
BOOLEAN_INPUTS = ["seo_important"]
LIST_INPUTS = ["api_requirements", "integrations"]

# Every fact the user provides = the initial working memory
INPUT_FACT_NAMES = list(INPUT_OPTIONS.keys()) + NUMERIC_INPUTS + BOOLEAN_INPUTS


# Slots that hold only ONE value; conflicting rules are resolved by priority
SINGLE_VALUE_SLOTS = [
    "architecture", "backend", "frontend", "mobile", "primary_database",
    "api_style", "realtime_protocol", "message_broker", "hosting",
    "deployment_strategy",
]

# Slots that collect MANY values; every applicable piece of advice is kept
MULTI_VALUE_SLOTS = [
    "data_services", "communication", "caching", "infrastructure", "storage",
    "security_measures", "scalability_measures", "performance", "devops", "risks",
]

# Intermediate facts concluded by the "Fact Derivation" rules
DERIVED_FACTS = [
    "traffic_level", "team_scale", "large_user_base", "needs_independent_scaling",
    "needs_acid_transactions", "needs_high_availability", "compliance_required",
    "needs_async_jobs",
]


# Conclusions that other rules test, defined once so a typo cannot break a reasoning chain
MONOLITH = "Monolithic Architecture"
MODULAR_MONOLITH = "Modular Monolith"
MICROSERVICES = "Microservices Architecture"
EVENT_DRIVEN = "Event-Driven Architecture"
SERVERLESS = "Serverless Architecture"

DJANGO = "Python (Django)"

POSTGRES = "PostgreSQL"
POSTGRES_JSONB = "PostgreSQL with JSONB"
MYSQL = "MySQL"
CASSANDRA = "Apache Cassandra"

GRAPHQL = "GraphQL"
WEBSOCKETS = "WebSockets"
CLOUD_OBJECT_STORAGE = "Cloud object storage (Amazon S3 / Google Cloud Storage)"


RULES = [

    # Fact derivation (priority 100, fires first)
    {"id": "FACT-01", "category": "Fact Derivation", "priority": 100,
     "if": [("concurrent_users", ">=", 10000)],
     "then": ("traffic_level", "High"),
     "because": "10,000 or more simultaneous users is high traffic; the system must be designed for load from day one."},

    {"id": "FACT-02", "category": "Fact Derivation", "priority": 100,
     "if": [("concurrent_users", ">=", 1000), ("concurrent_users", "<", 10000)],
     "then": ("traffic_level", "Medium"),
     "because": "Between 1,000 and 10,000 simultaneous users is moderate traffic: a single small server is no longer enough."},

    {"id": "FACT-03", "category": "Fact Derivation", "priority": 100,
     "if": [("concurrent_users", "<", 1000)],
     "then": ("traffic_level", "Low"),
     "because": "Fewer than 1,000 simultaneous users can be served comfortably by a single application instance."},

    {"id": "FACT-04", "category": "Fact Derivation", "priority": 100,
     "if": [("team_size", "<=", 5)],
     "then": ("team_scale", "Small"),
     "because": "Up to 5 developers form one small team that can share a single codebase easily."},

    {"id": "FACT-05", "category": "Fact Derivation", "priority": 100,
     "if": [("team_size", ">=", 6), ("team_size", "<=", 15)],
     "then": ("team_scale", "Medium"),
     "because": "6 to 15 developers usually split into two or three sub-teams."},

    {"id": "FACT-06", "category": "Fact Derivation", "priority": 100,
     "if": [("team_size", ">", 15)],
     "then": ("team_scale", "Large"),
     "because": "More than 15 developers means several independent teams that need clear ownership boundaries."},

    {"id": "FACT-07", "category": "Fact Derivation", "priority": 100,
     "if": [("expected_users", ">=", 100000)],
     "then": ("large_user_base", True),
     "because": "100,000+ registered users is a large, publicly visible user base."},

    {"id": "FACT-08", "category": "Fact Derivation", "priority": 100,
     "if": [("scalability", "==", "High"), ("traffic_level", "==", "High")],
     "then": ("needs_independent_scaling", True),
     "because": "High traffic combined with high scalability requirements means busy components must scale separately from quiet ones."},

    {"id": "FACT-09", "category": "Fact Derivation", "priority": 100,
     "if": [("scalability", "==", "High"), ("growth", "==", "Rapid")],
     "then": ("needs_independent_scaling", True),
     "because": "Rapid growth with high scalability requirements means parts of the system will outgrow others and need to scale independently."},

    {"id": "FACT-10", "category": "Fact Derivation", "priority": 100,
     "if": [("app_type", "in", ["E-commerce", "Fintech", "Healthcare"])],
     "then": ("needs_acid_transactions", True),
     "because": "Orders, money transfers and medical records must never be half-saved, so they need ACID transactions."},

    {"id": "FACT-11", "category": "Fact Derivation", "priority": 100,
     "if": [("integrations", "contains", "Payment gateway")],
     "then": ("needs_acid_transactions", True),
     "because": "Taking payments requires that payment and order records are updated atomically."},

    {"id": "FACT-12", "category": "Fact Derivation", "priority": 100,
     "if": [("availability", "in", ["High", "Mission-critical"])],
     "then": ("needs_high_availability", True),
     "because": "99.9% or higher availability cannot be met by a single server; redundancy is required."},

    {"id": "FACT-13", "category": "Fact Derivation", "priority": 100,
     "if": [("security", "==", "Critical")],
     "then": ("compliance_required", True),
     "because": "Critical security requirements normally come with regulatory compliance obligations."},

    {"id": "FACT-14", "category": "Fact Derivation", "priority": 100,
     "if": [("app_type", "in", ["Healthcare", "Fintech"])],
     "then": ("compliance_required", True),
     "because": "Healthcare and financial data are regulated (e.g. HIPAA, PCI-DSS, GDPR)."},

    {"id": "FACT-15", "category": "Fact Derivation", "priority": 100,
     "if": [("background_processing", "in", ["Light", "Heavy"])],
     "then": ("needs_async_jobs", True),
     "because": "Background processing must run asynchronously, outside the user's web request."},

    {"id": "FACT-16", "category": "Fact Derivation", "priority": 100,
     "if": [("integrations", "contains", "Email / SMS")],
     "then": ("needs_async_jobs", True),
     "because": "Sending emails or SMS is slow and may fail, so it should be done asynchronously by background jobs."},

    # Architecture selection
    {"id": "ARCH-01", "category": "Architecture", "priority": 96,
     "if": [("app_type", "==", "IoT"), ("traffic_level", "in", ["Medium", "High"])],
     "then": ("architecture", EVENT_DRIVEN),
     "because": "IoT devices emit continuous streams of events. In an event-driven design producers publish events and consumers react to them, which absorbs bursts and decouples data ingestion from processing."},

    {"id": "ARCH-02", "category": "Architecture", "priority": 95,
     "if": [("complexity", "==", "High"), ("needs_independent_scaling", "==", True),
            ("team_scale", "in", ["Medium", "Large"])],
     "then": ("architecture", MICROSERVICES),
     "because": "High complexity plus components that must scale independently is the classic case for microservices, and the team is large enough to own separate services."},

    {"id": "ARCH-03", "category": "Architecture", "priority": 85,
     "if": [("team_scale", "==", "Large"), ("complexity", "==", "High")],
     "then": ("architecture", MICROSERVICES),
     "because": "A large team on a complex product moves faster when split into autonomous teams that each own and deploy their own service (Conway's Law)."},

    {"id": "ARCH-04", "category": "Architecture", "priority": 80,
     "if": [("budget", "==", "Low"), ("traffic_level", "==", "Low"),
            ("complexity", "in", ["Low", "Medium"]), ("deployment", "==", "Cloud"),
            ("realtime", "!=", "Bidirectional"),
            ("team_experience", "in", ["Intermediate", "Expert"])],
     "then": ("architecture", SERVERLESS),
     "because": "Low traffic on a tight budget suits pay-per-request serverless functions: there are no idle servers to pay for and no infrastructure to manage."},

    {"id": "ARCH-05", "category": "Architecture", "priority": 70,
     "if": [("team_scale", "==", "Small"), ("complexity", "==", "Low")],
     "then": ("architecture", MONOLITH),
     "because": "A small team building a simple application is fastest with a single deployable codebase that is simple to develop, test and deploy."},

    {"id": "ARCH-06", "category": "Architecture", "priority": 60,
     "if": [("complexity", "in", ["Medium", "High"])],
     "then": ("architecture", MODULAR_MONOLITH),
     "because": "Medium or high complexity needs clear module boundaries, but without a proven need for independent scaling the operational cost of microservices is not justified. Modules can later be extracted into services."},

    {"id": "ARCH-07", "category": "Architecture", "priority": 55,
     "if": [("complexity", "==", "Low"), ("team_scale", "in", ["Medium", "Large"])],
     "then": ("architecture", MODULAR_MONOLITH),
     "because": "Several developers working on one simple codebase benefit from well-defined modules that give each sub-team clear ownership, while still deploying as one unit."},

    # Backend technology
    {"id": "BACK-01", "category": "Backend", "priority": 95,
     "if": [("traffic_level", "==", "High"), ("needs_independent_scaling", "==", True),
            ("team_experience", "==", "Expert")],
     "then": ("backend", "Go (Gin / Fiber)"),
     "because": "Go compiles to fast native binaries and uses lightweight goroutines, giving high throughput and low memory per instance. That suits an expert team serving very high traffic."},

    {"id": "BACK-02", "category": "Backend", "priority": 90,
     "if": [("needs_acid_transactions", "==", True), ("complexity", "==", "High"),
            ("team_scale", "in", ["Medium", "Large"])],
     "then": ("backend", "Java (Spring Boot)"),
     "because": "Spring Boot offers mature declarative transaction management, strong typing and a large enterprise ecosystem, which suit complex transactional domains."},

    {"id": "BACK-03", "category": "Backend", "priority": 88,
     "if": [("deployment", "==", "On-premises"), ("app_type", "==", "Internal Business Tool")],
     "then": ("backend", "C# (ASP.NET Core)"),
     "because": "On-premises internal business tools usually live in Microsoft-centric environments (Active Directory, Windows Server, SQL Server), which ASP.NET Core integrates with naturally."},

    {"id": "BACK-04", "category": "Backend", "priority": 85,
     "if": [("realtime", "==", "Bidirectional")],
     "then": ("backend", "Node.js (NestJS + Socket.IO)"),
     "because": "Node.js uses a non-blocking event loop that keeps thousands of open connections cheaply, and Socket.IO provides mature real-time messaging."},

    {"id": "BACK-05", "category": "Backend", "priority": 80,
     "if": [("background_processing", "==", "Heavy"), ("data_volume", "in", ["Medium", "Large"])],
     "then": ("backend", "Python (FastAPI)"),
     "because": "Heavy data processing benefits from Python's data ecosystem (pandas, NumPy, Celery). FastAPI adds a fast, asynchronous, typed API layer."},

    {"id": "BACK-06", "category": "Backend", "priority": 60,
     "if": [("team_experience", "==", "Beginner")],
     "then": ("backend", DJANGO),
     "because": "Django is 'batteries included' (ORM, admin panel, authentication, secure defaults) and Python is easy to learn, so it suits a beginner team."},

    {"id": "BACK-07", "category": "Backend", "priority": 50,
     "if": [("team_experience", "in", ["Intermediate", "Expert"])],
     "then": ("backend", "Node.js (NestJS / Express with TypeScript)"),
     "because": "A TypeScript backend lets an experienced team use one language for both frontend and backend, backed by a very large package ecosystem."},

    # Frontend technology (web and mobile)
    {"id": "FRONT-01", "category": "Frontend", "priority": 92,
     "if": [("app_type", "==", "Gaming")],
     "then": ("frontend", "Game client (Phaser / Unity WebGL) + React for menus"),
     "because": "Games need a rendering loop and asset pipeline that UI frameworks do not provide. A game engine renders gameplay while React handles menus, accounts and store pages."},

    {"id": "FRONT-02", "category": "Frontend", "priority": 90,
     "if": [("seo_important", "==", True)],
     "then": ("frontend", "Next.js (React with SSR / SSG)"),
     "because": "Search engines index server-rendered HTML best. Next.js renders pages on the server or at build time, which improves SEO and first-load speed."},

    {"id": "FRONT-03", "category": "Frontend", "priority": 91,
     "if": [("backend", "==", DJANGO), ("complexity", "==", "Low")],
     "then": ("frontend", "Django Templates + HTMX"),
     "because": "With a Django backend and a simple UI, server-rendered templates enhanced with HTMX avoid a separate single-page-app project. A beginner team maintains one codebase, and server-rendered HTML is already SEO-friendly."},

    {"id": "FRONT-04", "category": "Frontend", "priority": 80,
     "if": [("app_type", "in", ["Internal Business Tool", "Fintech", "Healthcare"]),
            ("team_scale", "in", ["Medium", "Large"])],
     "then": ("frontend", "Angular (TypeScript)"),
     "because": "Form-heavy enterprise applications built by larger teams benefit from Angular's opinionated structure, built-in forms and validation, and strict TypeScript."},

    {"id": "FRONT-05", "category": "Frontend", "priority": 65,
     "if": [("team_experience", "==", "Beginner")],
     "then": ("frontend", "Vue.js"),
     "because": "Vue has a gentle learning curve and clear documentation, which makes it the most approachable modern UI framework for beginners."},

    {"id": "FRONT-06", "category": "Frontend", "priority": 50,
     "if": [("team_experience", "in", ["Intermediate", "Expert"])],
     "then": ("frontend", "React + TypeScript (Vite SPA)"),
     "because": "React has the largest ecosystem and talent pool, and TypeScript adds type safety for maintainable interactive interfaces."},

    {"id": "FRONT-07", "category": "Frontend", "priority": 60,
     "if": [("api_requirements", "contains", "Mobile app clients")],
     "then": ("mobile", "Cross-platform app (Flutter / React Native)"),
     "because": "One cross-platform codebase delivers both iOS and Android apps for roughly half the cost of two native apps."},

    {"id": "FRONT-08", "category": "Frontend", "priority": 80,
     "if": [("api_requirements", "contains", "Mobile app clients"), ("budget", "==", "High"),
            ("complexity", "==", "High")],
     "then": ("mobile", "Native apps (Swift for iOS, Kotlin for Android)"),
     "because": "A complex mobile experience with a high budget gets the best performance and full access to platform features from native development."},

    # Database selection
    {"id": "DB-01", "category": "Database", "priority": 96,
     "if": [("app_type", "==", "IoT"), ("data_volume", "in", ["Medium", "Large"])],
     "then": ("primary_database", "Time-series DB (TimescaleDB / InfluxDB)"),
     "because": "Sensor data is a stream of timestamped measurements. Time-series databases compress it efficiently and make time-window queries fast."},

    {"id": "DB-02", "category": "Database", "priority": 93,
     "if": [("workload", "==", "Write-heavy"), ("data_volume", "==", "Large"),
            ("app_type", "in", ["Social Media", "Gaming", "Media Streaming", "IoT"])],
     "then": ("primary_database", CASSANDRA),
     "because": "Cassandra's masterless wide-column design scales writes linearly across nodes, which suits huge volumes of feeds, events or game state."},

    {"id": "DB-03", "category": "Database", "priority": 92,
     "if": [("needs_acid_transactions", "==", True), ("geo_distribution", "==", "Global"),
            ("scalability", "==", "High")],
     "then": ("primary_database", "Distributed SQL (CockroachDB / Google Spanner)"),
     "because": "Global users combined with strict transactions need a database that keeps ACID guarantees while replicating data across regions."},

    {"id": "DB-04", "category": "Database", "priority": 90,
     "if": [("data_structure", "==", "Relational"), ("needs_acid_transactions", "==", True)],
     "then": ("primary_database", POSTGRES),
     "because": "Highly relational data that needs ACID transactions (orders, payments, records) is exactly what PostgreSQL does best: strong consistency, foreign keys, constraints and rich SQL."},

    {"id": "DB-05", "category": "Database", "priority": 75,
     "if": [("data_structure", "==", "Mixed")],
     "then": ("primary_database", POSTGRES_JSONB),
     "because": "PostgreSQL's JSONB columns store flexible documents next to relational tables, so one database handles mixed data without running two database systems."},

    {"id": "DB-06", "category": "Database", "priority": 70,
     "if": [("data_structure", "==", "Document-based")],
     "then": ("primary_database", "MongoDB"),
     "because": "Document-shaped data with an evolving schema maps directly onto MongoDB's JSON-like documents, and MongoDB scales horizontally through sharding."},

    {"id": "DB-07", "category": "Database", "priority": 65,
     "if": [("data_structure", "==", "Relational"), ("budget", "==", "Low"),
            ("complexity", "==", "Low")],
     "then": ("primary_database", MYSQL),
     "because": "For a simple, low-budget relational application, MySQL is the most widely available and cheapest option on shared and managed hosting."},

    {"id": "DB-08", "category": "Database", "priority": 55,
     "if": [("data_structure", "==", "Relational")],
     "then": ("primary_database", POSTGRES),
     "because": "PostgreSQL is a robust, free, standards-compliant relational database and the safe default for structured data."},

    {"id": "DB-09", "category": "Database", "priority": 50,
     "if": [("app_type", "in", ["E-commerce", "Content / Blog", "Educational", "Social Media", "Media Streaming"]),
            ("data_volume", "in", ["Medium", "Large"])],
     "then": ("data_services", "Elasticsearch / OpenSearch (full-text search)"),
     "because": "Catalogues and content of this size need relevance-ranked full-text search, typo tolerance and filters that SQL LIKE queries cannot deliver efficiently."},

    {"id": "DB-10", "category": "Database", "priority": 50,
     "if": [("integrations", "contains", "Maps / Location"),
            ("primary_database", "in", [POSTGRES, POSTGRES_JSONB])],
     "then": ("data_services", "PostGIS extension (geospatial queries)"),
     "because": "Location features (nearby search, distances, geofencing) need spatial indexes. PostGIS adds them to the PostgreSQL database that was already recommended."},

    {"id": "DB-11", "category": "Database", "priority": 50,
     "if": [("integrations", "contains", "Analytics"), ("data_volume", "==", "Large")],
     "then": ("data_services", "Analytics data warehouse (BigQuery / Snowflake / ClickHouse)"),
     "because": "Heavy analytical queries on the production database slow it down for users. A column-oriented warehouse handles large-scale reporting separately."},

    {"id": "DB-12", "category": "Database", "priority": 50,
     "if": [("needs_high_availability", "==", True)],
     "then": ("data_services", "Primary-replica replication with automatic failover"),
     "because": "High availability requires the database to survive a server failure: a standby replica takes over automatically."},

    # API communication
    {"id": "API-01", "category": "API & Communication", "priority": 85,
     "if": [("api_requirements", "contains", "Public API for third parties")],
     "then": ("api_style", "REST + OpenAPI specification"),
     "because": "A public API must be easy for any third party to use. REST is universally understood, and an OpenAPI specification provides documentation and generated client SDKs."},

    {"id": "API-02", "category": "API & Communication", "priority": 80,
     "if": [("api_requirements", "contains", "Flexible client queries")],
     "then": ("api_style", GRAPHQL),
     "because": "Clients that need different shapes of data can request exactly the fields they need in one round trip, which avoids over-fetching and endless custom endpoints."},

    {"id": "API-03", "category": "API & Communication", "priority": 50,
     "if": [("api_requirements", "not contains", "Flexible client queries")],
     "then": ("api_style", "REST (JSON over HTTPS)"),
     "because": "Without special query needs, a resource-oriented REST API is the simplest, most widely supported and most cacheable choice."},

    {"id": "API-04", "category": "API & Communication", "priority": 50,
     "if": [("api_requirements", "contains", "Internal service-to-service"),
            ("architecture", "==", MICROSERVICES)],
     "then": ("communication", "gRPC for internal service-to-service calls"),
     "because": "gRPC sends compact binary Protocol Buffers over HTTP/2 with strict contracts, which is faster and safer than JSON for calls between internal services."},

    {"id": "API-05", "category": "API & Communication", "priority": 50,
     "if": [("integrations", "contains", "Payment gateway")],
     "then": ("communication", "Idempotent webhook endpoints for payment callbacks"),
     "because": "Payment providers confirm payments asynchronously through webhooks. The endpoints must be idempotent so a retried notification never double-charges or double-ships."},

    {"id": "API-06", "category": "API & Communication", "priority": 50,
     "if": [("api_requirements", "contains", "Mobile app clients"),
            ("realtime", "in", ["One-way updates", "Bidirectional"])],
     "then": ("communication", "Push notifications (Firebase Cloud Messaging / APNs)"),
     "because": "Mobile apps are often closed, so live updates must reach users through the operating system's push notification services."},

    {"id": "API-07", "category": "API & Communication", "priority": 50,
     "if": [("integrations", "contains", "ERP / CRM")],
     "then": ("communication", "Integration adapter layer with retries, timeouts and circuit breakers"),
     "because": "Enterprise systems are often slow or briefly unavailable. An adapter layer with retries, timeouts and circuit breakers stops their failures from spreading into your application."},

    {"id": "API-08", "category": "API & Communication", "priority": 50,
     "if": [("integrations", "contains", "Email / SMS")],
     "then": ("communication", "Transactional email / SMS provider (SendGrid / Twilio) called from background jobs"),
     "because": "Dedicated providers handle deliverability and spam compliance, and sending from background jobs keeps user requests fast even when the provider is slow."},

    # Real-time communication
    {"id": "RT-01", "category": "Real-time", "priority": 90,
     "if": [("app_type", "==", "Gaming"), ("realtime", "==", "Bidirectional"),
            ("traffic_level", "in", ["Medium", "High"])],
     "then": ("realtime_protocol", "WebRTC data channels / UDP game servers"),
     "because": "Fast multiplayer games need the lowest possible latency. UDP-based transports drop stale packets instead of waiting for re-transmission as TCP-based WebSockets do."},

    {"id": "RT-02", "category": "Real-time", "priority": 80,
     "if": [("realtime", "==", "Bidirectional")],
     "then": ("realtime_protocol", WEBSOCKETS),
     "because": "Chat, collaboration and live interaction need a persistent full-duplex connection on which both client and server can send messages at any time."},

    {"id": "RT-03", "category": "Real-time", "priority": 80,
     "if": [("realtime", "==", "One-way updates")],
     "then": ("realtime_protocol", "Server-Sent Events (SSE)"),
     "because": "When only the server pushes updates (feeds, notifications, live dashboards), SSE is simpler than WebSockets: plain HTTP, automatic reconnection and proxy-friendly."},

    # Caching
    {"id": "CACHE-01", "category": "Caching", "priority": 50,
     "if": [("workload", "==", "Read-heavy"), ("traffic_level", "in", ["Medium", "High"])],
     "then": ("caching", "Redis (cache-aside for frequently repeated queries)"),
     "because": "High read traffic runs the same database queries over and over. Caching the results in Redis (in memory) serves them in microseconds and takes load off the database."},

    {"id": "CACHE-02", "category": "Caching", "priority": 50,
     "if": [("geo_distribution", "in", ["Multi-region", "Global"])],
     "then": ("caching", "CDN (Cloudflare / Amazon CloudFront)"),
     "because": "Users far from the server suffer high latency. A CDN serves static assets from edge locations close to each user."},

    {"id": "CACHE-03", "category": "Caching", "priority": 50,
     "if": [("media_storage", "==", "Heavy")],
     "then": ("caching", "CDN (Cloudflare / Amazon CloudFront)"),
     "because": "Large media files consume a lot of bandwidth. Serving them from a CDN reduces load on the origin servers and speeds up delivery."},

    {"id": "CACHE-04", "category": "Caching", "priority": 50,
     "if": [("traffic_level", "==", "Low"), ("architecture", "in", [MONOLITH, MODULAR_MONOLITH])],
     "then": ("caching", "In-process application cache (framework / LRU cache)"),
     "because": "At low traffic on a single application, a simple in-memory cache inside the app gives most of the benefit without running a separate cache server."},

    # Message queues
    {"id": "MQ-01", "category": "Message Queues", "priority": 95,
     "if": [("architecture", "==", EVENT_DRIVEN)],
     "then": ("message_broker", "Apache Kafka (event streaming)"),
     "because": "An event-driven system needs a durable, high-throughput event log that many consumers can read independently and replay, which is Kafka's core design."},

    {"id": "MQ-02", "category": "Message Queues", "priority": 90,
     "if": [("architecture", "==", MICROSERVICES), ("traffic_level", "==", "High")],
     "then": ("message_broker", "Apache Kafka (event streaming)"),
     "because": "High-traffic microservices should communicate asynchronously through events. Kafka handles millions of messages per second and decouples the services."},

    {"id": "MQ-03", "category": "Message Queues", "priority": 88,
     "if": [("architecture", "==", SERVERLESS), ("needs_async_jobs", "==", True)],
     "then": ("message_broker", "Managed queue (AWS SQS / Google Pub/Sub)"),
     "because": "A serverless system should not run its own broker. Managed queues are pay-per-use, scale automatically and can trigger functions directly."},

    {"id": "MQ-04", "category": "Message Queues", "priority": 80,
     "if": [("background_processing", "==", "Heavy")],
     "then": ("message_broker", "RabbitMQ (reliable task queue)"),
     "because": "Heavy background work needs reliable delivery, acknowledgements, retries and dead-letter queues so that no job is lost, which are RabbitMQ's strengths."},

    {"id": "MQ-05", "category": "Message Queues", "priority": 70,
     "if": [("needs_async_jobs", "==", True)],
     "then": ("message_broker", "Redis-backed job queue (Celery / BullMQ)"),
     "because": "Light background jobs (emails, scheduled tasks) only need a simple job queue. Redis-backed workers are easy to set up and run tasks outside the request cycle."},

    # Cloud infrastructure
    {"id": "CLOUD-01", "category": "Cloud Infrastructure", "priority": 95,
     "if": [("deployment", "==", "On-premises"), ("architecture", "in", [MICROSERVICES, EVENT_DRIVEN])],
     "then": ("hosting", "Self-managed Kubernetes (OpenShift / Rancher)"),
     "because": "Many services on your own hardware need an orchestrator for scheduling, self-healing and scaling. OpenShift or Rancher provide Kubernetes on-premises."},

    {"id": "CLOUD-02", "category": "Cloud Infrastructure", "priority": 90,
     "if": [("architecture", "in", [MICROSERVICES, EVENT_DRIVEN])],
     "then": ("hosting", "Managed Kubernetes (EKS / GKE / AKS)"),
     "because": "Many independently deployable services require container orchestration. A managed Kubernetes service removes the burden of operating the cluster control plane."},

    {"id": "CLOUD-03", "category": "Cloud Infrastructure", "priority": 88,
     "if": [("architecture", "==", SERVERLESS)],
     "then": ("hosting", "Serverless functions (AWS Lambda / Google Cloud Functions)"),
     "because": "A serverless architecture is built from functions-as-a-service that scale to zero and are billed per request."},

    {"id": "CLOUD-04", "category": "Cloud Infrastructure", "priority": 85,
     "if": [("deployment", "==", "On-premises")],
     "then": ("hosting", "Docker containers on on-premises servers (Nginx reverse proxy)"),
     "because": "On-premises deployments are simplest and most portable when the application is packaged in Docker containers behind an Nginx reverse proxy."},

    {"id": "CLOUD-05", "category": "Cloud Infrastructure", "priority": 70,
     "if": [("budget", "==", "Low"), ("traffic_level", "==", "Low")],
     "then": ("hosting", "PaaS (Render / Railway / Heroku)"),
     "because": "A Platform-as-a-Service deploys straight from Git with no server administration and a low monthly cost, which is ideal for small, low-traffic projects."},

    {"id": "CLOUD-06", "category": "Cloud Infrastructure", "priority": 60,
     "if": [("deployment", "in", ["Cloud", "No preference"])],
     "then": ("hosting", "Managed containers (Google Cloud Run / AWS ECS / Azure App Service)"),
     "because": "Containers on a managed platform give portability and auto-scaling without managing servers or Kubernetes."},

    {"id": "CLOUD-07", "category": "Cloud Infrastructure", "priority": 50,
     "if": [("needs_high_availability", "==", True)],
     "then": ("infrastructure", "Load balancer + multiple instances across availability zones"),
     "because": "No single server or data centre may be a single point of failure. A load balancer spreads traffic across instances in different zones and removes unhealthy ones."},

    {"id": "CLOUD-08", "category": "Cloud Infrastructure", "priority": 50,
     "if": [("availability", "==", "Mission-critical"),
            ("geo_distribution", "in", ["Multi-region", "Global"])],
     "then": ("infrastructure", "Active-active multi-region deployment with DNS failover"),
     "because": "99.99% availability for users in several regions means surviving the loss of an entire cloud region, so traffic is served from several regions with automatic DNS failover."},

    {"id": "CLOUD-09", "category": "Cloud Infrastructure", "priority": 50,
     "if": [("architecture", "==", MICROSERVICES)],
     "then": ("infrastructure", "API Gateway (Kong / AWS API Gateway)"),
     "because": "Clients should not call dozens of services directly. An API gateway provides one entry point for routing, authentication, rate limiting and response aggregation."},

    {"id": "CLOUD-10", "category": "Cloud Infrastructure", "priority": 50,
     "if": [("budget", "==", "Low"), ("deployment", "in", ["Cloud", "No preference"])],
     "then": ("infrastructure", "Cloud cost controls (budget alerts, right-sizing, scale-to-zero)"),
     "because": "On a low budget an unexpected cloud bill is a real risk. Budget alerts, right-sized instances and scale-to-zero keep costs predictable."},

    # Storage
    {"id": "STORE-01", "category": "Storage", "priority": 50,
     "if": [("media_storage", "in", ["Moderate", "Heavy"]),
            ("deployment", "in", ["Cloud", "No preference"])],
     "then": ("storage", CLOUD_OBJECT_STORAGE),
     "because": "Images, documents and videos belong in object storage, not in the database: practically unlimited capacity, very high durability and a low cost per GB."},

    {"id": "STORE-02", "category": "Storage", "priority": 50,
     "if": [("media_storage", "in", ["Moderate", "Heavy"]), ("deployment", "==", "On-premises")],
     "then": ("storage", "Self-hosted S3-compatible object storage (MinIO)"),
     "because": "On-premises systems can still use object storage. MinIO is self-hosted and S3-compatible, so the code stays portable to the cloud later."},

    {"id": "STORE-03", "category": "Storage", "priority": 50,
     "if": [("media_storage", "==", "Heavy"), ("data_volume", "==", "Large")],
     "then": ("storage", "Storage lifecycle policies (move old media to cold storage)"),
     "because": "Large media libraries consist mostly of old, rarely accessed files. Lifecycle rules move them automatically to much cheaper cold-storage tiers."},

    # Security
    {"id": "SEC-01", "category": "Security", "priority": 50,
     "if": [("security", "in", ["Standard", "High", "Critical"])],
     "then": ("security_measures", "HTTPS/TLS everywhere, hashed passwords (Argon2/bcrypt), OWASP Top 10 protections"),
     "because": "These are baseline protections that every internet-facing application needs, whatever its security level."},

    {"id": "SEC-02", "category": "Security", "priority": 50,
     "if": [("security", "in", ["High", "Critical"])],
     "then": ("security_measures", "Multi-factor authentication + OAuth 2.0 / OpenID Connect"),
     "because": "Elevated security requirements call for strong, standards-based authentication. MFA stops most account-takeover attacks."},

    {"id": "SEC-03", "category": "Security", "priority": 50,
     "if": [("compliance_required", "==", True)],
     "then": ("security_measures", "Encryption at rest (AES-256) and tamper-proof audit logging"),
     "because": "Regulated data must stay protected even if storage is stolen, and every access must be traceable for auditors."},

    {"id": "SEC-04", "category": "Security", "priority": 50,
     "if": [("app_type", "==", "Healthcare")],
     "then": ("security_measures", "HIPAA safeguards: signed BAA with the hosting provider, role-based access to patient data"),
     "because": "Health data is protected by regulations such as HIPAA, which require contractual safeguards with providers and strict access control."},

    {"id": "SEC-05", "category": "Security", "priority": 50,
     "if": [("integrations", "contains", "Payment gateway")],
     "then": ("security_measures", "PCI-DSS: tokenised payments via Stripe / Adyen, never store card numbers"),
     "because": "Letting a PCI-certified provider handle card data keeps your system out of most PCI-DSS scope and avoids storing sensitive card numbers."},

    {"id": "SEC-06", "category": "Security", "priority": 50,
     "if": [("api_requirements", "contains", "Public API for third parties")],
     "then": ("security_measures", "API keys / OAuth scopes with rate limiting and throttling"),
     "because": "Public APIs are used by unknown clients. Keys identify them, and rate limits prevent abuse and denial of service."},

    {"id": "SEC-07", "category": "Security", "priority": 50,
     "if": [("integrations", "contains", "Social login")],
     "then": ("security_measures", "OpenID Connect social login using Authorization Code flow + PKCE"),
     "because": "Social login must use the secure OAuth 2.0 authorization-code flow with PKCE to prevent tokens from being intercepted."},

    {"id": "SEC-08", "category": "Security", "priority": 50,
     "if": [("architecture", "==", MICROSERVICES), ("security", "in", ["High", "Critical"])],
     "then": ("security_measures", "Mutual TLS between services (service mesh: Istio / Linkerd)"),
     "because": "In a microservice system the internal network is also an attack surface. mTLS authenticates and encrypts every service-to-service call (zero trust)."},

    {"id": "SEC-09", "category": "Security", "priority": 50,
     "if": [("security", "==", "Critical")],
     "then": ("security_measures", "Secrets manager (HashiCorp Vault / AWS KMS) + regular penetration testing"),
     "because": "Critical systems must never keep credentials in code or config files, and must be tested regularly with real attack techniques."},

    {"id": "SEC-10", "category": "Security", "priority": 50,
     "if": [("geo_distribution", "in", ["Multi-region", "Global"])],
     "then": ("security_measures", "GDPR & data-residency compliance (e.g. keep EU personal data in EU regions)"),
     "because": "Serving users in several jurisdictions brings privacy laws such as GDPR, which restrict where personal data may be stored and processed."},

    {"id": "SEC-11", "category": "Security", "priority": 50,
     "if": [("large_user_base", "==", True)],
     "then": ("security_measures", "Web Application Firewall (WAF) + DDoS protection"),
     "because": "Popular applications attract automated attacks. A WAF blocks common exploits and DDoS protection absorbs traffic floods."},

    {"id": "SEC-12", "category": "Security", "priority": 50,
     "if": [("realtime_protocol", "==", WEBSOCKETS)],
     "then": ("security_measures", "Authenticate WebSocket handshakes and validate every message"),
     "because": "WebSocket connections bypass normal per-request authentication, so tokens must be checked when the connection opens and every message must be validated."},

    {"id": "SEC-13", "category": "Security", "priority": 50,
     "if": [("media_storage", "in", ["Moderate", "Heavy"])],
     "then": ("security_measures", "Validate and malware-scan uploads; serve private files through signed URLs"),
     "because": "User uploads are a common attack vector (malware, oversized files, path tricks), and private files must never be publicly guessable."},

    # Scalability
    {"id": "SCALE-01", "category": "Scalability", "priority": 50,
     "if": [("scalability", "in", ["Medium", "High"]),
            ("architecture", "in", [MONOLITH, MODULAR_MONOLITH, MICROSERVICES, EVENT_DRIVEN])],
     "then": ("scalability_measures", "Stateless application servers with horizontal auto-scaling"),
     "because": "If servers keep no session state, identical instances can be added or removed behind the load balancer as demand changes. (Serverless platforms already do this automatically.)"},

    {"id": "SCALE-02", "category": "Scalability", "priority": 50,
     "if": [("workload", "==", "Read-heavy"), ("large_user_base", "==", True)],
     "then": ("scalability_measures", "Database read replicas"),
     "because": "A large user base that reads far more than it writes can be served by read-only copies of the database, multiplying read capacity."},

    {"id": "SCALE-03", "category": "Scalability", "priority": 50,
     "if": [("data_volume", "==", "Large"), ("primary_database", "in", [POSTGRES, POSTGRES_JSONB, MYSQL])],
     "then": ("scalability_measures", "Table partitioning first, then sharding when one database node is outgrown"),
     "because": "Very large relational tables slow down queries and maintenance. Partitioning splits them, and sharding spreads data across several servers."},

    {"id": "SCALE-04", "category": "Scalability", "priority": 50,
     "if": [("realtime_protocol", "==", WEBSOCKETS), ("traffic_level", "==", "High")],
     "then": ("scalability_measures", "Redis Pub/Sub backplane for horizontally scaled WebSocket servers"),
     "because": "With many WebSocket servers, a message published on one server must reach clients connected to the others. A Pub/Sub backplane broadcasts it to all servers."},

    {"id": "SCALE-05", "category": "Scalability", "priority": 50,
     "if": [("needs_independent_scaling", "==", True), ("architecture", "==", MICROSERVICES)],
     "then": ("scalability_measures", "Per-service auto-scaling (Kubernetes Horizontal Pod Autoscaler)"),
     "because": "Services with different loads should scale independently, so busy services grow without paying to scale idle ones."},

    {"id": "SCALE-06", "category": "Scalability", "priority": 50,
     "if": [("growth", "==", "Stable"), ("scalability", "==", "Low")],
     "then": ("scalability_measures", "Vertical scaling (upgrade to a larger server) is sufficient"),
     "because": "With stable load and low scalability needs, upgrading one server is cheaper and simpler than building a distributed setup."},

    {"id": "SCALE-07", "category": "Scalability", "priority": 50,
     "if": [("growth", "==", "Rapid")],
     "then": ("scalability_measures", "Load testing and capacity planning (k6 / JMeter) before each growth stage"),
     "because": "Rapid growth exposes bottlenecks suddenly. Regular load tests reveal the limits before real users hit them."},

    # Performance
    {"id": "PERF-01", "category": "Performance", "priority": 50,
     "if": [("primary_database", "in", [POSTGRES, POSTGRES_JSONB]),
            ("traffic_level", "in", ["Medium", "High"])],
     "then": ("performance", "Database connection pooling (PgBouncer)"),
     "because": "Every PostgreSQL connection is a separate server process. A connection pooler lets thousands of clients share a small number of real connections."},

    {"id": "PERF-02", "category": "Performance", "priority": 50,
     "if": [("data_volume", "in", ["Medium", "Large"])],
     "then": ("performance", "Indexing strategy + slow-query profiling (EXPLAIN ANALYZE)"),
     "because": "As tables grow, a missing index turns a millisecond query into a full-table scan."},

    {"id": "PERF-03", "category": "Performance", "priority": 50,
     "if": [("media_storage", "==", "Heavy")],
     "then": ("performance", "Asynchronous media processing (thumbnails, transcoding) in background workers"),
     "because": "Processing video or large images inside the web request would block users for seconds or even minutes."},

    {"id": "PERF-04", "category": "Performance", "priority": 50,
     "if": [("app_type", "==", "Media Streaming")],
     "then": ("performance", "Adaptive bitrate streaming (HLS / DASH)"),
     "because": "Video quality must adapt to each viewer's bandwidth to avoid buffering."},

    {"id": "PERF-05", "category": "Performance", "priority": 50,
     "if": [("api_requirements", "contains", "Mobile app clients")],
     "then": ("performance", "Pagination + response compression (Brotli / gzip) for mobile clients"),
     "because": "Mobile networks are slow and metered. Smaller, paginated responses load faster and use less data."},

    {"id": "PERF-06", "category": "Performance", "priority": 50,
     "if": [("storage", "contains", CLOUD_OBJECT_STORAGE), ("traffic_level", "in", ["Medium", "High"])],
     "then": ("performance", "Direct-to-storage uploads with pre-signed URLs"),
     "because": "Routing large uploads through the app servers wastes their bandwidth and CPU. Clients upload straight to object storage using a short-lived signed URL."},

    {"id": "PERF-07", "category": "Performance", "priority": 50,
     "if": [("api_style", "==", GRAPHQL)],
     "then": ("performance", "DataLoader batching + query complexity limits for GraphQL"),
     "because": "Naive GraphQL resolvers cause the N+1 query problem and allow arbitrarily expensive queries. Batching and complexity limits keep the API fast."},

    # Deployment
    {"id": "DEPLOY-01", "category": "Deployment", "priority": 92,
     "if": [("architecture", "==", MICROSERVICES), ("traffic_level", "==", "High")],
     "then": ("deployment_strategy", "Canary releases with automated rollback"),
     "because": "With heavy traffic, a new version should first reach a small percentage of users. If error rates rise it is rolled back automatically before most users are affected."},

    {"id": "DEPLOY-02", "category": "Deployment", "priority": 90,
     "if": [("availability", "==", "Mission-critical")],
     "then": ("deployment_strategy", "Blue-green deployment"),
     "because": "Mission-critical systems cannot afford downtime. Blue-green keeps the old version running next to the new one and switches traffic instantly, with instant rollback."},

    {"id": "DEPLOY-03", "category": "Deployment", "priority": 70,
     "if": [("availability", "==", "High")],
     "then": ("deployment_strategy", "Rolling deployment"),
     "because": "Replacing instances a few at a time keeps the service available during a release without paying for a full duplicate environment."},

    {"id": "DEPLOY-04", "category": "Deployment", "priority": 50,
     "if": [("availability", "==", "Standard")],
     "then": ("deployment_strategy", "Recreate deployment via CI/CD (short maintenance window)"),
     "because": "With standard availability a short maintenance window is acceptable, so the simplest strategy (stop the old version, start the new one) is enough."},

    {"id": "DEPLOY-05", "category": "Deployment", "priority": 50,
     "if": [("team_size", ">=", 2)],
     "then": ("devops", "CI/CD pipeline (GitHub Actions) with automated tests"),
     "because": "When several developers merge code, an automated build-test-deploy pipeline catches integration bugs early and makes releases repeatable."},

    {"id": "DEPLOY-06", "category": "Deployment", "priority": 50,
     "if": [("architecture", "in", [MICROSERVICES, EVENT_DRIVEN])],
     "then": ("devops", "Distributed tracing + centralised logging (OpenTelemetry, Grafana / ELK)"),
     "because": "One user request crosses many services. Without tracing and central logs, failures are almost impossible to diagnose."},

    {"id": "DEPLOY-07", "category": "Deployment", "priority": 50,
     "if": [("scalability", "==", "High"), ("deployment", "in", ["Cloud", "No preference"])],
     "then": ("devops", "Infrastructure as Code (Terraform)"),
     "because": "Highly scalable environments are rebuilt and resized often. Defining infrastructure as version-controlled code makes changes repeatable and reviewable."},

    {"id": "DEPLOY-08", "category": "Deployment", "priority": 50,
     "if": [("needs_high_availability", "==", True)],
     "then": ("devops", "Monitoring and alerting with SLOs (Prometheus + Grafana, uptime checks)"),
     "because": "You cannot keep an availability promise you do not measure. Alerts tell the team about problems before users notice them."},

    # Risk assessment
    {"id": "RISK-01", "category": "Risk Assessment", "priority": 40,
     "if": [("architecture", "==", MICROSERVICES), ("budget", "==", "Low")],
     "then": ("risks", "Microservices on a low budget: infrastructure and DevOps costs may exceed the budget."),
     "because": "Microservices multiply the number of deployments, environments and monitoring tools that must be paid for."},

    {"id": "RISK-02", "category": "Risk Assessment", "priority": 40,
     "if": [("complexity", "==", "High"), ("team_experience", "==", "Beginner")],
     "then": ("risks", "Skill gap: a beginner team on a highly complex system. Plan mentoring, training or senior hires."),
     "because": "Complex systems fail more often from design mistakes than from technology choices; experience reduces that risk."},

    {"id": "RISK-03", "category": "Risk Assessment", "priority": 40,
     "if": [("complexity", "==", "High"), ("needs_independent_scaling", "==", True),
            ("team_scale", "==", "Small")],
     "then": ("risks", "Team too small for microservices: start with a modular monolith and extract services as the team grows."),
     "because": "The requirements point to microservices, but a team of 5 or fewer cannot operate many services. This is why a modular monolith was preferred."},

    {"id": "RISK-04", "category": "Risk Assessment", "priority": 40,
     "if": [("availability", "==", "Mission-critical"), ("budget", "==", "Low")],
     "then": ("risks", "99.99% availability is unrealistic on a low budget; it needs redundant zones or regions and on-call staff."),
     "because": "Each extra 'nine' of availability roughly multiplies infrastructure and staffing cost."},

    {"id": "RISK-05", "category": "Risk Assessment", "priority": 40,
     "if": [("deployment", "==", "On-premises"), ("growth", "==", "Rapid")],
     "then": ("risks", "On-premises hardware cannot scale elastically: buy capacity ahead of growth or consider a hybrid cloud."),
     "because": "Buying and installing servers takes weeks, while rapid growth can double the load in days."},

    {"id": "RISK-06", "category": "Risk Assessment", "priority": 40,
     "if": [("architecture", "==", SERVERLESS)],
     "then": ("risks", "Serverless trade-offs: vendor lock-in, cold-start latency and execution time limits."),
     "because": "Serverless code depends on one provider's runtime and triggers, and idle functions take time to start."},

    {"id": "RISK-07", "category": "Risk Assessment", "priority": 40,
     "if": [("data_structure", "==", "Document-based"), ("needs_acid_transactions", "==", True)],
     "then": ("risks", "Transactions on a document database: keep money and inventory data strongly consistent (multi-document transactions or a relational store)."),
     "because": "Document databases favour flexibility and availability; strict transactional data needs extra care."},

    {"id": "RISK-08", "category": "Risk Assessment", "priority": 40,
     "if": [("budget", "==", "Low"), ("scalability", "==", "High")],
     "then": ("risks", "High scalability goals with a low budget: rely on managed auto-scaling services and monitor costs closely."),
     "because": "Scaling capacity costs money; without cost controls a traffic spike becomes a billing spike."},

    {"id": "RISK-09", "category": "Risk Assessment", "priority": 40,
     "if": [("primary_database", "==", CASSANDRA)],
     "then": ("risks", "Cassandra is eventually consistent and needs query-first data modelling (no joins)."),
     "because": "Tables must be designed around the exact queries the application runs, which is unfamiliar to SQL developers."},

    {"id": "RISK-10", "category": "Risk Assessment", "priority": 40,
     "if": [("architecture", "==", EVENT_DRIVEN)],
     "then": ("risks", "Event-driven flows are harder to trace and debug; design for eventual consistency and duplicate events."),
     "because": "With asynchronous events there is no single call stack to follow, and messages may arrive late, twice or out of order."},
]

RULES_BY_ID = {rule["id"]: rule for rule in RULES}


# Descriptive knowledge for the Assessment Summary (not rules)
ARCHITECTURE_PROFILES = {
    MONOLITH: {
        "summary": "The whole application (user interface, business logic and data access) is built, tested and deployed as one unit.",
        "strengths": ["Simplest to build, test and deploy", "Easy local development and debugging",
                      "Lowest infrastructure and operating cost"],
        "tradeoffs": ["Every change redeploys the whole application", "Can only scale as one unit",
                      "Code can become tangled as the product grows"],
    },
    MODULAR_MONOLITH: {
        "summary": "One deployable application internally split into well-separated modules (e.g. Users, Orders, Billing) that talk through clear interfaces.",
        "strengths": ["Keeps the simplicity of a single deployment", "Clear ownership and boundaries for sub-teams",
                      "Modules can later be extracted into microservices"],
        "tradeoffs": ["Module boundaries need discipline to enforce", "Still scales as a single unit",
                      "One faulty module can still affect the whole process"],
    },
    MICROSERVICES: {
        "summary": "The system is split into small, independently deployable services, each owning its own data and communicating over the network (APIs or events).",
        "strengths": ["Services scale independently", "Teams deploy autonomously",
                      "A failure can be isolated to one service", "Each service can use the best-fitting technology"],
        "tradeoffs": ["High operational complexity (orchestration, monitoring, tracing)",
                      "Network latency and partial failures", "Data consistency across services is harder",
                      "Higher infrastructure cost"],
    },
    EVENT_DRIVEN: {
        "summary": "Components communicate by publishing and consuming events through a broker, so producers never wait for consumers.",
        "strengths": ["Absorbs traffic bursts", "Very loose coupling between components",
                      "Events can be replayed for new consumers and analytics"],
        "tradeoffs": ["Eventual consistency", "Harder to debug and trace a request end to end",
                      "Must handle duplicate and out-of-order events"],
    },
    SERVERLESS: {
        "summary": "Business logic runs as short-lived cloud functions triggered by HTTP requests or events; the provider manages all servers.",
        "strengths": ["Pay only for actual usage", "Automatic scaling, including to zero",
                      "No servers to patch or manage"],
        "tradeoffs": ["Vendor lock-in", "Cold-start latency", "Execution time and memory limits",
                      "Harder to test locally"],
    },
}
