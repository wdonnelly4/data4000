## Get number
def get_tax_rate(income):
    if income < 50000:
        return 0.10
    elif income < 100000:
        return 0.20
    else:
        return 0.30

## Bracket function
def get_tax_bracket(income):
    if income < 0:
        return "Invalid income."
    elif income < 50000:
        bracket = "Low (10%)"
    elif income < 100000:
        bracket = "Medium (20%)"
    else:
        bracket = "High (30%)"

    return bracket + " (Deduction Eligible)" if income % 2 == 0 else bracket

## Modulo use
# return bracket + " (Deduction Eligible)" if income % 2 == 0 else bracket

## Main
income = float(input("What's your annual income? "))
bracket = get_tax_bracket(income)

if bracket == "Invalid income.":
    print(bracket)
else:
    rate = get_tax_rate(income)
    tax = income * rate
    print(f"Your bracket: {bracket}. Estimated tax: {tax}")