## Step 1
## Wrap input in float for floating point numbers
## Prompt user for revenue and cost
revenue = float(input("What's the revenue? "))
cost = float(input("What's the cost? "))

## Step 2
## Calculate profit
profit = revenue - cost

##Step 3
## Defensive programming, if/else
## Check for valid revenue
if revenue > 0:
    margin = (profit / revenue) * 100
    print(f"Profit: ${profit:,.2f} | Margin: {margin:.2f}%")
else:
    print("Invalid revenue.") 

##Step 4
## f-string formatting
## Calculating Proft | Margin
f"Profit: ${profit:,.2f} | Margin: {margin:.2f}%"