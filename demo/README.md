# Demo: token minimizing workflow

## What this is

A minimal reference implementation of the token minimizing pattern: one simulated model call writes a solution, the solution is cached, local checks and a synthetic workload run it many times with no new model calls, and exactly one simulated debug call is spent when a deliberately failing case appears. It is written in plain Python with no external packages.

## What it is not

It is not a shipped product and it is not an employer system. The simulated model calls are counters inside the code, and the demo calls no real model and uses no network. All sample data is synthetic and invented for illustration only.

## Run it

1. Open a terminal in this folder.
2. Run: python3 token_min_demo.py

## What you should see

One generation call writes the solution. Four local checks run and four pass. One hundred workload runs complete with zero failures, and the model call count is still one after the workload. One failing case then triggers exactly one debug call, the fixed solution returns a total of 10 for that case, and the summary prints one hundred six local executions in total against two simulated model calls in total: one generation call and one debug call.

## The point of the demo

The demo shows where the model spend happens, and where it does not. Spend appears at exactly two moments: writing the solution once, and debugging the one failure the checks caught. Everything between those moments is plain local execution. That gap is the whole pattern.
