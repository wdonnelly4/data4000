## Getting credit score as integer
score = int(input("What's your credit score? "))

## Validating range
if score < 300 or score > 850:
    print("Invalid score.")

## Categorizing with elif
elif score >= 750:
    category = "Excellent - Loan Approved"
    approved = True
elif 700 <= score < 750:
    category = "Good - Loan Approved with Review"
    approved = True
elif 600 <= score < 700:
    category = "Fair - Loan Conditional"
    approved = False
else:
    category = "Poor - Loan Denied"
    approved = False

## Approval message
message = "Interest rate: Low" if approved else "Seek credit improvement."

## Print, combination
print(f"{category}. {message}")
