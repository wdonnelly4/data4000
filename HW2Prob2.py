##Get the salary and performance score
salary = float(input("What's the annual salary? "))
score = int(input("What's the performance score (0-100)? "))

## Ensuring the score is in the valid range
if score < 0 or score > 100:
    print("Invalid score. Please enter a number from 0 to 100.")
else:
    ## Bonus percentage
    if score >= 90:
        bonus_percent = 20
    elif score >= 80:
        bonus_percent = 10
    elif score >= 70:
        bonus_percent = 5
    else:
        bonus_percent = 0

    ## Calculate the bonus
    bonus_amount = salary * bonus_percent / 100

    ## Results
    print(f"Performance Bonus: {bonus_percent}%")
    print(f"Bonus Amount: ${bonus_amount:,.2f}")