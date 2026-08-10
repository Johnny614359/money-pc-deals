import csv
import statistics
import os

DATA_FILE = "price_history.csv"

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

print("=== MONEY PC PRICE ANALYZER ===")
print()

for item, values in prices.items():
    average = statistics.mean(values)
    lowest = min(values)
    highest = max(values)
    median = statistics.median(values)

    print(f"Item: {item}")
    print(f"Prices recorded: {len(values)}")
    print(f"Average: ${average:.2f}")
    print(f"Median:  ${median:.2f}")
    print(f"Lowest:  ${lowest:.2f}")
    print(f"Highest: ${highest:.2f}")
    print()