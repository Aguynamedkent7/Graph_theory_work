import unittest

from havel_hakimi import (
    build_graph,
    check_sequence,
    havel_hakimi,
    is_graphical,
    verify_degrees,
)


class TestCheckSequence(unittest.TestCase):
    def test_valid_sequence(self):
        ok, errors = check_sequence([2, 2, 2], verbose=False)
        self.assertTrue(ok)
        self.assertEqual(errors, [])

    def test_odd_sum(self):
        ok, errors = check_sequence([5, 4, 3, 2, 1, 0], verbose=False)
        self.assertFalse(ok)
        self.assertEqual(len(errors), 1)

    def test_negative_degree(self):
        ok, errors = check_sequence([-1, 2, 3], verbose=False)
        self.assertFalse(ok)
        self.assertTrue(any("negative" in e for e in errors))

    def test_degree_ge_n(self):
        ok, errors = check_sequence([5, 1, 1], verbose=False)
        self.assertFalse(ok)
        self.assertTrue(any(">= the number" in e for e in errors))

    def test_empty_sequence(self):
        ok, errors = check_sequence([], verbose=False)
        self.assertTrue(ok)

    def test_all_zeros(self):
        ok, errors = check_sequence([0, 0, 0], verbose=False)
        self.assertTrue(ok)


class TestHavelHakimi(unittest.TestCase):
    def test_graphical(self):
        result, step = havel_hakimi([2, 2, 2], verbose=False)
        self.assertTrue(result)

    def test_not_graphical_odd_sum(self):
        result, step = havel_hakimi([5, 4, 3, 2, 1, 0], verbose=False)
        self.assertFalse(result)

    def test_not_graphical_negative(self):
        result, step = havel_hakimi([5, 4, 3, 2, 1, 0], verbose=False)
        self.assertFalse(result)

    def test_single_zero(self):
        result, step = havel_hakimi([0], verbose=False)
        self.assertTrue(result)

    def test_all_zeros(self):
        result, step = havel_hakimi([0, 0, 0], verbose=False)
        self.assertTrue(result)

    def test_two_vertices(self):
        result, step = havel_hakimi([1, 1], verbose=False)
        self.assertTrue(result)

    def test_four_regular(self):
        result, step = havel_hakimi([3, 3, 3, 3], verbose=False)
        self.assertTrue(result)


class TestIsGraphical(unittest.TestCase):
    def test_matches_networkx(self):
        import networkx as nx
        sequences = [
            [3, 3, 3, 3],
            [2, 2, 2],
            [3, 2, 2, 1],
            [1, 1],
            [0],
            [5, 4, 3, 2, 1, 0],
            [3, 3, 3, 1],
            [2, 2, 2, 2],
            [1],
            [6, 5, 4, 3, 2, 1],
        ]
        for seq in sequences:
            self.assertEqual(
                is_graphical(seq, verbose=False),
                nx.is_graphical(seq),
                f"Mismatch for {seq}",
            )


class TestBuildAndVerify(unittest.TestCase):
    def test_round_trip_triangle(self):
        seq = [2, 2, 2]
        labels = ["V1", "V2", "V3"]
        G = build_graph(seq, labels, verbose=False)
        self.assertTrue(verify_degrees(G, seq, labels))

    def test_round_trip_k4(self):
        seq = [3, 3, 3, 3]
        labels = ["V1", "V2", "V3", "V4"]
        G = build_graph(seq, labels, verbose=False)
        self.assertTrue(verify_degrees(G, seq, labels))

    def test_round_trip_mixed(self):
        seq = [3, 2, 2, 1]
        labels = ["V1", "V2", "V3", "V4"]
        G = build_graph(seq, labels, verbose=False)
        self.assertTrue(verify_degrees(G, seq, labels))

    def test_round_trip_two_vertices(self):
        seq = [1, 1]
        labels = ["V1", "V2"]
        G = build_graph(seq, labels, verbose=False)
        self.assertTrue(verify_degrees(G, seq, labels))

    def test_build_raises_on_non_graphical(self):
        with self.assertRaises(ValueError):
            build_graph([5, 4, 3, 2, 1, 0], verbose=False)

    def test_edge_count_matches_sum(self):
        seq = [2, 2, 2]
        labels = ["V1", "V2", "V3"]
        G = build_graph(seq, labels, verbose=False)
        self.assertEqual(G.number_of_edges(), sum(seq) // 2)


if __name__ == "__main__":
    unittest.main()
