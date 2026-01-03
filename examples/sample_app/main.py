from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, Union

from fastapi import FastAPI
from ruamel.yaml import YAML

from .jobs import create_engine
from .schemas import Order, OrderResponse, OrderStatus

app = FastAPI(title="Sauron Order Processing Service")


@app.post("/orders/process", response_model=OrderResponse)
def process_order(order: Order) -> OrderResponse:
    engine = create_engine()

    rule_path = Path(__file__).parent / "rules.yaml"
    rule = YAML().load(rule_path)

    session: Dict[str, Any] = {
        "order": order.model_dump(),
        "results": [],
        "discount": Decimal("0.0"),
        "shipping": Decimal("0.0"),
        "final_amount": order.total_amount,
        "approved": False,
    }

    engine.run(rule, session=session)

    if not session.get("approved"):
        return OrderResponse(
            order_id=order.order_id,
            status=OrderStatus.REJECTED,
            processed_amount=order.total_amount,
            applied_discount=session.get("discount", Decimal("0.0")),
            shipping_cost=session.get("shipping", Decimal("0.0")),
            final_amount=order.total_amount,
            results=session.get("results", []),
        )

    return OrderResponse(
        order_id=order.order_id,
        status=OrderStatus.APPROVED,
        processed_amount=order.total_amount,
        applied_discount=session.get("discount", Decimal("0.0")),
        shipping_cost=session.get("shipping", Decimal("0.0")),
        final_amount=session.get("final_amount", order.total_amount),
        results=session.get("results", []),
    )


@app.get("/orders/rules")
def get_available_rules() -> Union[str, Dict[str, Any]]:
    engine = create_engine()
    return engine.export_metadata()


@app.get("/health")
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}


def create_app() -> FastAPI:
    return app
