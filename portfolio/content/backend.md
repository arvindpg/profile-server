# Backend

## Languages

| Language | Experience | How I Use It |
|----------|------------|--------------|
| **Python** | 7+ years | My primary language - APIs, automation, security tooling |
| **Node.js** | 3 years | Monitoring tools, Puppeteer-based automation |
| **TypeScript** | 2 years | Frontend work, type-safe Node.js |

Python is a language that works across many domains - web development, APIs, DevOps scripting, security tooling, and now AI/ML. I made it a point to get proficient in Python so I could move between different areas without having to learn a new language each time. I also appreciate that Python lowers the barrier for non-programmers like scientists and researchers to build things.

## Frameworks

### Python
- **Django** - My go-to for full applications. I've optimized Django REST APIs to achieve 10x improvements in response times through PostgreSQL query optimization.
- **FastAPI** - For microservices. I use SQLAlchemy ORM and Pydantic for data validation.
- **Pytest** - I swear by test-driven development. Code without tests is hard to change confidently.

### Node.js
- **Express** - Basic API development
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
- **RabbitMQ** - Task queues

## What I've Built

A recent example: I built a pluggable platform where security researchers can write custom scripts and invoke them directly from our platform. The main goal was to make it extensible - we can add new integrations without touching core code. It's actively being used now with about 15 scripts integrated. The quality of the platform code directly affects the speed of new integrations.

Another example: I developed a system that enables security engineers to add custom scripts, automatically converting their outputs into Knowledge Graphs and storing them in PostgreSQL. This reduced data integration time from 2-3 days to hours.

## Principles

1. **Code without tests is incomplete** - Code without tests is hard to change confidently, and code without documentation is hard for others to understand.
2. **Design for failure** - I regularly work with asynchronous scan requests processed by pods on spot nodes. This forces me to design for interruption, so I build systems that checkpoint progress and resume without data loss.
3. **Observability is essential** - Logs, metrics, and alerts help developers understand what exactly is happening in complex systems.
