import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


def havel_hakimi(sequence, labels=None, verbose=True):
    seq = list(sequence)
    if labels is None:
        labels = [f"V{i+1}" for i in range(len(seq))]

    total = sum(seq)
    if verbose:
        print(f"Sequence: {', '.join(f'{l}:{d}' for l, d in zip(labels, seq))}")
        print(f"Sum of degrees = {total}")

    # Pre-checks: Handshaking Lemma, non-negative, degree < n
    if total % 2 != 0:
        if verbose:
            print(f">>> FAIL: sum = {total} (odd). Handshaking Lemma violated.")
        return False, 0
    if any(d < 0 for d in seq):
        if verbose:
            print(">>> FAIL: negative degree value.")
        return False, 0
    if any(d >= len(seq) for d in seq):
        if verbose:
            print(f">>> FAIL: degree >= {len(seq)} (number of vertices).")
        return False, 0

    # Reduction loop
    seq.sort(reverse=True)
    step = 0
    while seq:
        step += 1
        if verbose:
            print(f"\nStep {step}: {seq}")
        if all(d == 0 for d in seq):
            if verbose:
                print(">>> SUCCESS: all zeros. Sequence IS graphical.")
            return True, step
        d = seq.pop(0)
        if d > len(seq):
            if verbose:
                print(f">>> FAIL: degree {d} > {len(seq)} remaining vertices.")
            return False, step
        seq = [x - 1 if i < d else x for i, x in enumerate(seq)]
        if any(x < 0 for x in seq):
            if verbose:
                print(f">>> FAIL: negative degree after reduction.")
            return False, step
        seq.sort(reverse=True)
    return True, step


def is_graphical(sequence, verbose=True):
    return havel_hakimi(sequence, verbose=verbose)[0]


def build_graph(sequence, labels=None, verbose=True):
    if labels is None:
        labels = [f"V{i+1}" for i in range(len(sequence))]
    if not havel_hakimi(sequence, verbose=False)[0]:
        raise ValueError(f"Sequence {sequence} is NOT graphical.")

    G = nx.Graph()
    G.add_nodes_from(labels)
    remaining = {l: int(d) for l, d in zip(labels, sequence)}

    while remaining:
        v = max(remaining, key=remaining.get)
        d = remaining.pop(v)
        if d == 0:
            break
        neighbors = sorted(remaining, key=remaining.get, reverse=True)[:d]
        for w in neighbors:
            G.add_edge(v, w)
            remaining[w] -= 1

    if verbose:
        print("Built graph with nodes:", list(G.nodes))
    return G


def verify_degrees(G, expected, labels):
    ok = all(G.degree(l) == d for l, d in zip(labels, expected))
    for l, d in zip(labels, expected):
        print(f"  {l}: expected {d}, got {G.degree(l)} {'OK' if G.degree(l) == d else 'MISMATCH'}")
    return ok


def plot_graph(G, labels, title="Constructed Network", out_path=None):
    nx.draw_networkx(G, nx.circular_layout(G), labels={v: v for v in labels},
                     node_color="lightblue", node_size=800, font_size=12,
                     font_weight="bold", with_labels=True)
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
    sequence = [5, 4, 3, 2, 1, 0]
    labels = [f"V{i+1}" for i in range(len(sequence))]
    out_path = os.environ.get("HH_OUT_PATH")

    print("=" * 60)
    print("CS 414-4B ACTIVITY 1 (Part 2): Havel-Hakimi Algorithm")
    print("Scenario 2: Environmental sensor nodes")
    print(f"Target degree sequence S2 = {sequence}")
    print("=" * 60)

    result, step = havel_hakimi(sequence, labels)
    print(f"\nOutcome: {'Graphical' if result else 'NOT graphical'}")

    if not result:
        if out_path:
            with open(out_path, "w") as f:
                f.write(f"S2 = {sequence}\nSum = {sum(sequence)} (odd)\nResult: NOT graphical\n")
            print(f"Saved to {out_path}")
    else:
        G = build_graph(sequence, labels)
        print(f"Edge list: {sorted(G.edges())}")
        if verify_degrees(G, sequence, labels):
            plot_graph(G, labels, out_path=out_path)


if __name__ == "__main__":
    sys.exit(main())
