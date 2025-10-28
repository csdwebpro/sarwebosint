#!/bin/bash
# setup_github_repo.sh

set -e

echo "🔧 DARKFORGE-X GITHUB REPOSITORY SETUP"

# Check prerequisites
command -v git >/dev/null 2>&1 || { echo "Git required but not installed. Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3 required but not installed. Aborting."; exit 1; }

# Initialize git repository
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
fi

# Create necessary files
create_requirements() {
    cat > requirements.txt << 'EOF'
requests>=2.28.0
beautifulsoup4>=4.11.0
urllib3>=1.26.0
lxml>=4.9.0
colorama>=0.4.0
python-dotenv>=0.19.0
pyyaml>=6.0
jinja2>=3.0.0
cryptography>=3.4.0
EOF
}

create_setup_py() {
    cat > setup.py << 'EOF'
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="darkforge-web-exploiter",
    version="1.0.0",
    author="DarkForge-X Security",
    author_email="security@darkforge-x.com",
    description="Advanced Web Application Security Scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/darkforge-web-exploiter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "darkforge=darkforge_cli:main",
        ],
    },
    include_package_data=True,
)
EOF
}

create_gitignore() {
    cat > .gitignore << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Logs
*.log
darkforge_scan.log

# Scan results
*.json
*.html
*.pdf
reports/

# Environment
.env
.venv
env/
venv/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
EOF
}

create_readme() {
    cat > README.md << 'EOF'
# 🚀 DarkForge-X Web Exploitation Framework

![GitHub](https://img.shields.io/github/license/your-username/darkforge-web-exploiter)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![Tests](https://github.com/your-username/darkforge-web-exploiter/actions/workflows/ci-cd.yml/badge.svg)

Advanced, modular web application security scanner for authorized penetration testing and security research.

## ⚡ Features

- **Multi-Priority Scanning**: High, Medium, Low priority vulnerability detection
- **Comprehensive Reconnaissance**: Technology stack detection, endpoint discovery
- **Advanced Exploitation**: SQLi, XSS, Command Injection, Path Traversal
- **CI/CD Ready**: GitHub Actions integration with automated testing
- **Professional Reporting**: JSON, HTML, and PDF report generation

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/your-username/darkforge-web-exploiter.git
cd darkforge-web-exploiter

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
