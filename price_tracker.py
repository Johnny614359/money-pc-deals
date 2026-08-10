import csv
import os
from datetime import datetime

DATA_FILE = "price_history.csv"


def record_price(item, price):
    file_exists = os.path.exists(DATA_FILE)

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["date", "item", "price"])

        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            item,
            price
        ])

    print(f"Recorded: {item} = ${price:.2f}")


print("=== MONEY PC PRICE TRACKER ===")
print("This is our first price database.")
print()

while True:
    item = input("Item name (or 'quit'): ").strip()

    if item.lower() == "quit":
        break

    try:
        price = float(input("Price: $"))
    except ValueError:
        print("Please enter a number.")
        continue

    record_price(item, price)

print()
print("Price tracker stopped.")