# Batch Jobs Quickstart

Batch jobs allow you to import multiple conditions and actions from a module at once, keeping your code organized and reusable.

## What are Batch Jobs?

Batch jobs are a way to organize your conditions and actions into separate modules and import them into your engine in bulk. This is especially useful for:
- Keeping your main code clean and focused
- Reusing job definitions across multiple engines
- Organizing jobs by domain or functionality
- Managing large numbers of jobs

## Quick Example

### Step 1: Create a jobs module

Create a Python module (e.g., `my_jobs.py`) and define your conditions and actions:

```python
# my_jobs.py
from decimal import Decimal


def has_items(session) -> bool:
    """Check if order has items"""
    order = session.get("order", {})
    items = order.get("items", [])
    return len(items) > 0


def amount_sufficient(session, min_amount: float = 10.0) -> bool:
    """Check if order amount meets minimum"""
    order = session.get("order", {})
    total = order.get("total_amount", Decimal("0.0"))
    return total >= Decimal(str(min_amount))


def calculate_discount(
    session, threshold: float = 100.0, rate: float = 0.1
) -> None:
    """Calculate discount based on threshold"""
    order = session.get("order", {})
    total = order.get("total_amount", Decimal("0.0"))

    threshold_dec = Decimal(str(threshold))
    rate_dec = Decimal(str(rate))

    discount = total * rate_dec if total >= threshold_dec else Decimal("0.0")
    session["discount"] = round(discount, 2)
    session["final_amount"] = round(total - discount, 2)
```

### Step 2: Import jobs into your engine

```python
# main.py
from sauron.rule_engine import RuleEngine
import my_jobs

engine = RuleEngine()

# Import all jobs from the module
engine.import_jobs(my_jobs)

# All jobs are now available
print(engine.callables_collected.keys())
# Output: dict_keys(['has_items', 'amount_sufficient', 'calculate_discount'])
```

### Step 3: Use the imported jobs

```python
rule = {
    "conditions": [
        {
            "name": "has_items",
            "args": {},
        }
    ],
    "actions": [
        {
            "name": "calculate_discount",
            "args": {"threshold": 100.0, "rate": 0.1},
        }
    ],
}

session = {
    "order": {
        "items": [{"product_id": "PROD-A", "quantity": 2}],
        "total_amount": Decimal("150.00"),
    }
}

engine.run(rule, session=session)

print(session["discount"])
print(session["final_amount"])
```

## Advanced Usage

### Using `jobs_list` for Explicit Control

For more control over job names, types, and metadata, define a `jobs_list` in your module:

```python
# order_jobs.py
from decimal import Decimal
from typing import Any, List, Tuple


def has_items(session) -> bool:
    """Check if order has items"""
    order = session.get("order", {})
    items = order.get("items", [])
    return len(items) > 0


def amount_sufficient(session, min_amount: float = 10.0) -> bool:
    """Check if order amount meets minimum"""
    order = session.get("order", {})
    total = order.get("total_amount", Decimal("0.0"))
    return total >= Decimal(str(min_amount))


def calculate_discount(
    session, threshold: float = 100.0, rate: float = 0.1
) -> None:
    """Calculate discount based on threshold"""
    order = session.get("order", {})
    total = order.get("total_amount", Decimal("0.0"))

    threshold_dec = Decimal(str(threshold))
    rate_dec = Decimal(str(rate))

    discount = total * rate_dec if total >= threshold_dec else Decimal("0.0")
    session["discount"] = round(discount, 2)
    session["final_amount"] = round(total - discount, 2)


def calculate_shipping(session) -> None:
    """Calculate shipping based on priority"""
    order = session.get("order", {})
    priority = order.get("priority", "normal")
    shipping = Decimal("15.0") if priority == "express" else Decimal("5.0")
    session["shipping"] = shipping

    current_final = session.get("final_amount", Decimal("0.0"))
    session["final_amount"] = round(current_final + shipping, 2)


# Explicitly define jobs with metadata
jobs_list: List[Tuple[str, Any]] = [
    (
        "has_items",
        {
            "verbose_name": "Has Order Items",
            "callable": has_items,
            "job_type": "condition",
        },
    ),
    (
        "amount_sufficient",
        {
            "verbose_name": "Order Amount Sufficient",
            "callable": amount_sufficient,
            "job_type": "condition",
        },
    ),
    (
        "calculate_discount",
        {
            "verbose_name": "Calculate Discount",
            "callable": calculate_discount,
            "job_type": "action",
        },
    ),
    (
        "calculate_shipping",
        {
            "verbose_name": "Calculate Shipping",
            "callable": calculate_shipping,
            "job_type": "action",
        },
    ),
]
```

### Importing with `jobs_list`

```python
from sauron.rule_engine import RuleEngine
import order_jobs

engine = RuleEngine()

# Import jobs from the jobs_list
engine.import_jobs(order_jobs)

# Jobs are now available with their verbose names
for job_name, job_info in engine.callables_collected.items():
    print(f"{job_name}: {job_info['verbose_name']} ({job_info['type']})")

# Output:
# has_items: Has Order Items (condition)
# amount_sufficient: Order Amount Sufficient (condition)
# calculate_discount: Calculate Discount (action)
# calculate_shipping: Calculate Shipping (action)
```

### Using Imported Jobs with Rules

```python
rule = {
    "conditions": [
        {
            "name": "has_items",
            "args": {},
        },
        {
            "name": "amount_sufficient",
            "args": {"min_amount": 10.0},
        },
    ],
    "actions": [
        {
            "name": "calculate_discount",
            "args": {"threshold": 100.0, "rate": 0.1},
        },
        {
            "name": "calculate_shipping",
            "args": {},
        },
    ],
}

session = {
    "order": {
        "items": [{"product_id": "PROD-A", "quantity": 2}],
        "total_amount": Decimal("150.00"),
        "priority": "express",
    }
}

engine.run(rule, session=session)

print(f"Discount: ${session['discount']}")
print(f"Shipping: ${session['shipping']}")
print(f"Final Amount: ${session['final_amount']}")
```

## How It Works

### Automatic Discovery (without `jobs_list`)

When you call `engine.import_jobs(module)` and the module doesn't have a `jobs_list`:

1. The engine automatically discovers all functions in the module using `inspect.getmembers()`
2. Each function is imported as a job with:
   - `verbose_name`: The function name
   - `job_type`: "job" (default)
   - `callable`: The function itself

```python
# Any module with functions can be imported
engine.import_jobs(my_jobs_module)

# All functions become available as jobs
```

### Explicit Definition (with `jobs_list`)

When you define a `jobs_list` in your module:

1. The engine uses your explicit definitions
2. You control:
   - The job name (key in the tuple)
   - The verbose name (for display purposes)
   - The job type: "condition", "action", or "job"
   - Which functions to include

```python
jobs_list = [
    ("job_name", {
        "verbose_name": "Display Name",
        "callable": my_function,
        "job_type": "condition",  # or "action" or "job"
    }),
]
```

## Job Types

- **condition**: Jobs that return `bool`. If any condition returns `False`, the engine stops execution.
- **action**: Jobs that perform operations (mutations, calculations, etc.)
- **job**: Generic job type (default when not specified)

## Best Practices

1. **Organize by domain**: Group related conditions and actions in the same module
2. **Use `jobs_list` for clarity**: It makes your module self-documenting
3. **Use descriptive names**: Both function names and verbose names should be clear
4. **Specify job types**: Always set `job_type` to "condition" or "action" for clarity
5. **Keep modules focused**: Each module should handle a specific domain or functionality

## Example: Complete Application

See a complete example using batch jobs in the [Order Processing Sample App](../examples/sample_app/README.md).

## Related Features

- [Getting Started](getting_started.md) - Basic usage and decorator syntax
- [Schema Generation](schema.md) - Exporting job schemas for frontend integration
- [Sessions](index.md#sessions) - Sharing data between jobs
