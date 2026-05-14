# 🛡️ DSM System Automation Framework

![Python](https://img.shields.io/badge/Python-3.14+-3776AB?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-UI%20Automation-2EAD33?logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-Test%20Runner-0A9EDC?logo=pytest&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-Test%20Reports-FF6A00?logo=allure&logoColor=white)
![REST API](https://img.shields.io/badge/REST%20API-Backend%20Validation-7B2CBF)
![Docker](https://img.shields.io/badge/Docker-Local%20Environment-2496ED?logo=docker&logoColor=white)
![POM](https://img.shields.io/badge/Pattern-Page%20Object%20Model-6C63FF)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-CI%20Ready-181717?logo=github&logoColor=white)
![HTML Report](https://img.shields.io/badge/HTML-Report-E34F26?logo=html5&logoColor=white)
![Logging](https://img.shields.io/badge/Logging-Enabled-2F4858)
![Security Flow](https://img.shields.io/badge/Security-Alert%20Lifecycle-C1121F)
![Expected Failure](https://img.shields.io/badge/Expected%20Failure-xfail-B45309)
![Status](https://img.shields.io/badge/Assignment-Cyera%20DSPM-111827)

Automation framework for validating DSPM alert lifecycle workflows using **Python**, **Playwright**, **Pytest**, **Allure**, and **REST API testing**.

Repository:

```bash
https://github.com/shlomi10/dsm_system
```

---

## 📌 Overview

The tested system simulates a DSPM platform that scans cloud/SaaS assets, evaluates security policies, creates alerts, and supports remediation workflows.

Core product flow:

```text
Policies → Scan → Alerts → Remediation → Resolved Alert → Rescan Verification
```

This project includes:

- UI automation for manual remediation
- REST API automation for auto-remediation and rescan verification
- API component-level tests
- Shared infrastructure for pages, API clients, constants, logging, and reports
- Allure reporting
- Failure screenshots
- Playwright traces
- Runtime logs

---

## 🧩 Target Application Context

The tested application is a mock DSPM portal built as an automation testing target.

The system includes:

- Web UI
- REST API
- Local database
- Simulated scan engine
- Seeded policies, alerts, audit trail, remediation, and auto-remediation behavior

Main local services:

```text
Web UI: http://localhost:3000
API:    http://localhost:8080
```
In this automation project, API requests are executed through:
```text
http://localhost:3000/api
```
because the same API routes are available through the running web application host.

Main API endpoints used by the framework:
```text
POST   /api/login
GET    /api/health
GET    /api/policy-config
GET    /api/alerts
POST   /api/scans
PATCH  /api/alerts/:id
POST   /api/alerts/:id/comments
POST   /api/admin/reset
```
Authentication is handled by sending:
```text
Authorization: Bearer <token>
```
The application intentionally avoids overusing data-testid, so the UI framework uses accessible locators such as:
```text
get_by_role()
get_by_label()
visible text
CSS selectors for tables and cells
```

---

## ✅ Automated Scenarios

### 1. UI Test — Manual Remediation Flow

Automated through the frontend.

Flow:

```text
Start scan
Open Alerts
Find alert where:
  Status = Open
  Auto Remediate = OFF
Change status to In Progress
Assign to Security Analyst
Add remediation notes
Click Remediate
Wait for remediation completion
Change status to Resolved
Add resolution comment
Reset environment
```

Test file:

```text
tests/ui/test_manual_remediation.py
```

---

### 2. API Test — Auto-Remediation + Rescan Verification

Automated through REST API.

Flow:

```text
Reset environment
Start scan
Find alert where:
  Status = Open / Remediation In Progress
  Auto Remediate = ON
Wait until auto-remediation completes
Change status to Resolved
Add resolution comment
Start another scan
Verify no identical alert was recreated
Reset environment
```

This test is marked as `xfail` because the assignment intentionally recreates the same alert after rescan.

Test file:

```text
tests/api/test_auto_remediation_rescan.py
```

---

### 3. API Component Tests

Basic API validation for system endpoints.

Covered examples:

```text
Health check
Policy config
Alerts endpoint
Start scan endpoint
Reset environment endpoint
```

Test file:

```text
tests/api/test_api_components.py
```

---

## 🧱 Project Structure

```text
dsm_system/
├── api/
│   ├── api_client.py
│   ├── alerts_api.py
│   ├── reset_api.py
│   └── scans_api.py
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   ├── home_page.py
│   ├── policies_page.py
│   └── alerts_page.py
├── tests/
│   ├── conftest.py
│   ├── api/
│   │   ├── test_api_components.py
│   │   └── test_auto_remediation_rescan.py
│   └── ui/
│       └── test_manual_remediation.py
├── utils/
│   ├── constants.py
│   └── logger.py
├── reports/
│   ├── logs/
│   ├── screenshots/
│   └── traces/
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## 🛠 Tech Stack

- Python
- Playwright
- Pytest
- Pytest-Playwright
- Allure Pytest
- Python Dotenv
- REST API testing through Playwright request context

---

## ✅ Prerequisites

Install before running:

- Python 3.14+
- Docker Desktop
- Git
- Node.js / npm only if you want to use Allure CLI through npm

---

## 🚀 Start the Application

Start the DSPM system:

```bash
docker compose up -d
```

Verify the app:

```text
http://localhost:3000
```

Verify API health:

```text
http://localhost:3000/api/health
```

Stop the system:

```bash
docker compose down
```

View app logs:

```bash
docker compose logs -f
```

---

## ⚙️ Environment Variables

Create `.env` in the project root:

```env
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:3000

API_USERNAME=admin
API_PASSWORD=Aa123456
```

`.env` should not be committed.

Example `.gitignore` entry:

```gitignore
.env
reports/
allure-results/
allure-report/
__pycache__/
.venv/
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/shlomi10/dsm_system.git
cd dsm_system
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

---

## ▶️ Running Tests

Run all tests:

```bash
pytest
```

Run only UI tests:

```bash
pytest tests/ui
```

Run only API tests:

```bash
pytest tests/api
```

Run API component tests only:

```bash
pytest tests/api/test_api_components.py
```

Run the expected-failure API lifecycle test:

```bash
pytest tests/api/test_auto_remediation_rescan.py
```

Run with verbose output:

```bash
pytest -v
```

Run with logs printed:

```bash
pytest -s
```

---

## 📊 Allure Report

Generate Allure results:

```bash
pytest --alluredir=allure-results
```

Generate an Allure HTML report:

```bash
allure generate allure-results -o allure-report
```

Open Allure report:

```bash
allure open allure-report
```

---
## 📄 HTML Report

Generate a standalone HTML report:

```bash
pytest --html=reports/report.html --self-contained-html
```
The report will be created at:
```bash
reports/report.html
```
Open it directly in the browser after the test run.

Required package:
```bash
pytest-html
```
Do not use pytest-html-reporter, it can conflict with newer Pytest versions.

---
## 📁 Runtime Artifacts

Artifacts are generated under:

```text
reports/
├── logs/
│   └── automation.log
├── screenshots/
│   └── <test-name>.png
└── traces/
    └── <test-name>.zip
```

Open Playwright trace:

```bash
playwright show-trace reports/traces/<test-name>.zip
```

---

## 🧾 Logging

The framework writes runtime logs to:

```text
reports/logs/automation.log
```

Logging is implemented in:

```text
utils/logger.py
```

Used by:

```text
api/api_client.py
pages/base_page.py
tests/ui/test_manual_remediation.py
```

The API client logs every request:

```text
GET /api/alerts
POST /api/scans
PATCH /api/alerts/{alert_id}
POST /api/admin/reset
```

---

## 🧪 Test Design

### UI Layer

Uses Page Object Model.

```text
pages/
├── base_page.py
├── login_page.py
├── home_page.py
├── policies_page.py
└── alerts_page.py
```

Responsibilities:

- selectors are stored in page classes
- reusable actions are stored in `BasePage`
- UI test only describes the business flow

---

### API Layer

Uses API wrapper classes.

```text
api/
├── api_client.py
├── alerts_api.py
├── scans_api.py
└── reset_api.py
```

Responsibilities:

- `ApiClient` handles HTTP methods and response validation
- `AlertsApi` handles alert lifecycle actions
- `ScansApi` handles scan creation and scan polling
- `ResetApi` handles environment cleanup

---

## 🔐 Authentication

UI tests login through the frontend.

API tests authenticate through:

```text
POST /api/login
```

Payload:

```json
{
  "username": "admin",
  "password": "Aa123456"
}
```

The token is stored in the Playwright API request context and sent as:

```text
Authorization: Bearer <token>
```

---

## ⚠️ Expected Failure

The test below is expected to fail by product design:

```text
tests/api/test_auto_remediation_rescan.py
```

It verifies that an identical alert is not recreated after remediation and rescan.

The assignment states that the identical alert is intentionally recreated, so the test is marked with:

```python
@pytest.mark.xfail(
    reason="Assignment expects identical alert to be recreated after rescan",
    strict=True
)
```

Expected pytest result:

```text
XFAIL
```

---

## 🧹 Cleanup

Both lifecycle flows reset the system state after execution.

UI cleanup:

```text
Reset environment through the frontend
```

API cleanup:

```text
POST /api/admin/reset
```

Payload:

```json
{
  "confirm": "RESET"
}
```

---

## 🧷 Pytest Configuration

`pytest.ini`:

```ini
[pytest]
testpaths = tests
markers =
    ui: UI tests
    api: API tests
addopts = -ra
```

---

## 📌 Notes

- API tests do not depend on the browser.
- UI and API tests can be executed independently.
- Runtime artifacts are generated automatically.
- `.env` is used for environment-specific values.
- Stable API endpoint paths are kept in `utils/constants.py`.
- The expected failing API lifecycle test is documented with `xfail`.

---

## ✅ Useful Commands

```bash
docker compose up -d
pytest tests/ui
pytest tests/api
pytest --alluredir=allure-results
pytest --html=reports/report.html --self-contained-html
allure generate allure-results -o allure-report
allure open allure-report
docker compose down
```

---

## ❤️ Made By

Built by **Shlomi** — from code to the world, with love.
