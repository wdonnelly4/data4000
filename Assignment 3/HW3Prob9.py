## Business Growth Projection
revenue = float(input("Initial revenue: "))
growth_percent = float(input("Annual growth rate (%): "))

growth_rate = growth_percent / 100

print()
print(f"{'Year':<6}{'Revenue':>16}")
print("-" * 22)
print(f"{0:<6}{revenue:>16,.2f}")

for year in range(1, 11):
    revenue = revenue * (1 + growth_rate)
    print(f"{year:<6}{revenue:>16,.2f}")