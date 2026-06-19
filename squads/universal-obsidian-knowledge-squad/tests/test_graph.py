import unittest
import _helper
import obsidian_index as idx
import obsidian_graph as graph


class TestGraph(unittest.TestCase):
    def setUp(self):
        self.cfg = _helper.write_temp_config(_helper.temp_config())
        idx.build_index(self.cfg, None)

    def test_graph_has_nodes_and_edges(self):
        g = graph.build_graph(self.cfg, None)
        self.assertGreaterEqual(g["node_count"], 3)
        self.assertGreater(g["edge_count"], 0)
        self.assertIn("clusters", g)


if __name__ == "__main__":
    unittest.main()
