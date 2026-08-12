import csv
from pathlib import Path

INPUT_FILE = "product_feed.csv"
OUTPUT_FILE = "candidates.csv"

# Simple category keywords we care about for now.
TARGET_KEYWORDS = [
    "xbox",
    "playstation",
    "ps5",
    "nintendo",
    "switch",
    "gaming",
    "graphics card",
    "gpu",
    "laptop",
    "ssd",
    "monitor"
]

MIN_PRICE = 25.00
MAX_PRICE = 1500.00


def text_matches(title):
    title_lower = title.lower()

    return any(
        keyword in title_lower
        for keyword in TARGET_KEYWORDS
    )


def load_products():
    products = []

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:
            try:
                title = row["title"].strip()
                price = float(row["price"])
                normal_value = float(row["normal_value"])
                shipping = float(row.get("shipping", 0) or 0)
                url = row["url"].strip()

            except (
                KeyError,
                ValueError,
                AttributeError
            ):
                continue

            if not text_matches(title):
                continue

            if price < MIN_PRICE or price > MAX_PRICE:
                continue

            if normal_value <= 0:
                continue

            products.append({
                "title": title,
                "price": price,
                "shipping": shipping,
                "normal_value": normal_value,
                "url": url
            })

    return products


def save_candidates(products):

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "title",
            "price",
            "shipping",
            "normal_value",
            "url"
        ])

        for product in products:

            writer.writerow([
                product["title"],
                f"{product['price']:.2f}",
                f"{product['shipping']:.2f}",
                f"{product['normal_value']:.2f}",
                product["url"]
            ])


print()
print("================================")
print(" MONEY PC PRODUCT IMPORTER")
print("================================")
print()

if not Path(INPUT_FILE).exists():
    print(f"Missing file: {INPUT_FILE}")
    print()
    print("Create product_feed.csv first.")
    raise SystemExit(1)

products = load_products()

save_candidates(products)

print(f"Products imported: {len(products)}")
print(f"Created: {OUTPUT_FILE}")
print()
print("Product import complete.")