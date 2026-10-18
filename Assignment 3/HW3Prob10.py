## Startup Pitch Deck Visualizer
## Projected revenue by year in millions
revenue_by_year = {1: 3, 2: 5, 3: 8, 4: 12, 5: 15}

print("Projected Revenue (each # = $1M)")
print()

## Version A using string multiplication
for year, value in revenue_by_year.items():
    print(f"Year {year}: {'#' * value}")

print()
print("Same chart built with nested loops:")
print()

## Version B nested loops
for year, value in revenue_by_year.items():
    bar = ""
    for i in range(value):
        bar += "#"
    print(f"Year {year}: {bar} (${value}M)")