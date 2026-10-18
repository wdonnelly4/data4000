## Sample survey data
preferences = ["coffee", "tea", "coffee", "soda"]

## Empty dictionary for counts
counts = {}

## Count each choice
for choice in preferences:
    if choice in counts:
        counts[choice] += 1
    else:
        counts[choice] = 1

## Results
total = len(preferences)
for product in counts:
    percent = counts[product] / total * 100
    print(f"{product}: {percent:.0f}%")