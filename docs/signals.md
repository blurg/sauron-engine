## Signals Quickstart

Signals (also known as hooks) allow you to run custom code at specific points during engine execution. This is useful for logging, monitoring, auditing, or custom side effects.

## Available Signals

The Sauron Engine provides four signals:

| Signal | When It Fires | Payload |
|--------|---------------|---------|
| `pre_engine_run` | Before the engine starts executing | `rule`, `session` |
| `post_engine_run` | After the engine finishes executing | `rule`, `session` |
| `pre_job_call` | Before each job executes | `job_name`, `job`, `session` |
| `post_job_call` | After each job executes | `job_name`, `job`, `session` |

## Basic Example: Logging Hook

```python
from sauron.rule_engine import RuleEngine

engine = RuleEngine()


@engine.condition("is_positive")
def is_positive(session, number: int = 10) -> bool:
    return number > 0


@engine.action("print_number")
def print_number(session, number: int = 10) -> None:
    print(f"Number: {number}")


# Define a callback function
def log_job_start(sender, **kwargs):
    print(f"Starting job: {kwargs['job_name']}")


# Connect the callback to the pre_job_call signal
pre_job_signal = engine.get_signal("pre_job_call")
pre_job_signal.connect(log_job_start, sender=engine)


rule = {
    "conditions": [
        {
            "name": "is_positive",
            "args": {"number": 5},
        }
    ],
    "actions": [
        {
            "name": "print_number",
            "args": {"number": 5},
        }
    ],
}

engine.run(rule)
# Output:
# Starting job: is_positive
# Starting job: print_number
# Number: 5
```

## Advanced Example: Performance Monitoring

```python
from sauron.rule_engine import RuleEngine
import time

engine = RuleEngine()


@engine.action("slow_action")
def slow_action(session) -> None:
    time.sleep(0.1)


@engine.action("fast_action")
def fast_action(session) -> None:
    time.sleep(0.01)


# Track job execution times
job_times = {}


def track_job_time(sender, **kwargs):
    job_name = kwargs["job_name"]
    if job_name not in job_times:
        job_times[job_name] = {"start": time.time(), "count": 0}
    else:
        duration = time.time() - job_times[job_name]["start"]
        job_times[job_name]["total_time"] = job_times.get(job_name, {}).get("total_time", 0) + duration
        job_times[job_name]["count"] += 1


# Connect tracking to both pre and post job calls
pre_signal = engine.get_signal("pre_job_call")
post_signal = engine.get_signal("post_job_call")

pre_signal.connect(track_job_time, sender=engine)
post_signal.connect(track_job_time, sender=engine)


def log_performance(sender, **kwargs):
    print("Job Performance Summary:")
    for job_name, data in job_times.items():
        if "total_time" in data:
            avg_time = data["total_time"] / data["count"]
            print(f"  {job_name}: {avg_time:.3f}s average")


# Connect to post_engine_run to print summary at the end
post_engine_signal = engine.get_signal("post_engine_run")
post_engine_signal.connect(log_performance, sender=engine)


rule = {
    "actions": [
        {"name": "slow_action"},
        {"name": "fast_action"},
        {"name": "slow_action"},
    ]
}

engine.run(rule)
# Output:
# Job Performance Summary:
#   slow_action: 0.100s average
#   fast_action: 0.010s average
```

## Disconnecting Signals

You can disconnect callbacks when they're no longer needed:

```python
pre_job_signal = engine.get_signal("pre_job_call")
pre_job_signal.disconnect(log_job_start, sender=engine)
```

## Multiple Callbacks

Multiple callbacks can be connected to the same signal:

```python
def audit_log(sender, **kwargs):
    with open("audit.log", "a") as f:
        f.write(f"Job executed: {kwargs['job_name']}\n")


def update_metrics(sender, **kwargs):
    # Update your metrics system
    pass


pre_job_signal = engine.get_signal("pre_job_call")
pre_job_signal.connect(audit_log, sender=engine)
pre_job_signal.connect(update_metrics, sender=engine)
```

## Session Monitoring Example

```python
from sauron.rule_engine import RuleEngine

engine = RuleEngine()


@engine.action("add_to_session")
def add_to_session(session, key: str, value: str) -> None:
    session[key] = value


def monitor_session(sender, **kwargs):
    print(f"Session state: {kwargs['session']}")


pre_job_signal = engine.get_signal("pre_job_call")
pre_job_signal.connect(monitor_session, sender=engine)


rule = {
    "actions": [
        {"name": "add_to_session", "args": {"key": "foo", "value": "bar"}},
        {"name": "add_to_session", "args": {"key": "baz", "value": "qux"}},
    ]
}

engine.run(rule)
# Output:
# Session state: {}
# Session state: {'foo': 'bar'}
```

## Use Cases

Signals are perfect for:

- **Logging**: Track job execution, session state, and results
- **Monitoring**: Measure performance, track metrics, set up alerts
- **Auditing**: Record all job executions for compliance
- **Caching**: Preload or invalidate caches based on job execution
- **Notifications**: Send alerts or messages when jobs run
- **Testing**: Add verification logic during test runs
