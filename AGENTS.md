# CS 414-4B Activity 1 (Part 2): Havel-Hakimi Algorithm

## Project Overview

Group project: implement the Havel-Hakimi algorithm in Python using `networkx` and `matplotlib`.

The task: decide if each degree sequence is **graphical**, and if so, construct the graph, verify degrees, and render a matplotlib plot. If not graphical, print a clear explanation of why.

## Scenarios

| # | Scenario | Degree Sequence | Status |
|---|----------|-----------------|--------|
| 1 | Local tech company (6 servers) | S1 = (5, 4, 3, 2, 1, 1) | OPEN |
| 2 | Environmental sensor nodes (6) | S2 = (5, 4, 3, 2, 1, 0) | DONE (not graphical) |
| 3 | Data center switches (7) | S3 = (4, 3, 2, 2, 1, 0) | OPEN |
| 4 | Hex-grid map (6 territories) | S4 = (6, 3, 3, 2, 1, 1) | OPEN |
| 5 | Social network (6 members) | S5 = (5, 4, 3, 2, 1, 3) | OPEN |

> Note: the assignment only requires scenario 2, but we implement the shared library so any scenario can be run.

## How to run

```bash
python -m pip install -r requirements.txt
python havel_hakimi.py          # runs scenario 2 by default
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

- Each OPEN scenario has a GitHub issue. Use the issue for discussion.
- Consult `havel_hakimi.py` before raising "new" bugs — it's meant to be shared.