import csv
import statistics
import os

DATA_FILE = "price_history.csv"

# How far below the normal price before we flag something
DEAL_THRESHOLD = 0.20


if not os.path.exists(DATA_FILE):
    print("No price history found.")
    exit()


prices = {}

with open(DATA_FILE, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        item = row["item"].strip()
        price = float(row["price"])

        if item not in prices:
            prices[item] = []

        prices[item].append(price)


print("=== MONEY PC DEAL DETECTOR ===")
print()

for item, values in prices.items():

    if len(values) < 2:
        print(f"{item}: Not enough data yet.")
        continue

    typical_price = statistics.median(values)

    print(f"Item: {item}")
    print(f"Typical price: ${typical_price:.2f}")

    for price in values:
        discount = (typical_price - price) / typical_price

        if discount >= DEAL_THRESHOLD:
            print(
                f"🚨 POSSIBLE DEAL: ${price:.2f} "
                f"({discount:.1%} below typical)"
            )

    print()