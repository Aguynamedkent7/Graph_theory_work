# CS 414-4B Activity 1 (Part 2): Havel-Hakimi Algorithm

## The Havel-Hakimi Algorithm

The Havel-Hakimi algorithm determines whether a given degree sequence can be realized as a simple graph (no loops, no multi-edges).

**Steps:**
1. Sort the sequence in non-increasing order.
2. Remove the first element *d*.
3. Subtract 1 from the next *d* elements.
4. Repeat until all elements are zero (graphical) or a negative element appears (not graphical).

A necessary precondition (Handshaking Lemma): the sum of all degrees must be even, since every edge contributes 2 to the total.

## Scenario 2

| # | Scenario | Nodes | Degree Sequence | Graphical? |
|---|----------|-------|-----------------|------------|
| 2 | Environmental sensor nodes | 6 | S2 = (5, 4, 3, 2, 1, 0) | **No** |

**Why not graphical:** Sum = 15 (odd), violating the Handshaking Lemma. Additionally, after removing the vertex of degree 5 and subtracting from the next 5 entries, a negative degree (-1) appears.

## Quick Start

```bash
python -m pip install -r requirements.txt
python havel_hakimi.py
```

## Headless / Report Figures

Set `HH_OUT_PATH` to save output instead of opening a display:

```bash
set HH_OUT_PATH=report_output.txt
python havel_hakimi.py
```

For graph plots (graphical scenarios only):

```bash
set HH_OUT_PATH=graph.png
python -c "from havel_hakimi import *; ..."
```

## Running Tests

```bash
python -m unittest test_havel_hakimi -v
```

## Project Structure

```
havel_hakimi.py        # Library + scenario 2 runner
test_havel_hakimi.py   # Unit tests (20 tests)
report.md              # Manual HH trace for the activity report
requirements.txt       # networkx, matplotlib
```
