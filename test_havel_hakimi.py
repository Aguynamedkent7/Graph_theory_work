import unittest

from havel_hakimi import build_graph, havel_hakimi, is_graphical, verify_degrees


class TestHavelHakimi(unittest.TestCase):
    def test_graphical(self):
        result, _ = havel_hakimi([2, 2, 2], verbose=False)
        self.assertTrue(result)

    def test_odd_sum(self):
        result, _ = havel_hakimi([5, 4, 3, 2, 1, 0], verbose=False)
        self.assertFalse(result)

    def test_negative_degree(self):
        result, _ = havel_hakimi([-1, 2, 3], verbose=False)
        self.assertFalse(result)

    def test_degree_ge_n(self):
        result, _ = havel_hakimi([5, 1, 1], verbose=False)
        self.assertFalse(result)

    def test_single_zero(self):
        result, _ = havel_hakimi([0], verbose=False)
        self.assertTrue(result)

    def test_all_zeros(self):
        result, _ = havel_hakimi([0, 0, 0], verbose=False)
        self.assertTrue(result)

    def test_two_vertices(self):
        result, _ = havel_hakimi([1, 1], verbose=False)
        self.assertTrue(result)

    def test_four_regular(self):
        result, _ = havel_hakimi([3, 3, 3, 3], verbose=False)
        self.assertTrue(result)

    def test_matches_networkx(self):
        import networkx as nx
        for seq in [[3,3,3,3], [2,2,2], [3,2,2,1], [1,1], [0],
                    [5,4,3,2,1,0], [3,3,3,1], [2,2,2,2], [1], [6,5,4,3,2,1]]:
            self.assertEqual(is_graphical(seq, verbose=False), nx.is_graphical(seq), f"Mismatch for {seq}")


class TestBuildAndVerify(unittest.TestCase):
    def test_round_trip(self):
        for seq, labels in [([2,2,2], ["V1","V2","V3"]),
                            ([3,3,3,3], ["V1","V2","V3","V4"]),
                            ([3,2,2,1], ["V1","V2","V3","V4"]),
                            ([1,1], ["V1","V2"])]:
            G = build_graph(seq, labels, verbose=False)
            self.assertTrue(verify_degrees(G, seq, labels))

    def test_build_raises_on_non_graphical(self):
        with self.assertRaises(ValueError):
            build_graph([5, 4, 3, 2, 1, 0], verbose=False)

    def test_edge_count(self):
        G = build_graph([2, 2, 2], verbose=False)
        self.assertEqual(G.number_of_edges(), 3)


if __name__ == "__main__":
    unittest.main()
