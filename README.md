
```markdown
# 🏨 Restful Booker API Test Framework

A scalable, robust, and data-driven API testing framework built with **Python**, **Pytest**, and **Requests**. This suite provides comprehensive coverage for the Restful Booker API, including automated functional tests, schema validation, and performance benchmarks.

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.10+
* **Test Runner:** [Pytest](https://pytest.org) for functional automation and DDT
* **HTTP Client:** [Requests](https://requests.readthedocs.io) for core API interaction
* **Performance:** [Locust](https://locust.io) for load and stress testing
* **Reporting:** [Allure Report](https://qameta.io/allure-report/) for detailed visual analytics
* **Validation:** [Pydantic](https://docs.pydantic.dev/) for strict response schema enforcement
* **CI/CD:** Optimized for [Jenkins](https://www.jenkins.io/) integration and automated pipeline execution
* **Environment:** [Python-dotenv](https://pypi.org/project/python-dotenv/) for managing secrets and environment variables

---

## 📂 Project Structure

```text
restful_booker_tests/
├── config/              # ⚙️ Configuration & Environment management (config.py)
├── core/                # 🧱 Base API Client (Requests wrapping & logging)
├── data/                # 📄 JSON Test Data (Input for DDT)
├── performance/         # 📈 Locust performance scripts (locustfile.py)
├── schemas/             # 🛡️ Pydantic Models (Response validation)
├── services/            # 🧠 Service Object Model (Business Logic)
├── tests/               # 🧪 Test Scripts (Pytest functional tests)
├── utils/               # 🔧 Helpers (Data processor & date generators)
├── .env.example         # 🔒 Template for environment secrets
└── pytest.ini           # ⚡ Pytest and Allure configuration
```

---

## 🚀 Setup & Installation

### 1. Prerequisites

* Python 3.10 or higher
* Allure Commandline (optional, for viewing reports)

### 2. Create Virtual Environment

Isolate dependencies by creating a virtual environment:

**Mac/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate

```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## ⚙️ Configuration

This framework uses a **`.env`** file to manage sensitive credentials and environment switching (Dev/Staging/Prod).

1. **Create the file:**
Copy `.env.example` to a new file named `.env`.
2. **Configure Secrets:**
Open `.env` and update the values. **Never commit this file to Git.**
```ini
# Select Environment: DEV, STAGING, or PROD
TEST_ENV=STAGING

# Credentials
COMMON_USERNAME=admin
COMMON_PASSWORD=password123

```



---

## 🧪 Running Tests

### Standard Run

Runs all tests using the environment defined in your `.env` file.

```bash
pytest

```

### Run in Parallel (Recommended for Speed)

Uses multiple CPU cores to run tests simultaneously.

```bash
pytest -n auto

```

### Switch Environment on the Fly

Override the `.env` file directly from the command line (useful for CI/CD).

```bash
TEST_ENV=PROD pytest

```

### Performance Testing (Locust)
Execute load tests to measure API performance.

```Bash
locust -f performance/locustfile.py
```
### Generate Reporting

Run tests and generate a visual Allure report.

```bash
# 1. Run tests and save results
pytest --alluredir=allure-results

# 2. Serve the report in browser
allure serve allure-results

```

---

## 🧠 How It Works (Architecture)

### 1. Service Object Model (SOM)

Instead of writing `requests.get()` inside test files, we abstract API endpoints into "Service Classes" under the `services/` folder.

* **Benefit:** If an endpoint URL changes, you update it in one place, not 50 tests.

### 2. Data Driven Testing (DDT)

Tests in `tests/test_booking_ddt.py` do not contain data. They read from JSON files in the `data/` folder.

* **Benefit:** One test function can run 100 different scenarios just by adding entries to the JSON file.

### 3. Dynamic Data Processing

We use special placeholders in our JSON data to prevent "stale dates."

* **Input:** `"checkin": "{{today}}"`
* **Runtime:** The framework converts this to `2024-10-25` (or whatever today is).

---

## 📝 QA Guide: How to Add New Test Cases

**You do not need to write Python code to add new test cases.** Follow these steps:

### Step 1: Open the Data File

Navigate to the `data/` folder.

* **`booking_valid.json`**: For positive tests (expecting HTTP 200).
* **`booking_invalid.json`**: For negative tests (expecting HTTP 400/500).

### Step 2: Add Your Data

Copy an existing block and modify the values.

```json
{
  "firstname": "Manual",
  "lastname": "Tester",
  "totalprice": 500,
  "depositpaid": true,
  "bookingdates": {
    "checkin": "{{today}}",       <-- Automatically calculated
    "checkout": "{{next_week}}"   <-- Automatically calculated
  },
  "additionalneeds": "Wheelchair Access"
}

```

### Step 3: Run

Save the file. The next time the automation suite runs (locally or on Jenkins), your new test case will be executed automatically!

```

```
