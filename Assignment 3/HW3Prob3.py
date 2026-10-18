## Expense Summary Report
expenses = {
    "Travel": [500, 200],
    "Meals": [40, 60, 30],
    "Supplies": [100]
}

grand_total = 0  

print("EXPENSE SUMMARY REPORT")
print("-" * 21)

## Outer loop over categories
for category, amounts in expenses.items():
    category_total = 0  
    ## Inner loop over this category's amounts
    for amount in amounts:
        category_total += amount

    grand_total += category_total
    print(f"{category:<10} ${category_total:>9,.2f}")

## Results
print("-" * 21)
print(f"{'TOTAL':<10} ${grand_total:>9,.2f}")