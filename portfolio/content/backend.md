# Backend & Platform Engineering

I specialize in building secure, optimized, and extensible backend systems using **Python (Django and FastAPI)**. I prioritize technical rigor and systems that "break loudly and early" to prevent silent failures.

### Technical Proficiencies
* **Core:** Python (Type-annotated), Django, FastAPI, Pydantic, Mypy.
* **Databases:** PostgreSQL, MySQL, Google Bigtable, Elasticsearch, Redis, MongoDB.
* **Messaging:** Google Pub/Sub, RabbitMQ.
* **Testing:** Pytest, Unit Testing, Integration Testing.

### High-Impact Projects

#### **Senior Engineer | FireCompass** (Dec 2022 – Present)
* **10x API Performance:** Optimized Django REST APIs by restructuring PostgreSQL queries and indexing, delivering an order of magnitude improvement in response times for an External Attack Surface Management platform.
* **Microservices Architecture:** Developed FastAPI services using SQLAlchemy ORM and engineered a proxy service to orchestrate **Playwright** containers for automated browser-based security testing.
* **Distributed Caching:** Architected a global server-side **Redis** cache with configurable invalidation rules, balancing real-time data accuracy with low latency.
* **Data Integration (5x Speedup):** Built a pluggable system to convert custom security scripts into Knowledge Graphs (PostgreSQL), reducing integration time from **days to hours**.
* **Scalable Data Strategy:** Transitioned asset metadata to **Google Bigtable** and scan data to **Google Cloud Storage** to ensure high availability and reliability.
* **Concurrency Management:** Engineered a system to manage and gracefully abort concurrent security scans using **Google Pub/Sub** for real-time signaling.
* **Global Alerting:** Developed a company-wide Slack alerting library for real-time incident notifications across all microservices.
* **Security Automation:** Integrated 30+ external security tools (Nmap, Nessus, etc.) into a unified automated discovery workflow.

#### **Senior Full Stack Engineer | VuNet Systems** (Jan 2020 – Dec 2022)
* **Identity Management:** Re-architected a Big Data Analytics platform's access control, integrating **LDAP, ADFS SSO (Azure), and OAuth2**.
* **Elasticsearch Upgrade:** Successfully reverse-engineered Kibana components to upgrade Elasticsearch from **6.8 to 7.17**, ensuring stability and modern feature access.
* **Internal Tools:** Designed and implemented an HR Management System (HRMS) integrated directly into the platform's core authentication.

#### **Analyst | Ernst & Young (EY)** (June 2018 – Dec 2019)
* **Workflow Automation:** Enhanced internal Django applications by automating baseline configuration checks using **Ansible**, significantly reducing manual audit effort.

## Languages

| Language | Experience | How I Use It |
|----------|------------|--------------|
| **Python** | 7+ years | My primary language - APIs, automation, security tooling |
| **Node.js** | 6 months| Monitoring tools, Puppeteer-based automation |
| **Go** | 1-2 months| Integrate Plugins for Graphana |


### Python
- **Django** - My go-to for full applications. I've optimized Django REST APIs to achieve 10x improvements in response times through PostgreSQL query optimization.
- **FastAPI** - For microservices. I use SQLAlchemy ORM and Pydantic for data validation.

### Node.js
- **Puppeteer** - Built monitoring tools that perform passive application monitoring across multiple clients

## Databases

### Relational
- **PostgreSQL** - Primary choice. I've worked extensively with query optimization, indexing strategies, and schema design.
- **MySQL** - Used in previous projects

### NoSQL & Specialized
- **Redis** - Architected a global server-side cache for API microservices with configurable caching policies and invalidation rules
- **Elasticsearch/OpenSearch** - Time-series data, search functionality, CVE matching
- **Google Bigtable** - Metadata storage for asset monitoring at scale
- **MongoDB** - Document storage when needed

## Message Queues

- **Google Pub/Sub** - Real-time abort signals for distributed security scans

## Cloud Services

- **Google Cloud Platform** - Pub/Sub, GKE, BigTable, GCS
- **AWS** - Cloud Watch. (EC2 for personal projects)
- **Azure** - Implemented SSO using Oauth2 with Azure AD 
