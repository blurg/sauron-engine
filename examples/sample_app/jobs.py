from decimal import Decimal

from sauron.rule_engine import RuleEngine

engine = RuleEngine()


@engine.condition("Has Items")
def has_items(session) -> bool:
    order = session.get("order", {})
    items = order.get("items", [])
    return len(items) > 0


@engine.condition("Amount Sufficient")
def amount_sufficient(session, min_amount: float = 10.0) -> bool:
    order = session.get("order", {})
    # order["total_amount"] is Decimal because of Pydantic model
    total = order.get("total_amount", Decimal("0.0"))
    # min_amount comes as float from YAML, convert to Decimal safely
    return total >= Decimal(str(min_amount))


@engine.condition("Priority Valid")
def priority_valid(session) -> bool:
    order = session.get("order", {})
    priority = order.get("priority", "normal")
    return priority in ["normal", "express"]


@engine.action("Calculate Discount")
def calculate_discount(
    session, threshold: float = 100.0, rate: float = 0.1
) -> None:
    order = session.get("order", {})
    total = order.get("total_amount", Decimal("0.0"))

    threshold_dec = Decimal(str(threshold))
    rate_dec = Decimal(str(rate))

    discount = total * rate_dec if total >= threshold_dec else Decimal("0.0")
    session["discount"] = round(discount, 2)
    session["final_amount"] = round(total - discount, 2)


@engine.action("Calculate Shipping")
def calculate_shipping(session) -> None:
    order = session.get("order", {})
    priority = order.get("priority", "normal")
    shipping = Decimal("15.0") if priority == "express" else Decimal("5.0")
    session["shipping"] = shipping

    current_final = session.get("final_amount", Decimal("0.0"))
    session["final_amount"] = round(current_final + shipping, 2)


@engine.action("Finalize Order")
def finalize_order(session) -> None:
    session["approved"] = True


def create_engine() -> RuleEngine:
    return engine
