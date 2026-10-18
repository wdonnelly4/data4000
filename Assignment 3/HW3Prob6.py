## Bank Loan Repayment Simulator
def months_to_payoff(balance, annual_rate, payment):
    monthly_rate = annual_rate / 100 / 12
    months = 0

    while balance > 0:
        interest = balance * monthly_rate
        balance = balance + interest - payment
        months += 1

    return months


loan = float(input("Loan amount: "))
rate = float(input("Annual interest rate (%): "))
payment = float(input("Monthly payment: "))

## Payment must beat the first month's interest
first_month_interest = loan * (rate / 100 / 12)

if loan <= 0 or payment <= 0:
    print("Loan amount and payment must be positive.")
elif payment <= first_month_interest:
    print("Payment is too small to ever pay off this loan.")
else:
    months = months_to_payoff(loan, rate, payment)
    years = months // 12
    leftover_months = months % 12
    print(f"It takes {months} months ({years} years, {leftover_months} months) to pay off the loan.")