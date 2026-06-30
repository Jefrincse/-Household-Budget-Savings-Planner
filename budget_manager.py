import json
import os
import uuid
from datetime import datetime

DEFAULT_DATA = {
    "income": [],
    "expenses": [],
    "savings_goal": 0.0,
    "category_budgets": {}
}

EXPENSE_CATEGORIES = [
    "Food",
    "Housing/Rent",
    "Utilities",
    "Transportation/Travel",
    "Entertainment/Leisure",
    "Healthcare",
    "Education",
    "Shopping",
    "Miscellaneous"
]

def load_data(filepath: str) -> dict:
    """
    Loads budget data from a JSON file.
    Uses try/except to handle missing, empty, or corrupt files.
    """
    if not os.path.exists(filepath):
        return dict(DEFAULT_DATA)
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Ensure all required keys exist
            for key in DEFAULT_DATA:
                if key not in data:
                    data[key] = DEFAULT_DATA[key]
            return data
    except (json.JSONDecodeError, IOError) as e:
        # If file is corrupt or unreadable, return default and log/handle gracefully
        print(f"Error loading budget data: {e}. Starting with default blank dataset.")
        return dict(DEFAULT_DATA)

def save_data(data: dict, filepath: str) -> bool:
    """
    Saves budget data to a JSON file.
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, default=str)
        return True
    except IOError as e:
        print(f"Error saving budget data: {e}")
        return False

def add_income(data: dict, source: str, amount: float, date_str: str) -> str:
    """
    Adds an income entry. Performs basic input validation.
    Returns status message or raises ValueError.
    """
    if not source.strip():
        raise ValueError("Income source cannot be empty.")
    
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Income amount must be a valid numeric value.")

    if amount <= 0:
        raise ValueError("Income amount must be greater than zero.")

    # Validate date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    new_income = {
        "source": source.strip(),
        "amount": amount,
        "date": date_str,
        "id": str(uuid.uuid4()) # Unique UUID
    }
    data["income"].append(new_income)
    return "Income added successfully!"

def add_expense(data: dict, title: str, amount: float, category: str, date_str: str) -> str:
    """
    Adds an expense entry. Performs basic validation.
    Returns status message or raises ValueError.
    """
    if not title.strip():
        raise ValueError("Expense title cannot be empty.")
    
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Expense amount must be a valid numeric value.")

    if amount <= 0:
        raise ValueError("Expense amount must be greater than zero.")

    if category not in EXPENSE_CATEGORIES:
        raise ValueError(f"Invalid expense category. Choose from: {', '.join(EXPENSE_CATEGORIES)}")

    # Validate date
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")

    new_expense = {
        "title": title.strip(),
        "amount": amount,
        "category": category,
        "date": date_str,
        "id": str(uuid.uuid4()) # Unique UUID
    }
    data["expenses"].append(new_expense)
    return "Expense logged successfully!"

def delete_income(data: dict, income_id: int) -> bool:
    """
    Deletes an income entry by its unique ID.
    """
    initial_len = len(data["income"])
    data["income"] = [inc for inc in data["income"] if inc.get("id") != income_id]
    return len(data["income"]) < initial_len

def delete_expense(data: dict, expense_id: int) -> bool:
    """
    Deletes an expense entry by its unique ID.
    """
    initial_len = len(data["expenses"])
    data["expenses"] = [exp for exp in data["expenses"] if exp.get("id") != expense_id]
    return len(data["expenses"]) < initial_len

def update_savings_goal(data: dict, goal_amount: float) -> str:
    """
    Updates the overall savings goal.
    """
    try:
        goal_amount = float(goal_amount)
    except (TypeError, ValueError):
        raise ValueError("Savings goal must be a numeric value.")

    if goal_amount < 0:
        raise ValueError("Savings goal cannot be negative.")
    data["savings_goal"] = goal_amount
    return "Savings goal updated successfully!"

def update_category_budget(data: dict, category: str, limit_amount: float) -> str:
    """
    Sets or updates a monthly budget limit for a specific expense category.
    """
    if category not in EXPENSE_CATEGORIES:
        raise ValueError("Invalid category.")
    try:
        limit_amount = float(limit_amount)
    except (TypeError, ValueError):
        raise ValueError("Budget limit must be a numeric value.")

    if limit_amount < 0:
        raise ValueError("Budget limit cannot be negative.")
    
    if "category_budgets" not in data:
        data["category_budgets"] = {}
        
    if limit_amount == 0:
        if category in data["category_budgets"]:
            del data["category_budgets"][category]
    else:
        data["category_budgets"][category] = limit_amount
    return f"Budget limit for {category} updated."

def get_financial_summary(data: dict) -> dict:
    """
    Calculates key metrics: total income, total expenses, savings, and savings rate.
    Also returns aggregated expenses by category.
    """
    total_income = sum(item["amount"] for item in data["income"])
    total_expense = sum(item["amount"] for item in data["expenses"])
    savings = total_income - total_expense
    
    savings_rate = 0.0
    if total_income > 0:
        savings_rate = (savings / total_income) * 100
        
    # Aggregate expenses by category
    by_category = {cat: 0.0 for cat in EXPENSE_CATEGORIES}
    for exp in data["expenses"]:
        cat = exp["category"]
        if cat in by_category:
            by_category[cat] += exp["amount"]
        else:
            by_category[cat] = exp["amount"]
            
    # Filter categories with 0 spent to clean up presentation
    active_categories = {k: v for k, v in by_category.items() if v > 0}

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "savings": savings,
        "savings_rate": savings_rate,
        "expenses_by_category": active_categories,
        "savings_goal": data.get("savings_goal", 0.0),
        "category_budgets": data.get("category_budgets", {})
    }
