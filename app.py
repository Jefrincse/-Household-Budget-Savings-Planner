import streamlit as st
import json
import pandas as pd

def load_data(path="budget.json"):
    try:
        with open(path, "r") as f: return json.load(f)
    except Exception:
        return {"income": 0.0, "expenses": []}

def save_data(data, path="budget.json"):
    with open(path, "w") as f: json.dump(data, f, indent=2)

st.set_page_config(page_title="Savings Planner", page_icon="🏡")
st.title("🏡 Household Budget & Savings Planner")
data = load_data()

st.sidebar.header("Financial Log")
try:
    inc = st.sidebar.number_input("Income ($)", min_value=0.0, value=float(data["income"]))
    if inc != data["income"]:
        data["income"] = inc
        save_data(data)
except Exception as e:
    st.sidebar.error(f"Input Error: {e}")

with st.sidebar.form("expense_form", clear_on_submit=True):
    title = st.text_input("Expense Description")
    amount = st.number_input("Amount ($)", min_value=0.0)
    cat = st.selectbox("Category", ["Food", "Travel", "Utilities", "Other"])
    if st.form_submit_button("Add Expense") and title and amount > 0:
        data["expenses"].append({"title": title, "amount": amount, "category": cat})
        save_data(data)
        st.rerun()

total_exp = sum(e["amount"] for e in data["expenses"])
savings = data["income"] - total_exp

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${data['income']:,.2f}")
col2.metric("Total Expenses", f"${total_exp:,.2f}")
col3.metric("Savings", f"${savings:,.2f}", delta=f"{((savings/data['income'])*100) if data['income'] > 0 else 0:.1f}% Rate")

if data["expenses"]:
    df = pd.DataFrame(data["expenses"])
    st.subheader("📊 Spending Breakdown")
    st.bar_chart(df.groupby("category")["amount"].sum())
    
    st.subheader("📋 Spending Report")
    st.dataframe(df[["category", "title", "amount"]], use_container_width=True)
    if st.button("Reset Budget Planner"):
        save_data({"income": 0.0, "expenses": []})
        st.rerun()
else:
    st.info("No expenses recorded yet. Add expenses in the sidebar.")
