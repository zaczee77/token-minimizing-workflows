"""Token minimizing workflow demo.

A minimal reference implementation of the pattern described in the
repository README: one simulated model call writes a solution, the
solution is cached, local checks and a synthetic workload run it many
times with no new model calls, and exactly one simulated debug call
is spent when a deliberately failing case appears.

This demo is a teaching artifact built to illustrate the pattern. It
is not a shipped product and it is not an employer system. Every
record it touches is synthetic and invented for illustration only.
The simulated model calls are counters in this code. The demo calls
no real model and uses no network. It uses only the Python standard
library.

Run it with: python3 token_min_demo.py
"""


class ModelBudget:
    """Count simulated model calls by kind."""

    def __init__(self):
        self.generation_calls = 0
        self.debug_calls = 0

    def total_calls(self):
        return self.generation_calls + self.debug_calls


class LocalRunner:
    """Run cached solutions locally and count every execution."""

    def __init__(self):
        self.executions = 0

    def run(self, solution, records):
        self.executions += 1
        return solution(records)


def generate_solution(budget):
    """Simulate one expensive model call that writes the solution once."""
    budget.generation_calls += 1

    def solution(records):
        total = 0
        for record in records:
            total += record["quantity"]
        return total

    return solution


def debug_solution(budget):
    """Simulate one model call spent only because a check failed."""
    budget.debug_calls += 1

    def fixed(records):
        total = 0
        for record in records:
            quantity = record.get("quantity")
            if isinstance(quantity, int):
                total += quantity
        return total

    return fixed


ROUTES = [
    ("New code that does not exist yet", "big model, once, then cache the code"),
    ("The same task again", "plain local code, no model call"),
    ("A check fails", "big model, only to debug that failure"),
    ("One narrow task repeated at volume", "small model or plain rules"),
]


def main():
    budget = ModelBudget()
    runner = LocalRunner()
    cache = {}

    print("Step 1. One simulated generation call writes the solution once.")
    cache["total_quantity"] = generate_solution(budget)
    print("Generation calls: " + str(budget.generation_calls))
    solution = cache["total_quantity"]

    checks = [
        ([{"quantity": 30}, {"quantity": 12}], 42),
        ([{"quantity": 90}], 90),
        ([{"quantity": 5}, {"quantity": 5}, {"quantity": 5}], 15),
        ([], 0),
    ]
    passed = 0
    for records, expected in checks:
        result = runner.run(solution, records)
        if result == expected:
            passed += 1
    print("Step 2. Local checks run against the cached solution.")
    print("Checks run: " + str(len(checks)))
    print("Checks passed: " + str(passed))

    workload_runs = 100
    workload_failures = 0
    for index in range(workload_runs):
        batch = [{"quantity": (index % 5) + 1}, {"quantity": 2}]
        expected = (index % 5) + 3
        result = runner.run(solution, batch)
        if result != expected:
            workload_failures += 1
    print("Step 3. A synthetic workload runs locally with no new model calls.")
    print("Workload runs: " + str(workload_runs))
    print("Workload failures: " + str(workload_failures))
    print("Model calls after the workload: " + str(budget.total_calls()))

    print("Step 4. One failing case appears and triggers one simulated debug call.")
    failing_records = [{"quantity": 10}, {"note": "quantity missing"}]
    failing_cases = 0
    try:
        runner.run(solution, failing_records)
    except KeyError:
        failing_cases += 1
    fixed = debug_solution(budget)
    cache["total_quantity"] = fixed
    fixed_result = runner.run(fixed, failing_records)
    print("Failing cases: " + str(failing_cases))
    print("Debug calls: " + str(budget.debug_calls))
    print("Fixed run total: " + str(fixed_result))
    print("Fixed run matches the expected total of 10: " + str(fixed_result == 10))

    print("Summary")
    print("Local executions in total: " + str(runner.executions))
    print("Simulated model calls in total: " + str(budget.total_calls()))
    print("Generation calls: " + str(budget.generation_calls))
    print("Debug calls: " + str(budget.debug_calls))
    print("Routing used by this pattern:")
    for task, route in ROUTES:
        print(task + ": " + route)


if __name__ == "__main__":
    main()
