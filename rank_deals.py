import csv

INPUT_FILE = "candidates.csv"
OUTPUT_FILE = "deals.csv"

MINIMUM_SAVINGS_DOLLARS = 40
MINIMUM_SAVINGS_PERCENT = 15
MAX_DEALS = 20


def load_candidates():
    listings = []

    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                price = float(row["price"])
                shipping = float(row["shipping"])
                normal_value = float(row["normal_value"])

                delivered_price = price + shipping

                savings = normal_value - delivered_price

                if normal_value > 0:
                    savings_percent = (
                        savings / normal_value
                    ) * 100
                else:
                    savings_percent = 0

                listings.append({
                    "title": row["title"],
                    "price": delivered_price,
                    "normal_value": normal_value,
                    "affiliate_url": row["url"],
                    "savings": savings,
                    "savings_percent": savings_percent
                })

            except (ValueError, KeyError):
                continue

    return listings


def qualifies(listing):
    if listing["savings"] < MINIMUM_SAVINGS_DOLLARS:
        return False

    if listing["savings_percent"] < MINIMUM_SAVINGS_PERCENT:
        return False

    return True


def calculate_score(listing):
    dollar_score = listing["savings"]
    percentage_score = listing["savings_percent"] * 2

    return dollar_score + percentage_score


def rank_deals(listings):
    good_deals = []

    for listing in listings:
        if qualifies(listing):
            listing["score"] = calculate_score(listing)
            good_deals.append(listing)

    good_deals.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return good_deals[:MAX_DEALS]


def save_deals(deals):
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
            "normal_value",
            "affiliate_url"
        ])

        for deal in deals:
            writer.writerow([
                deal["title"],
                f"{deal['price']:.2f}",
                f"{deal['normal_value']:.2f}",
                deal["affiliate_url"]
            ])


candidates = load_candidates()
deals = rank_deals(candidates)
save_deals(deals)

print()
print("================================")
print(" MONEY PC DEAL RANKER")
print("================================")
print()

print(f"Listings scanned: {len(candidates)}")
print(f"Deals accepted:   {len(deals)}")
print()

for number, deal in enumerate(deals, start=1):

    print(
        f"{number}. {deal['title']}"
    )

    print(
        f"   Delivered: ${deal['price']:.2f}"
    )

    print(
        f"   Normal:    ${deal['normal_value']:.2f}"
    )

    print(
        f"   Savings:   ${deal['savings']:.2f} "
        f"({deal['savings_percent']:.1f}%)"
    )

    print(
        f"   Score:     {deal['score']:.1f}"
    )

    print()

print("deals.csv updated.")