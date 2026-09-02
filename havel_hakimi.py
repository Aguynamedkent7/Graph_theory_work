import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


def describe(seq, labels):
    return ", ".join(f"{label}:{deg}" for label, deg in zip(labels, seq))


def havel_hakimi(sequence, labels=None, verbose=True):
    seq = list(sequence)
    if labels is None:
        labels = [f"V{i+1}" for i in range(len(seq))]

    total = sum(seq)
    if verbose:
        print(f"Sequence: {describe(seq, labels)}")
        print(f"Sum of degrees = {total}")
        if total % 2 != 0:
            print(
                f">>> FAIL: Handshaking Lemma violated. A simple graph must have an "
                f"even number of total degree, but sum = {total} (odd). Therefore the "
                f"sequence is NOT graphical and no such network can be built."
            )
        else:
            print(f"Sum is even ({total}), so the Handshaking Lemma holds.")

    seq = sorted(seq, reverse=True)
    step = 0
    while seq:
        step += 1
        if verbose:
            print(f"\nStep {step}: current sequence (sorted) = {seq}")
        if seq[0] > len(seq) - 1:
            if verbose:
                print(
                    f">>> FAIL: d1 = {seq[0]} but there are only {len(seq) - 1} other "
                    f"vertices. This would require more neighbors than exist. "
                    f"Sequence is NOT graphical."
                )
            return False, step
        if all(d == 0 for d in seq):
            if verbose:
                print(">>> SUCCESS: all degrees are zero. Sequence IS graphical.")
            return True, step
        d = seq.pop(0)
        if verbose:
            print(f"Remove vertex of degree {d}: {d} -> remaining {seq}")
        if d > len(seq):
            if verbose:
                print(
                    f">>> FAIL: degree {d} exceeds the number of remaining vertices "
                    f"({len(seq)}). Sequence is NOT graphical."
                )
            return False, step
        seq = [x - 1 if i < d else x for i, x in enumerate(seq)]
        if verbose:
            print(f"Subtract 1 from next {d} degrees: {seq}")
        if any(x < 0 for x in seq):
            if verbose:
                print(
                    f">>> FAIL: a degree became negative. "
                    f"Sequence is NOT graphical."
                )
            return False, step
        seq.sort(reverse=True)
    if verbose:
        print(">>> SUCCESS: sequence exhausted. Sequence IS graphical.")
    return True, step


def check_sequence(sequence, labels=None, verbose=True):
    errors = []
    total = sum(sequence)
    if total % 2 != 0:
        errors.append(
            f"sum of degrees is {total} (odd), violating the Handshaking Lemma which "
            f"requires the total degree of any graph to be even."
        )
    if any(d < 0 for d in sequence):
        errors.append("a degree value is negative, which is invalid.")
    if any(d >= len(sequence) for d in sequence):
        errors.append(
            "a degree value is >= the number of vertices, meaning a vertex would need "
            "to connect to more vertices than exist in a simple graph."
        )
    if errors:
        if verbose:
            print("\nPre-check failed:")
            for e in errors:
                print(f"  - {e}")
        return False, errors
    return True, []


def is_graphical(sequence, labels=None, verbose=True):
    ok, errors = check_sequence(sequence, labels, verbose=verbose)
    if errors:
        return False
    return havel_hakimi(sequence, labels, verbose=verbose)[0]


def build_graph(sequence, labels=None, verbose=True):
    if labels is None:
        labels = [f"V{i+1}" for i in range(len(sequence))]

    graphical, _ = havel_hakimi(sequence, labels, verbose=False)
    if not graphical:
        raise ValueError(
            f"Sequence {sequence} is NOT graphical, so no simple graph can be "
            f"constructed from it."
        )

    degs = {label: int(d) for label, d in zip(labels, sequence)}
    G = nx.Graph()
    G.add_nodes_from(labels)

    remaining = dict(degs)
    while True:
        v = max(remaining, key=remaining.get)
        d = remaining.pop(v)
        if d == 0:
            break
        neighbors = sorted(remaining, key=remaining.get, reverse=True)[:d]
        if len(neighbors) < d or any(remaining[w] <= 0 for w in neighbors):
            raise ValueError(
                f"Internal error while constructing graph for {sequence}: vertex "
                f"{v} needs degree {d} but not enough remaining vertices can accept "
                f"an edge. The Havel-Hakimi precondition is not satisfiable."
            )
        for w in neighbors:
            G.add_edge(v, w)
            remaining[w] -= 1

    if verbose:
        print("\nBuilt networkx graph object with nodes:", list(G.nodes))
    return G


def verify_degrees(G, expected, labels):
    failures = []
    for label, want in zip(labels, expected):
        got = G.degree(label)
        status = "OK" if got == want else "MISMATCH"
        if got != want:
            failures.append(label)
        print(f"  Vertex {label}: expected degree {want}, actual degree {got} [{status}]")

    if failures:
        print(f"ERROR: degree verification failed for vertices: {failures}")
        return False
    print("\nAll degrees verified successfully. The graph matches the sequence.")
    return True


def plot_graph(G, labels, title="Constructed Network", out_path=None):
    pos = nx.circular_layout(G)
    nx.draw_networkx(
        G,
        pos,
        labels={v: v for v in labels},
        node_color="lightblue",
        node_size=800,
        font_size=12,
        font_weight="bold",
        with_labels=True,
    )
    plt.title(title)
    plt.axis("off")
    plt.tight_layout()
    if out_path:
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        print(f"Figure saved to {out_path}")
    else:
        plt.show()
    plt.close()


def main():
    import os
    sequence = [5, 4, 3, 2, 1, 0]
    labels = [f"V{i+1}" for i in range(len(sequence))]
    out_path = os.environ.get("HH_OUT_PATH")

    print("=" * 60)
    print("CS 414-4B ACTIVITY 1 (Part 2): Havel-Hakimi Algorithm")
    print("Scenario 2: Environmental sensor nodes")
    print(f"Target degree sequence S2 = {sequence}")
    print("=" * 60)

    result, step = havel_hakimi(sequence, labels)
    print(f"\nHavel-Hakimi outcome: {'Graphical' if result else 'NOT graphical'}")
    if not result:
        print(f"Sequence {sequence} cannot be realized as a simple graph.")
        if out_path:
            msg = (
                f"Scenario 2: S2 = {sequence}\n"
                f"Sum of degrees = {sum(sequence)} (odd)\n"
                f"Havel-Hakimi result: NOT graphical\n"
            )
            with open(out_path, "w") as f:
                f.write(msg)
            print(f"Non-graphical message saved to {out_path}")
    else:
        print(f"Sequence {sequence} is graphical (verified at step {step}).")
        print("\n--- Constructing graph ---")
        G = build_graph(sequence, labels)
        if G is None:
            return
        print(f"\nEdge list: {sorted(G.edges())}")
        print("\nDegree verification:")
        if verify_degrees(G, sequence, labels):
            plot_graph(G, labels, title="Scenario 2: Sensor Network (S2)", out_path=out_path)


if __name__ == "__main__":
    sys.exit(main())