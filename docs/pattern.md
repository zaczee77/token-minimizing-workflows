# The token minimizing pattern

## The problem

A model call is priced per token, and an agent loop multiplies that price by every step of every run. When the workflow rethinks the same task from scratch each time, the team pays full price again and again for reasoning that has not changed. The output may be fine. The economics are not.

## The routing table

1. New code that does not exist yet goes to the big model, once. The deliverable is saved code, not a chat answer that evaporates.
2. Repeat execution goes to plain local code. Once the solution exists and passes its checks, running it again is a compute task, not a thinking task.
3. A failing check goes back to the big model for debugging, and only that failure goes. The model sees the failing case and the error, fixes the code, and steps away again.
4. One narrow task repeated at volume goes to plain rules first, and to a small model tuned for that single job when rules are not enough. The biggest model is the last resort for narrow work, not the default.

## Rules that keep it honest

1. Cache the code, not the answer. An answer helps once. Code keeps helping on every run after.
2. Tests are the gate. Saved code earns its local runs by passing checks that a person wrote on purpose.
3. One failure, one debug call. Repeated failures of the same kind are batched into a single debugging pass instead of paying for each one separately.
4. Count model calls like money. Generation calls and debug calls are counted separately, so the team can see exactly where the spend goes.
5. Keep a human review point for anything the checks cannot confirm. Cheap execution of an unreviewed action is still an unreviewed action.

## When to spend tokens anyway

Some work deserves the expensive call every time: a genuinely new problem, an ambiguous requirement, a failure nobody understands yet, and any task where judgment itself is the product. Token minimizing is not about avoiding the model. It is about refusing to buy the same reasoning twice.

## Relation to evals and his research

This pattern stands or falls on the quality of its checks, which is the same lesson as his published research on bias mitigation in generative AI: model outputs need structured scrutiny before anyone calls them good. A cheap rerun of an unchecked solution is just a cheaper error. The checks are what let the spend drop without the trust dropping with it.
