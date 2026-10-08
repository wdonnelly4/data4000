## Purchase amount and membership status
amount = float(input("What's the purchase amount? "))
status = input("Are you a member? (yes/no) ").strip().lower()

## Ensuring Membership answer is valid
if status != "yes" and status != "no":
    print("Invalid membership status. Please enter yes or no.")
else:
    ## Determine the discount percentage
    if status == "yes":
        #Member rules
        if amount >= 100:
            discount = 15
        else:
            discount = 5
    else:
        #Non-member rules
        if amount >= 150:
            discount = 10
        else:
            discount = 0

    ##Calculate the final price after the discount
    final_price = amount * (1 - discount / 100)

    ##Results
    print(f"Discount applied: {discount}%")
    print(f"Final price: ${final_price:,.2f}")