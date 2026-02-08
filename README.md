## Directory structure
└── portfolio
    ├── app.py
    ├── content
    │   ├── about.md
    │   ├── backend.md
    │   ├── devops.md
    │   ├── frontend.md
    │   ├── others.md
    │   └── security.md
    ├── docker-compose.yml
    ├── Dockerfile
    ├── .dockerignore
    ├── .gitignore
    ├── __pycache__
    │   └── run_tui.cpython-312.pyc
    ├── README.md
    ├── requirements.txt
    ├── run_tui.py
    ├── screens
    │   ├── __init__.py
    │   └── portfolio.py
    ├── ssh_server.py
    ├── styles.tcss
    └── test_pty.py

## To DO:
1. Change the Markdown files in portfolio/content/*
2. cd portfolio
3. docker-compose up -d --build
