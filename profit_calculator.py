print("=== MONEY PC OPPORTUNITY CALCULATOR ===")
print()

try:
    sale_price = float(input("Expected selling price: $"))
    purchase_price = float(input("Purchase price: $"))
    parts_cost = float(input("Estimated repair/parts: $"))
    shipping_cost = float(input("Estimated shipping: $"))
    selling_fee_percent = float(input("Selling fee percentage: %"))
    risk_reserve = float(input("Repair risk reserve: $"))
    minimum_profit = float(input("Minimum profit wanted: $"))

    selling_fee = sale_price * (selling_fee_percent / 100)

    total_cost = (
        purchase_price
        + parts_cost
        + shipping_cost
        + selling_fee
        + risk_reserve
    )

    profit_after_risk = sale_price - total_cost

    maximum_purchase_price = (
        sale_price
        - parts_cost
        - shipping_cost
        - selling_fee
        - risk_reserve
        - minimum_profit
    )

    print()
    print("=== RESULT ===")

    print(f"Expected sale:           ${sale_price:,.2f}")
    print(f"Purchase price:          ${purchase_price:,.2f}")
    print(f"Estimated repair:        ${parts_cost:,.2f}")
    print(f"Shipping:                ${shipping_cost:,.2f}")
    print(f"Selling fees:            ${selling_fee:,.2f}")
    print(f"Repair risk reserve:     ${risk_reserve:,.2f}")

    print("--------------------------------")

    print(f"Profit after risk:       ${profit_after_risk:,.2f}")
    print(f"Minimum profit wanted:   ${minimum_profit:,.2f}")
    print(f"MAXIMUM PURCHASE PRICE:  ${maximum_purchase_price:,.2f}")

    print()

    if profit_after_risk >= minimum_profit:
        print("🟢 POTENTIAL OPPORTUNITY")
        print("Investigate the fault before buying.")

    elif profit_after_risk >= 0:
        print("🟡 POSSIBLE PROFIT — NOT ENOUGH MARGIN")
        print("PASS unless there is a very good reason.")

    else:
        print("🔴 PASS — EXPECTED LOSS")

except ValueError:
    print("Please enter numbers only.")