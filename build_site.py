import csv
import html
from pathlib import Path

DEALS_FILE = "deals.csv"
OUTPUT_FILE = "index.html"


def load_deals():
    deals = []

    with open(DEALS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            deals.append(row)

    return deals


def money(value):
    return f"${float(value):,.2f}"


def build_deal_card(deal):
    title = html.escape(deal["title"])
    url = html.escape(deal["affiliate_url"], quote=True)

    price = float(deal["price"])
    normal_value = float(deal["normal_value"])

    savings = normal_value - price

    if normal_value > 0:
        savings_percent = (savings / normal_value) * 100
    else:
        savings_percent = 0

    return f"""
    <div class="deal">
        <div class="badge">DEAL</div>

        <h2>{title}</h2>

        <div class="price">
            {money(price)}
        </div>

        <p>
            Typical value:
            <strong>{money(normal_value)}</strong>
        </p>

        <p>
            Estimated savings:
            <strong>{money(savings)} ({savings_percent:.0f}%)</strong>
        </p>

        <a
            class="button"
            href="{url}"
            target="_blank"
            rel="nofollow sponsored"
        >
            View Deal on eBay
        </a>
    </div>
    """


def build_site(deals):
    cards = ""

    for deal in deals:
        cards += build_deal_card(deal)

    return f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Money PC Deals</title>

    <style>

        body {{
            font-family: Arial, sans-serif;
            background: #f4f5f7;
            color: #222;
            margin: 0;
        }}

        header {{
            background: #111827;
            color: white;
            padding: 40px 20px;
            text-align: center;
        }}

        header h1 {{
            margin: 0;
            font-size: 38px;
        }}

        header p {{
            color: #d1d5db;
        }}

        main {{
            max-width: 900px;
            margin: 30px auto;
            padding: 0 20px;
        }}

        .deal {{
            position: relative;
            background: white;
            padding: 25px;
            margin-bottom: 20px;
            border-radius: 12px;
            box-shadow: 0 3px 12px rgba(0,0,0,.08);
        }}

        .deal h2 {{
            margin-top: 5px;
        }}

        .badge {{
            display: inline-block;
            background: #e8e8e8;
            padding: 5px 9px;
            border-radius: 5px;
            font-size: 12px;
            font-weight: bold;
        }}

        .price {{
            font-size: 30px;
            font-weight: bold;
            margin: 15px 0;
        }}

        .button {{
            display: inline-block;
            margin-top: 10px;
            padding: 12px 18px;
            background: #111827;
            color: white;
            text-decoration: none;
            border-radius: 7px;
            font-weight: bold;
        }}

        footer {{
            max-width: 900px;
            margin: 50px auto;
            padding: 20px;
            color: #666;
            font-size: 13px;
        }}

    </style>
</head>

<body>

<header>

    <h1>Money PC Deals</h1>

    <p>
        Automated deal discovery for gaming hardware,
        electronics and other online bargains.
    </p>

</header>

<main>

    <h2>Latest Deals</h2>

    {cards}

</main>

<footer>

    <p>
        Prices, availability and item condition can change.
        Verify all information on the seller's listing
        before purchasing.
    </p>

    <p>
        As an eBay Partner, I may earn from qualifying purchases.
    </p>

</footer>

</body>
</html>
"""


deals = load_deals()

website = build_site(deals)

Path(OUTPUT_FILE).write_text(
    website,
    encoding="utf-8"
)

print()
print("================================")
print(" MONEY PC WEBSITE BUILDER")
print("================================")
print()
print(f"Deals loaded: {len(deals)}")
print(f"Created: {OUTPUT_FILE}")
print()
print("Website successfully generated.")