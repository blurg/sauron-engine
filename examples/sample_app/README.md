# Order Processing Sample App

A FastAPI application demonstrating Sauron Engine integration with external rules and job modules.

## Features

- FastAPI REST endpoints for order processing
- External rule definitions (YAML)
- Multi-file job module organization
- Session-based state sharing between conditions and actions

## Quick Start

```bash
# Install dependencies
poetry install

# Run the server
poetry run uvicorn examples.sample_app.main:app --reload
```

## API Endpoints

### POST /orders/process

Process an order through the rule engine.

```bash
curl -X POST "http://localhost:8000/orders/process" \
  -H "Content-Type: application/json" \
  -d '{
    "order_id": "ORD-001",
    "customer_id": "CUST-123",
    "items": [
      {"product_id": "PROD-A", "quantity": 2, "unit_price": 50.0}
    ],
    "total_amount": 100.0,
    "payment_method": "credit_card",
    "priority": "express"
  }'
```

**Rules applied:**
- Order must have at least one item
- Total amount must be at least $10.00
- Priority must be "normal" or "express"

**Actions executed:**
- 10% discount if total >= $100
- Shipping: $5 (normal) or $15 (express)

### GET /orders/rules

Returns available conditions and actions with their schemas.

```bash
curl "http://localhost:8000/orders/rules"
```

### GET /health

Health check endpoint.

```bash
curl "http://localhost:8000/health"
```
