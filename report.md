# CS 414-4B Activity 1 (Part 2): Havel-Hakimi Trace

## Scenario 2 — Environmental Sensor Nodes (6 nodes)

**Degree sequence:** S2 = (5, 4, 3, 2, 1, 0)

### Handshaking Lemma check

Sum of degrees = 5 + 4 + 3 + 2 + 1 + 0 = **15 (odd)**.

The Handshaking Lemma states that every graph must have an even total degree because
each edge contributes 2 to the sum. Since 15 is odd, the sequence immediately fails.

### Havel-Hakimi reduction (continues for completeness)

| Step | Sorted sequence | Action | Result |
|------|----------------|--------|--------|
| 1 | [5, 4, 3, 2, 1, 0] | Remove d1 = 5, subtract 1 from next 5 entries | [3, 2, 1, 0, -1] |

A degree became **negative** (-1). The sequence is **NOT graphical**.

### networkx confirmation

```
>>> import networkx as nx
>>> nx.is_graphical([5, 4, 3, 2, 1, 0])
False
```

### Console output

```
============================================================
CS 414-4B ACTIVITY 1 (Part 2): Havel-Hakimi Algorithm
Scenario 2: Environmental sensor nodes
Target degree sequence S2 = [5, 4, 3, 2, 1, 0]
============================================================
Sequence: V1:5, V2:4, V3:3, V4:2, V5:1, V6:0
Sum of degrees = 15
>>> FAIL: Handshaking Lemma violated. A simple graph must have an
even number of total degree, but sum = 15 (odd). Therefore the
sequence is NOT graphical and no such network can be built.

Step 1: current sequence (sorted) = [5, 4, 3, 2, 1, 0]
Remove vertex of degree 5: 5 -> remaining [4, 3, 2, 1, 0]
Subtract 1 from next 5 degrees: [3, 2, 1, 0, -1]
>>> FAIL: a degree became negative. Sequence is NOT graphical.

Havel-Hakimi outcome: NOT graphical
Sequence [5, 4, 3, 2, 1, 0] cannot be realized as a simple graph.
```

### Conclusion

S2 = (5, 4, 3, 2, 1, 0) is **not graphical**. No simple graph with 6 vertices can realize this degree sequence.
