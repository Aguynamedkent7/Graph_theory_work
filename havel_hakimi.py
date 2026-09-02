import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import networkx as nx


def havel_hakimi(sequence, labels=None, verbose=True):
    """Run Havel-Hakimi reduction. Returns (is_graphical, step_count)."""
    seq = list(sequence)
    if labels is None:
        labels = [f"V{i+1}" for i in range(len(seq))]

    total = sum(seq)
    n = len(seq)
    if verbose:
        print(f"Sequence: {', '.join(f'{l}:{d}' for l, d in zip(labels, seq))}")
        print(f"Sum of degrees = {total}")
        print(f"Number of vertices = {n}")

    # Pre-checks: collect all violations
    violations = []

    if total % 2 != 0:
        violations.append(f"Sum = {total} is odd — Handshaking Lemma violated (sum of degrees must be even).")

    if any(d < 0 for d in seq):
        neg = [labels[i] for i, d in enumerate(seq) if d < 0]
        violations.append(f"Negative degree(s) found: {', '.join(f'{l}={seq[labels.index(l)]}' for l in neg)}.")

    if any(d >= n for d in seq):
        over = [labels[i] for i, d in enumerate(seq) if d >= n]
        violations.append(f"Degree(s) exceed or equal n-1 ({n-1}): {', '.join(f'{l}={d}' for l, d in zip(labels, seq) if d >= n)}.")

    if violations:
        if verbose:
            print("\nPre-check violations:")
            for v in violations:
                print(f"  - {v}")
            print(f"\nConclusion: Sequence is NOT graphical.")
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
    if out_path:
        plt.switch_backend("Agg")
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


def parse_sequence(raw):
    raw = raw.strip()
    parts = raw.replace(",", " ").split()
    return [int(p) for p in parts]


def main():
    out_path = os.environ.get("HH_OUT_PATH")

    print("=" * 60)
    print("CS 414-4B ACTIVITY 1 (Part 2): Havel-Hakimi Algorithm")
    print("=" * 60)

    while True:
        raw = input("\nEnter degree sequence (comma or space separated, or 'exit' to quit): ").strip()
        if raw.lower() == "exit":
            print("Goodbye!")
            break
        sequence = parse_sequence(raw)
        labels = [f"V{i+1}" for i in range(len(sequence))]

        result, step = havel_hakimi(sequence, labels)
        print(f"\nOutcome: {'Graphical' if result else 'NOT graphical'}")

        if not result:
            if out_path:
                with open(out_path, "w") as f:
                    f.write(f"Sequence = {sequence}\nSum = {sum(sequence)}\nResult: NOT graphical\n")
                print(f"Saved to {out_path}")
        else:
            G = build_graph(sequence, labels)
            print(f"Edge list: {sorted(G.edges())}")
            if verify_degrees(G, sequence, labels):
                plot_graph(G, labels, out_path=out_path)


if __name__ == "__main__":
    sys.exit(main())
