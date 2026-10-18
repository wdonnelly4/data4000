## Stock Portfolio Tracker
import random


def total_value(portfolio):
    total = 0
    for ticker, info in portfolio.items():
        total += info["shares"] * info["price"]
    return total


portfolio = {
    "AAPL": {"shares": 10, "price": 170},
    "TSLA": {"shares": 4, "price": 250},
    "AMZN": {"shares": 2, "price": 130}
}

## Results
print(f"Starting value: ${total_value(portfolio):,.2f}")

## Bonus
for day in range(1, 8):
    for ticker, info in portfolio.items():
        change = random.uniform(-0.05, 0.05)
        info["price"] = info["price"] * (1 + change)
    print(f"Day {day}: ${total_value(portfolio):,.2f}")