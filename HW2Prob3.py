## Getting credit score and annual income
credit_score = int(input("What's the credit score? "))
income = float(input("What's the annual income? "))

## Classify applicant
if credit_score >= 720 and income >= 60000:
    risk = "Low Risk"
elif credit_score >= 650 and income >= 40000:
    risk = "Medium Risk"
else:
    risk = "High Risk"

## Result
print(f"Loan Risk Category: {risk}")