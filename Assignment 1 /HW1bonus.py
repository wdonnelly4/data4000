## Calling main
## Returning bool
def is_profitable(revenue, cost):
    return revenue > cost

## Match casing category and suggestion
def get_investment_suggestion(category):
    match category:
        case "high margin":
            return "Reinvest"
        case "medium margin":
            return "Expand Cautiously"
        case "low margin":
            return "Cut Costs"
        case _:
            return "Review Category"

## Main
def main():
    revenue = float(input("What's the business revenue? "))
    cost = float(input("What's the business cost? "))
    category = input("What's the category? ").strip().lower()

    if is_profitable(revenue, cost):
        profit = revenue - cost
        suggestion = get_investment_suggestion(category)
        print(f"Profit: ${profit:,.2f} | Suggested action: {suggestion}")
    else:
        print("Not profitable. No investment suggested.")

## Calling main
if __name__ == "__main__":
    main()
    