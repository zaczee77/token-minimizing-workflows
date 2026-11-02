# Token minimizing workflows

This repository collects a working note and a runnable reference demo by Nirmeet Rao on one rule for building with AI: token minimizing, not token maximizing. Spend the expensive model call where it creates something durable, then let plain code do the repeating.

## The rule

Most agent workflows pay a model for every step, every run, forever. This pattern pays once. A big model writes the code for a task. The code is saved, checked with tests, and then run locally as often as the work needs, at no further model cost. The big model comes back for exactly one job: debugging a failure the checks caught. Narrow tasks that repeat at volume go to plain automation first, and to a small model tuned for that one job only when rules are not enough.

## The pattern

1. Generate once. Ask the big model to write the solution for a task, and save the code, not just the answer.
2. Check it. Run tests and sample cases against the saved code locally until it earns trust.
3. Run it cheap. Execute the saved code for the repeat work. A rerun costs compute, not tokens.
4. Debug with the model, only on failure. When a check fails, send that one failure back to the big model, fix the code, and return to local runs.
5. Route narrow work down. A task that is narrow and repeated belongs to plain rules or a small model, never to the biggest model by default.

## Relation to his verified work

The rule grows out of the same discipline visible in his other projects. ephe, his Model Context Protocol platform for agent tooling, treats context as a budget and tool contracts as a product surface. PharmFlows, the LLM workflows he shipped at Concordia Pharma, reported serving time errors down 86 percent and cycle time down 30 percent on his resume, and those gains came from structure, validation, and review around the model rather than from more model calls. Paxei applied the same shape to prior authorization preparation, cutting prep time from 45 minutes to 10 minutes. His published research on bias mitigation in generative AI adds the matching caution: outputs need structured scrutiny before anyone trusts them. In each case the model does the part it is uniquely good at, and the surrounding system carries the rest.

## The demo in this repository

The demo folder contains a small reference implementation of this pattern in plain Python with no external packages. It simulates one model call that writes a solution, caches that solution, runs it locally through checks and a synthetic workload, then spends exactly one simulated debug call when a deliberately failing case appears. The counters are computed by the code itself and printed at the end. The demo calls no real model and uses no network. All sample data is synthetic and invented for illustration only.

## What this is not

This is not a shipped product. It is not an employer system. It is not a measured result from any job. It is a reference demo and a written pattern, built to illustrate a way of working that his verified projects already reflect.

## Links

1. Portfolio: https://nirmeetrao.com
2. GitHub: https://github.com/Zaczee77
3. LinkedIn: https://www.linkedin.com/in/nirmeet-rao
