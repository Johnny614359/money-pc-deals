import csv

EXPECTED_SALE_PRICE = 390.00
BROKEN_RESALE_VALUE = 210.00
SELLING_FEE_PERCENT = 10.0
OUTBOUND_SHIPPING = 25.00
MINIMUM_EXPECTED_PROFIT = 75.00

REPAIR_RULES_FILE = "repair_rules.csv"


def load_repair_rules():
    rules = {}

    with open(REPAIR_RULES_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rules[row["fault"]] = {
                "repair_cost": float(row["repair_cost"]),
                "risk_reserve": float(row["risk_reserve"]),
                "risk_level": row["risk_level"],
                "reject": row["reject"].strip().lower() == "true",
                "success_probability": float(row["success_probability"])
            }

    return rules


def check_model(title):
    title_lower = title.lower()

    wrong_models = [
        "xbox one x",
        "xbox one s",
        "xbox series s",
        "xbox 360",
        "xbox one"
    ]

    for model in wrong_models:
        if model in title_lower:
            return False

    return "series x" in title_lower


def classify_fault(text):
    text = text.lower()

    if any(term in text for term in [
        "liquid damage",
        "water damage",
        "corrosion",
        "missing motherboard",
        "motherboard missing",
        "board removed",
        "parts missing",
        "stripped for parts"
    ]):
        return "Major damage / missing parts"

    if any(term in text for term in [
        "hdmi",
        "no display",
        "no video",
        "black screen"
    ]):
        return "HDMI / display"

    if any(term in text for term in [
        "no power",
        "doesn't turn on",
        "does not turn on",
        "won't turn on",
        "wont turn on",
        "dead"
    ]):
        return "No power"

    if any(term in text for term in [
        "disc drive",
        "disk drive",
        "won't read disc",
        "doesn't read disc",
        "not reading discs"
    ]):
        return "Disc drive"

    if any(term in text for term in [
        "overheat",
        "overheating",
        "shuts off",
        "turns off"
    ]):
        return "Cooling / shutdown"

    if any(term in text for term in [
        "untested",
        "unknown issue",
        "unknown problem",
        "don't know what's wrong",
        "do not know what's wrong"
    ]):
        return "Unknown / untested"

    return "Unclassified"


def calculate(
    item_price,
    inbound_shipping,
    repair_cost,
    success_probability
):
    delivered_cost = item_price + inbound_shipping

    working_fee = (
        EXPECTED_SALE_PRICE
        * SELLING_FEE_PERCENT / 100
    )

    broken_fee = (
        BROKEN_RESALE_VALUE
        * SELLING_FEE_PERCENT / 100
    )

    success_profit = (
        EXPECTED_SALE_PRICE
        - delivered_cost
        - repair_cost
        - OUTBOUND_SHIPPING
        - working_fee
    )

    failure_profit = (
        BROKEN_RESALE_VALUE
        - delivered_cost
        - repair_cost
        - OUTBOUND_SHIPPING
        - broken_fee
    )

    failure_probability = 1 - success_probability

    expected_profit = (
        success_probability * success_profit
        + failure_probability * failure_profit
    )

    return (
        delivered_cost,
        success_profit,
        failure_profit,
        expected_profit
    )


repair_rules = load_repair_rules()

print()
print("====================================")
print("       MONEY PC SCANNER v6")
print("       Expected Value Mode")
print("====================================")
print()

while True:

    title = input("Listing title (or 'quit'): ").strip()

    if title.lower() == "quit":
        break

    if not check_model(title):
        print()
        print("🔴 REJECTED — WRONG OR UNCERTAIN MODEL")
        print()
        continue

    description = input(
        "Seller's fault description: "
    ).strip()

    try:
        item_price = float(input("Item price: $"))
        shipping = float(input("Shipping TO YOU: $"))

    except ValueError:
        print()
        print("Invalid price.")
        print()
        continue

    fault_name = classify_fault(
        title + " " + description
    )

    fault_rule = repair_rules.get(
        fault_name,
        repair_rules["Unclassified"]
    )

    print()
    print("--------- FAULT ANALYSIS ---------")
    print(f"Detected fault:      {fault_name}")
    print(f"Risk level:          {fault_rule['risk_level']}")
    print(f"Repair budget:       ${fault_rule['repair_cost']:.2f}")
    print(
        f"Success probability: "
        f"{fault_rule['success_probability']:.0%}"
    )

    if fault_rule["reject"]:
        print()
        print("🔴 AUTOMATIC REJECT")
        print()
        continue

    (
        delivered_cost,
        success_profit,
        failure_profit,
        expected_profit
    ) = calculate(
        item_price,
        shipping,
        fault_rule["repair_cost"],
        fault_rule["success_probability"]
    )

    print()
    print("--------- MONEY ANALYSIS ---------")
    print(f"Delivered cost:         ${delivered_cost:.2f}")
    print()
    print("SUCCESS CASE")
    print(f"Estimated profit:       ${success_profit:.2f}")
    print()
    print("FAILURE CASE")
    print(f"Estimated result:       ${failure_profit:.2f}")
    print()
    print("----------------------------------")
    print(f"EXPECTED PROFIT:        ${expected_profit:.2f}")
    print("----------------------------------")
    print()

    if expected_profit >= MINIMUM_EXPECTED_PROFIT:
        print("🚨 EXPECTED-VALUE OPPORTUNITY")

        if failure_profit >= 0:
            print("🛡️ Failure case currently remains profitable.")
        else:
            print(
                f"⚠️ Failed repair could lose "
                f"${abs(failure_profit):.2f}"
            )

    elif expected_profit >= 0:
        print("🟡 POSITIVE EXPECTED VALUE — TOO LOW FOR NOW")

    else:
        print("🔴 NEGATIVE EXPECTED VALUE — PASS")

    print()
    print("NOTE: Repair probabilities are placeholders.")
    print("Do not buy based on these numbers yet.")
    print()
    print("==================================")
    print()

print()
print("Money PC stopped.")