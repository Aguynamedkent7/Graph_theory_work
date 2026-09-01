# CS 414-4B Activity 1 (Part 2): Havel-Hakimi Algorithm

## Project Overview

Group project: implement the Havel-Hakimi algorithm in Python using `networkx` and `matplotlib`.

Activity 1 Part 2 covers scenario 2: decide if the degree sequence is **graphical**, and if so, construct the graph, verify degrees, and render a matplotlib plot. If not graphical, print a clear explanation of why.

## Scenario

| # | Scenario | Degree Sequence | Graphical? | Status |
|---|----------|-----------------|------------|--------|
| 2 | Environmental sensor nodes (6) | S2 = (5, 4, 3, 2, 1, 0) | No | DONE |

> Graphical status was verified with `networkx.is_graphical`.

## How to run

```bash
python -m pip install -r requirements.txt
python havel_hakimi.py          # runs scenario 2
```

## Code structure

- `havel_hakimi.py` — main library + scenario 2 runner
  - `havel_hakimi(sequence, labels, verbose=True)` — returns `(is_graphical, step)`, prints every reduction step
  - `is_graphical(sequence)` — pre-checks + HH outcome
  - `build_graph(sequence, labels)` — constructs the graph if graphical
  - `verify_degrees(G, expected, labels)` — confirms each vertex degree
  - `plot_graph(G, labels, title)` — renders with matplotlib
- `requirements.txt` — `networkx`, `matplotlib`

## Conventions

- Python 3.10+, standard PEP 8.
- No comments unless the code genuinely needs an explanation.
- Labels: nodes are named `V1, V2, ...`.
- Keep existing function signatures backward-compatible (others import from this file).
- Do not `git push`; commit on your own branch and someone approves/merges.

## GitHub issues workflow

- Use the GitHub issue for discussion.
- Consult `havel_hakimi.py` before raising "new" bugs — it's meant to be shared.