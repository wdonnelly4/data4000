## Retail Checkout Simulation
prices = []  

## Priming read
price = float(input("Enter the price of an item (0 to finish): "))

## Loop until user enters 0
while price != 0:
    if price < 0:
        print("Price can't be negative. Try again.")
    else:
        prices.append(price)
    price = float(input("Enter the price of an item (0 to finish): "))

## Results
if len(prices) == 0:
    print("No items were purchased.")
else:
    total = sum(prices)
    count = len(prices)
    average = total / count

    print(f"Number of items bought: {count}")
    print(f"Total purchase amount: ${total:,.2f}")
    print(f"Average item cost: ${average:,.2f}")