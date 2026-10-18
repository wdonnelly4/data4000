## Input
name = input("What's the product name? ").strip().lower()

## Match/case
match name:
    case "electronics" | "gadget":
        category = "High Margin"
    case "clothing" | "apparel":
        category = "Medium Margin"
    case "food" | "grocery":
        category = "Low Margin"
    case _:
        category = "Uncategorized - Review Needed"

## Tech case
match name:
    case "electronics" | "gadget":
        category = "High Margin"
    case _ if name.startswith("tech"):
        category = "High Margin"
    case "clothing" | "apparel":
        category = "Medium Margin"
    case "food" | "grocery":
        category = "Low Margin"
    case _:
        category = "Uncategorized - Review Needed"

## Result
print(f"Product: {name} | Category: {category}")

