# Runtime Metrics

The Sauron Engine provides runtime metrics to help you track the performance of your rule executions. After each `engine.run()` call, you can access detailed timing information for each job and the total execution time.

## Metrics Structure

The `engine.runtime_metrics` dictionary contains:

- **`jobs`**: A dictionary mapping each job name to its execution time in seconds
- **`total_runtime`**: The total time taken for the entire rule execution in seconds

## Example

Here's a complete example showing how to use runtime metrics:

```py

from sauron.rule_engine import RuleEngine

engine = RuleEngine()


@engine.condition("Check Threshold")
def check_threshold(session, value: int = 10, threshold: int = 5) -> bool:
    """
    Checks if value exceeds threshold
    """
    return value > threshold


@engine.action("Process Value")
def process_value(session, value: int = 10, multiplier: int = 2) -> None:
    """
    Processes the value by multiplying it
    """
    result = value * multiplier
    print(f"Processed result: {result}")


@engine.action("Log Result")
def log_result(session) -> None:
    """
    Logs the processing result
    """
    print("Logging completed")


rule = {
    "conditions": [
        {
            "name": "check_threshold",
            "args": {"value": 15, "threshold": 10},
        }
    ],
    "actions": [
        {
            "name": "process_value",
            "args": {"value": 15, "multiplier": 3},
        },
        {
            "name": "log_result",
            "args": {},
        }
    ],
}


engine.run(rule)

# Access runtime metrics
metrics = engine.runtime_metrics

print("\n=== Runtime Metrics ===")
print(f"Total runtime: {metrics['total_runtime']:.6f} seconds")
print("\nPer-job execution times:")
for job_name, runtime in metrics['jobs'].items():
    print(f"  - {job_name}: {runtime:.6f} seconds")
```

Expected output:

```
Processed result: 45
Logging completed

=== Runtime Metrics ===
Total runtime: 0.001234 seconds

Per-job execution times:
  - check_threshold: 0.000005 seconds
  - process_value: 0.000012 seconds
  - log_result: 0.000003 seconds
```

## Notes

- Metrics are initialized to zero when the engine is created
- Job execution times are accumulated on the first run of each job
- `total_runtime` measures the complete rule execution from start to finish
- Use these metrics to identify performance bottlenecks in your rule chains
