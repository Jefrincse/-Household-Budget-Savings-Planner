# 🏡 Household Budget & Savings Planner
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://img.shields.io/badge/framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![JSON DB](https://img.shields.io/badge/database-JSON%20File-green.svg)](https://www.json.org/)
A robust, lightweight personal finance dashboard designed to track income, categorize expenses, monitor budget category thresholds, and analyze monthly net savings. The project illustrates core Python programming principles combined with modern web application dashboards.
---
## 🗺️ Project Scope & Features
### 🔹 Basic (Core Functionality)
* **Income Log**: Add monthly income sources with custom titles and dates.
* **Savings Calculation**: Real-time evaluation of total savings and progress percentage.
### 🔸 Intermediate (Categorization & Logic)
* **Categorized Expense Logging**: Organizes spending into standard categories like `Food`, `Housing/Rent`, `Utilities`, `Transportation/Travel`, `Entertainment`, etc.
* **Strict Validation Rules**: Employs robust `try/except` statements validating dates, non-negative amounts, and required descriptors.
### 🚀 Extended (Dashboard & Analytics)
* **Visual Breakdown**: Interactive chart summaries dynamically displaying spending ratios.
* **Savings Goal Target**: Live indicator detailing current progress toward a set financial goal.
* **Threshold Alerts**: Warning alerts notifying the user when category budget limits are breached.
* **Backup & Restore**: Download full database state as a JSON file, or restore from a backup.
---
## 🛠️ Technology Stack
* **Language**: Python 3.8+
* **UI Framework**: Streamlit
* **Data Processing**: Pandas
* **Charts/Visualizations**: Plotly / Native Streamlit Charts
* **Database**: JSON file persistence
---
## 🚀 Getting Started
### 1. Installation
Clone the repository and install the dependencies:
```bash
pip install streamlit pandas plotly
### 2. Running the Application
Launch the interactive web dashboard:

bash
streamlit run app.py

3. Running Automated Tests
Validate database operations, calculation logic, and validation rules using:

bash
python test_budget.py

📂 File Architecture
app.py
: Main frontend file. Features a user-friendly sidebar for logs and main dashboard components.
budget_manager.py
: The underlying processing library implementing file I/O operations, validations, additions, and deletions.
test_budget.py
: Comprehensive test suite validating financial calculations, serialization, deletion, and validation logic.
budget.json / data/: JSON database instances storing serialized state.
