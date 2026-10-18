## Customer Loyalty Tiers
customers = {
    "Alice": 450,
    "Bob": 1200,
    "Carol": 5200,
    "Dan": 999.99,
    "Eve": 3000,
    "Frank": 8000
}

tier_counts = {"Bronze": 0, "Silver": 0, "Gold": 0}

for name, total_spent in customers.items():
    if total_spent < 1000:
        tier = "Bronze"
    elif total_spent < 5000:
        tier = "Silver"
    else:
        tier = "Gold"

    tier_counts[tier] += 1

print("LOYALTY TIER SUMMARY")
for tier, count in tier_counts.items():
    print(f"{tier}: {count} customers")