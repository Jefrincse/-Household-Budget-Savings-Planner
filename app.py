import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import budget_manager as bm
import os

# Page configuration
st.set_page_config(
    page_title="Household Budget & Savings Planner",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern design and custom metric cards
st.markdown("""
<style>
    /* Main container styling */
    .reportview-container {
        background: #f8f9fa;
    }
    
    /* Card design */
    .metric-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #eef2f5;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    }
    
    /* Card headers */
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    /* Card values */
    .metric-val-income {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2ec4b6;
    }
    .metric-val-expense {
        font-size: 1.8rem;
        font-weight: 700;
        color: #e71d36;
    }
    .metric-val-savings {
        font-size: 1.8rem;
        font-weight: 700;
        color: #ff9f1c;
    }
    .metric-val-rate {
        font-size: 1.8rem;
        font-weight: 700;
        color: #011627;
    }
</style>
""", unsafe_allow_html=True)

# File path for saving data
DATA_FILE = "data/budget_data.json"

# Load initial budget data
if 'budget_data' not in st.session_state:
    st.session_state.budget_data = bm.load_data(DATA_FILE)

data = st.session_state.budget_data

# Header Area
st.title("🏡 Household Budget & Savings Planner")
st.markdown("Track income, monitor expense categories, and visually plan your household savings goals.")

# ----------------- SIDEBAR: INPUT MANAGEMENT -----------------
st.sidebar.header("⚙️ Financial Actions")

# Sub-navigation or toggles in Sidebar
action_tab = st.sidebar.radio("Choose Action:", ["Add Record", "Manage Goals", "Upload/Export Data"])

if action_tab == "Add Record":
    st.sidebar.subheader("💰 Income Source")
    with st.sidebar.form(key="income_form", clear_on_submit=True):
        inc_source = st.text_input("Source Name", placeholder="e.g. Salary, Freelance")
        inc_amount = st.number_input("Amount ($)", min_value=0.0, step=50.0, format="%.2f")
        inc_date = st.date_input("Date Received", value=date.today())
        submit_inc = st.form_submit_button("Add Income")
        
        if submit_inc:
            try:
                msg = bm.add_income(data, inc_source, inc_amount, str(inc_date))
                bm.save_data(data, DATA_FILE)
                st.sidebar.success(msg)
                st.rerun()
            except ValueError as e:
                st.sidebar.error(str(e))

    st.sidebar.subheader("💸 Log Expense")
    with st.sidebar.form(key="expense_form", clear_on_submit=True):
        exp_title = st.text_input("Expense Title", placeholder="e.g. Grocery Shop, Gas bill")
        exp_amount = st.number_input("Amount ($)", min_value=0.0, step=10.0, format="%.2f")
        exp_cat = st.selectbox("Category", bm.EXPENSE_CATEGORIES)
        exp_date = st.date_input("Date Paid", value=date.today())
        submit_exp = st.form_submit_button("Log Expense")
        
        if submit_exp:
            try:
                # Check category budget before logging to see if it will overflow
                # Let's log it first, then notify the user if they've exceeded their limit
                msg = bm.add_expense(data, exp_title, exp_amount, exp_cat, str(exp_date))
                bm.save_data(data, DATA_FILE)
                st.sidebar.success(msg)
                st.rerun()
            except ValueError as e:
                st.sidebar.error(str(e))

elif action_tab == "Manage Goals":
    st.sidebar.subheader("🎯 Savings Goal")
    current_goal = data.get("savings_goal", 0.0)
    new_goal = st.sidebar.number_input("Monthly Savings Goal ($)", min_value=0.0, value=float(current_goal), step=100.0)
    if st.sidebar.button("Update Goal"):
        try:
            msg = bm.update_savings_goal(data, new_goal)
            bm.save_data(data, DATA_FILE)
            st.sidebar.success(msg)
            st.rerun()
        except ValueError as e:
            st.sidebar.error(str(e))

    st.sidebar.subheader("🛡️ Category Limits")
    cat_to_limit = st.sidebar.selectbox("Select Category to Limit", bm.EXPENSE_CATEGORIES)
    current_cat_limits = data.get("category_budgets", {})
    current_limit = current_cat_limits.get(cat_to_limit, 0.0)
    new_limit = st.sidebar.number_input(f"Limit for {cat_to_limit} ($)", min_value=0.0, value=float(current_limit), step=50.0, help="Set to 0 to remove limit")
    if st.sidebar.button("Set Limit"):
        try:
            msg = bm.update_category_budget(data, cat_to_limit, new_limit)
            bm.save_data(data, DATA_FILE)
            st.sidebar.success(msg)
            st.rerun()
        except ValueError as e:
            st.sidebar.error(str(e))

elif action_tab == "Upload/Export Data":
    st.sidebar.subheader("📂 Backup & Restore")
    
    # Download JSON
    json_str = json_data = pd.io.json.dumps(data, indent=4)
    st.sidebar.download_button(
        label="📥 Download JSON Data Backup",
        data=json_str,
        file_name="budget_data_backup.json",
        mime="application/json"
    )
    
    # Upload JSON
    uploaded_file = st.sidebar.file_uploader("Upload budget JSON file", type="json")
    if uploaded_file is not None:
        try:
            import json
            uploaded_data = json.load(uploaded_file)
            # Basic schema validation
            for key in bm.DEFAULT_DATA:
                if key not in uploaded_data:
                    uploaded_data[key] = bm.DEFAULT_DATA[key]
            
            if st.sidebar.button("Restore Uploaded Data"):
                st.session_state.budget_data = uploaded_data
                bm.save_data(uploaded_data, DATA_FILE)
                st.sidebar.success("Data restored successfully!")
                st.rerun()
        except Exception as e:
            st.sidebar.error(f"Invalid file format: {e}")

# ----------------- MAIN CONTENT: DASHBOARD & CHARTS -----------------

# Get financials summary
summary = bm.get_financial_summary(data)

# KPI Metrics layout (Custom design cards)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Income</div>
        <div class="metric-val-income">${summary['total_income']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Expenses</div>
        <div class="metric-val-expense">${summary['total_expense']:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    savings_val = summary['savings']
    savings_color_class = "metric-val-savings" if savings_val >= 0 else "metric-val-expense"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Net Savings</div>
        <div class="metric-color-val {savings_color_class}">${savings_val:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Savings Rate</div>
        <div class="metric-val-rate">{summary['savings_rate']:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

# Alerts Section
warnings = []

# Budget Category warnings check
for category, spent in summary["expenses_by_category"].items():
    limit = summary["category_budgets"].get(category, 0.0)
    if limit > 0 and spent > limit:
        warnings.append(f"⚠️ **{category} Budget Exceeded!** Spent: **${spent:,.2f}** (Limit: **${limit:,.2f}**)")

# Savings goal warnings check
savings_goal = summary["savings_goal"]
if savings_goal > 0 and summary["savings"] < savings_goal:
    gap = savings_goal - summary["savings"]
    warnings.append(f"🎯 **Savings Goal Unmet!** You are **${gap:,.2f}** away from your monthly savings goal of **${savings_goal:,.2f}**.")

if warnings:
    with st.expander("🔔 Alerts & Notifications", expanded=True):
        for warning in warnings:
            st.info(warning)

# Main Visualizations Row
col_chart1, col_chart2 = st.columns([3, 2])

with col_chart1:
    st.subheader("📊 Spending Breakdown & Trends")
    
    if not data["expenses"]:
        st.info("No expenses logged yet. Add some expenses in the sidebar to view charts.")
    else:
        # Prepare Plotly Donut Chart
        df_exp = pd.DataFrame(data["expenses"])
        # Group by category
        df_cat = df_exp.groupby("category")["amount"].sum().reset_index()
        
        fig_donut = px.pie(
            df_cat,
            names="category",
            values="amount",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Safe,
            title="Expenses by Category"
        )
        fig_donut.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_donut, use_container_width=True)

with col_chart2:
    st.subheader("🎯 Savings Goal Target")
    if savings_goal <= 0:
        st.info("No Savings Goal set. Set a savings goal in the sidebar 'Manage Goals' panel.")
    else:
        # Gauge chart or progress bar
        current_savings = summary["savings"]
        percent = min(100.0, max(0.0, (current_savings / savings_goal) * 100.0)) if savings_goal > 0 else 0
        
        # Plotly gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = max(0.0, current_savings),
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Savings Target Progress ($)"},
            gauge = {
                'axis': {'range': [None, max(savings_goal, current_savings * 1.2)]},
                'bar': {'color': "#2ec4b6"},
                'steps': [
                    {'range': [0, savings_goal], 'color': "#eef2f5"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': savings_goal
                }
            }
        ))
        fig_gauge.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=250)
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.write(f"Goal Achieved: **{percent:.1f}%** of **${savings_goal:,.2f}** target.")

# ----------------- TABS: DETAILS & TRANSACTION MANAGEMENT -----------------
st.subheader("🔍 Transaction Details & Budgets")

tab_exp, tab_inc, tab_budgets = st.tabs(["💸 Expense Logs", "💰 Income Logs", "🛡️ Category Budgets"])

with tab_exp:
    if not data["expenses"]:
        st.info("No expenses logged.")
    else:
        df_exp_full = pd.DataFrame(data["expenses"])
        # Format for nicer view
        df_exp_view = df_exp_full.copy()
        df_exp_view["amount"] = df_exp_view["amount"].apply(lambda x: f"${x:,.2f}")
        df_exp_view = df_exp_view.sort_values(by="date", ascending=False)
        
        st.dataframe(
            df_exp_view[["date", "title", "category", "amount"]],
            use_container_width=True,
            column_config={
                "date": "Date Paid",
                "title": "Item Description",
                "category": "Expense Category",
                "amount": "Cost"
            }
        )
        
        # Row deletion UI
        st.write("---")
        st.markdown("### 🗑️ Delete Expense Entry")
        delete_options = {
            f"{x['date']} - {x['title']} ({x['category']}: ${x['amount']:.2f})": x['id'] 
            for x in data["expenses"]
        }
        selected_deletes = st.multiselect("Select expenses to remove", options=list(delete_options.keys()))
        if st.button("Delete Selected Expenses"):
            deleted_count = 0
            for key in selected_deletes:
                id_to_del = delete_options[key]
                if bm.delete_expense(data, id_to_del):
                    deleted_count += 1
            if deleted_count > 0:
                bm.save_data(data, DATA_FILE)
                st.success(f"Deleted {deleted_count} expense entries!")
                st.rerun()

with tab_inc:
    if not data["income"]:
        st.info("No income sources logged.")
    else:
        df_inc_full = pd.DataFrame(data["income"])
        df_inc_view = df_inc_full.copy()
        df_inc_view["amount"] = df_inc_view["amount"].apply(lambda x: f"${x:,.2f}")
        df_inc_view = df_inc_view.sort_values(by="date", ascending=False)
        
        st.dataframe(
            df_inc_view[["date", "source", "amount"]],
            use_container_width=True,
            column_config={
                "date": "Date Received",
                "source": "Income Source",
                "amount": "Earnings"
            }
        )
        
        # Row deletion UI
        st.write("---")
        st.markdown("### 🗑️ Delete Income Entry")
        delete_inc_options = {
            f"{x['date']} - {x['source']} (${x['amount']:.2f})": x['id'] 
            for x in data["income"]
        }
        selected_inc_deletes = st.multiselect("Select income entries to remove", options=list(delete_inc_options.keys()))
        if st.button("Delete Selected Income"):
            deleted_inc_count = 0
            for key in selected_inc_deletes:
                id_to_del = delete_inc_options[key]
                if bm.delete_income(data, id_to_del):
                    deleted_inc_count += 1
            if deleted_inc_count > 0:
                bm.save_data(data, DATA_FILE)
                st.success(f"Deleted {deleted_inc_count} income entries!")
                st.rerun()

with tab_budgets:
    st.write("### 🛡️ Category Budget Tracker")
    st.write("Monitor your category spending limits. Limits can be added via the sidebar 'Manage Goals' section.")
    
    budget_data_rows = []
    category_budgets = summary["category_budgets"]
    
    for category in bm.EXPENSE_CATEGORIES:
        limit = category_budgets.get(category, 0.0)
        spent = summary["expenses_by_category"].get(category, 0.0)
        remaining = limit - spent if limit > 0 else 0.0
        
        status = "No Limit Set"
        if limit > 0:
            status = "Within Limit" if spent <= limit else "🚨 Over Limit"
            
        budget_data_rows.append({
            "Category": category,
            "Monthly Limit": f"${limit:,.2f}" if limit > 0 else "N/A",
            "Amount Spent": f"${spent:,.2f}",
            "Remaining Budget": f"${remaining:,.2f}" if limit > 0 else "N/A",
            "Status": status
        })
        
    df_budget_table = pd.DataFrame(budget_data_rows)
    st.dataframe(df_budget_table, use_container_width=True)
