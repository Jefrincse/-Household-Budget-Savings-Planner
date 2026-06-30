# 🏡 Household Budget & Savings Planner
A lightweight, modern Python web application built using **Streamlit** that helps households track income, expenses, and savings while providing detailed spending breakdowns.
## 🚀 Quick Start
### 1. Install Dependencies
Make sure you have Python installed, then install the required libraries:
```bash
pip install streamlit pandas plotly
```
### 2. Run the Web Dashboard
Start the Streamlit server from the project directory:
```bash
streamlit run app.py
```
### 3. Run Automated Verification Tests
You can run the built-in testing suite to verify budget and data handling functions:
```bash
python test_budget.py
```
---
## 🛠️ Features
- **Income Tracking**: Add monthly income sources.
- **Categorized Expenses**: Log expenses with description and category (e.g., Food, Travel, Utilities, Other).
- **Savings Analysis**: Instantly calculates total expenses, net savings, and savings rate.
- **Visual Analytics**: Interactive Streamlit charts showcasing a category breakdown of expenditures.
- **Data Persistence**: Automatically stores and reads budget data to/from a local `budget.json` database.
---
## 📚 Concepts Covered
- **Functions**: Encapsulated read/write procedures (`load_data`, `save_data`) and modular computation logic.
- **Lists & Dictionaries**: Structured nested storage representing transactions, categories, and dataset schemas.
- **try/except**: Resilient error handling safeguarding file loading issues and corrupt structures.
- **File Handling (JSON)**: State serialization across user sessions.
- **Streamlit (Extended)**: Custom metrics dashboard, interactive bar graphs, tables, and reactive user forms.
---
## 📁 File Structure
- [app.py](file:///c:/Users/Jefrin%20Raj/OneDrive/Desktop/Anti_Gravity/app.py): The main 55-line Streamlit dashboard application.
- [budget_manager.py](file:///c:/Users/Jefrin%20Raj/OneDrive/Desktop/Anti_Gravity/budget_manager.py): Core library containing back-end processing logic.
- [test_budget.py](file:///c:/Users/Jefrin%20Raj/OneDrive/Desktop/Anti_Gravity/test_budget.py): Testing script validating data persistence, limits, and math logic.
- `budget.json` / `data/`: Local storage containing database backups.
