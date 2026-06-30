import budget_manager as bm
import os
import tempfile

def run_tests():
    print("Running automated verification tests for budget_manager.py...")
    
    # Use a temporary file for testing
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        test_filepath = tmp.name
    
    try:
        # Test 1: Load nonexistent file
        data = bm.load_data(test_filepath)
        assert isinstance(data, dict), "Data should be a dictionary"
        assert "income" in data and len(data["income"]) == 0, "Initial income list should be empty"
        assert "expenses" in data and len(data["expenses"]) == 0, "Initial expenses list should be empty"
        assert data["savings_goal"] == 0.0, "Initial savings goal should be 0.0"
        print("[PASS] Test 1: Load non-existent file")
        
        # Test 2: Add Income
        bm.add_income(data, "Salary", 5000.0, "2026-06-01")
        bm.add_income(data, "Freelance", 800.0, "2026-06-15")
        summary = bm.get_financial_summary(data)
        assert summary["total_income"] == 5800.0, f"Expected total income 5800, got {summary['total_income']}"
        assert summary["total_expense"] == 0.0, "Total expense should be 0.0"
        assert summary["savings"] == 5800.0, "Net savings should match total income"
        assert summary["savings_rate"] == 100.0, "Savings rate should be 100%"
        print("[PASS] Test 2: Add income & check summary")

        # Test 3: Input validation checks using try-except
        try:
            bm.add_income(data, "Invalid", -100.0, "2026-06-01")
            assert False, "Should have failed with negative amount"
        except ValueError as e:
            assert "must be greater than zero" in str(e), f"Unexpected error message: {e}"
            
        try:
            bm.add_income(data, " ", 100.0, "2026-06-01")
            assert False, "Should have failed with empty source"
        except ValueError as e:
            assert "cannot be empty" in str(e), f"Unexpected error message: {e}"

        try:
            bm.add_income(data, "Job", 100.0, "2026-13-45")
            assert False, "Should have failed with invalid date"
        except ValueError as e:
            assert "Invalid date format" in str(e), f"Unexpected error message: {e}"
        print("[PASS] Test 3: Input validation check")

        # Test 4: Add Expense & category breakdown
        bm.add_expense(data, "Grocery shopping", 350.0, "Food", "2026-06-02")
        bm.add_expense(data, "Rent payment", 1200.0, "Housing/Rent", "2026-06-01")
        bm.add_expense(data, "Coffee", 15.0, "Food", "2026-06-03")
        summary = bm.get_financial_summary(data)
        assert summary["total_expense"] == 1565.0, f"Expected total expense 1565, got {summary['total_expense']}"
        assert summary["savings"] == 4235.0, f"Expected savings 4235, got {summary['savings']}"
        
        # Check active category sums
        categories = summary["expenses_by_category"]
        assert categories["Food"] == 365.0, f"Expected Food sum 365, got {categories.get('Food')}"
        assert categories["Housing/Rent"] == 1200.0, f"Expected Rent sum 1200, got {categories.get('Housing/Rent')}"
        print("[PASS] Test 4: Add expense & verify categories")

        # Test 5: Savings Goal & Category limits
        bm.update_savings_goal(data, 2000.0)
        bm.update_category_budget(data, "Food", 300.0)
        summary = bm.get_financial_summary(data)
        assert summary["savings_goal"] == 2000.0, "Savings goal should be updated"
        assert summary["category_budgets"]["Food"] == 300.0, "Food budget limit should be updated"
        
        # Verify limit alerts checking
        food_limit = summary["category_budgets"]["Food"]
        food_spent = summary["expenses_by_category"]["Food"]
        assert food_spent > food_limit, "Food spending should exceed the limit"
        print("[PASS] Test 5: Goal updates & alerts logic")

        # Test 6: Deletion
        # Get IDs
        exp_id_to_delete = data["expenses"][-1]["id"]  # Coffee
        bm.delete_expense(data, exp_id_to_delete)
        new_summary = bm.get_financial_summary(data)
        assert new_summary["total_expense"] == 1550.0, f"Expected total expense 1550 after delete, got {new_summary['total_expense']}"
        assert "Coffee" not in [x["title"] for x in data["expenses"]], "Coffee entry should be deleted"
        print("[PASS] Test 6: Entry deletion")

        # Test 7: Persistence
        bm.save_data(data, test_filepath)
        loaded_data = bm.load_data(test_filepath)
        assert loaded_data["savings_goal"] == 2000.0, "Saved savings goal did not match on load"
        assert len(loaded_data["income"]) == 2, "Saved income length mismatch"
        assert len(loaded_data["expenses"]) == 2, "Saved expenses length mismatch"
        print("[PASS] Test 7: JSON Persistence (Save & Load)")

        print("\nAll automated verification tests PASSED successfully!")
    finally:
        # Cleanup
        if os.path.exists(test_filepath):
            os.remove(test_filepath)

if __name__ == "__main__":
    run_tests()
