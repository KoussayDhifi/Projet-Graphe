# ============================================================
# tests/test_graphs.py — Unit tests and sample graph fixtures
# ============================================================

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.graph import Graph


# ============================================================
# Fixtures
# ============================================================

def make_small_graph() -> Graph:
    """
    4-node undirected unweighted graph:

        0 -- 1
        |    |
        3 -- 2
    """
    g = Graph(directed=False, weighted=False)
    for pos in [(100, 100), (200, 100), (200, 200), (100, 200)]:
        g.add_node(*pos)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    return g


def make_weighted_graph() -> Graph:
    """
    5-node directed weighted graph for shortest-path testing:

        0 --(4)--> 1 --(1)--> 4
        |                     ^
       (2)                   (3)
        v                     |
        2 --(5)--> 3 ----------
    """
    g = Graph(directed=True, weighted=True)
    for pos in [(50,100),(150,100),(50,200),(150,200),(250,100)]:
        g.add_node(*pos)
    g.add_edge(0, 1, 4.0)
    g.add_edge(0, 2, 2.0)
    g.add_edge(1, 4, 1.0)
    g.add_edge(2, 3, 5.0)
    g.add_edge(3, 4, 3.0)
    return g


def make_disconnected_graph() -> Graph:
    """
    Two isolated components:
        Component A: 0 -- 1 -- 2
        Component B: 3 -- 4
    """
    g = Graph(directed=False, weighted=False)
    for pos in [(100,100),(200,100),(300,100),(100,300),(200,300)]:
        g.add_node(*pos)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    return g


def make_directed_graph() -> Graph:
    """
    Directed graph for SCC / traversal testing:

        0 → 1 → 2
            ↑   |
            |   ↓
            4 ← 3
    """
    g = Graph(directed=True, weighted=False)
    for pos in [(100,100),(200,100),(300,100),(300,200),(200,200)]:
        g.add_node(*pos)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)
    return g


# ============================================================
# Graph core tests
# ============================================================

class TestGraphConstruction:

    def test_add_nodes_sequential(self):
        g = Graph()
        ids = [g.add_node(i * 10, 0) for i in range(5)]
        assert ids == [0, 1, 2, 3, 4]

    def test_node_count(self):
        g = make_small_graph()
        assert g.node_count() == 4

    def test_edge_count_undirected(self):
        g = make_small_graph()
        assert g.edge_count() == 4

    def test_duplicate_edge_ignored(self):
        g = Graph()
        g.add_node(0, 0)
        g.add_node(10, 0)
        g.add_edge(0, 1)
        g.add_edge(0, 1)    # duplicate — should be ignored
        assert g.edge_count() == 1

    def test_self_loop_rejected(self):
        g = Graph()
        g.add_node(0, 0)
        with pytest.raises(ValueError):
            g.add_edge(0, 0)

    def test_nonexistent_node_rejected(self):
        g = Graph()
        g.add_node(0, 0)
        with pytest.raises(ValueError):
            g.add_edge(0, 99)


class TestAdjMatrix:

    def test_matrix_size(self):
        g = make_small_graph()
        m = g.to_matrix()
        assert len(m) == 4
        assert all(len(row) == 4 for row in m)

    def test_matrix_diagonal_zero(self):
        g = make_small_graph()
        m = g.to_matrix()
        for i in range(4):
            assert m[i][i] == 0.0

    def test_undirected_matrix_symmetric(self):
        g = make_small_graph()
        m = g.to_matrix()
        for i in range(4):
            for j in range(4):
                assert m[i][j] == m[j][i]

    def test_missing_edge_is_inf(self):
        g = Graph()
        g.add_node(0, 0)
        g.add_node(10, 0)
        # No edge added
        m = g.to_matrix()
        assert m[0][1] == float('inf')

    def test_weighted_matrix_values(self):
        g = make_weighted_graph()
        m = g.to_matrix()
        # Edge 0→1 has weight 4.0
        assert m[0][1] == 4.0
        # Directed: 1→0 should be inf
        assert m[1][0] == float('inf')


class TestAdjList:

    def test_adj_list_keys(self):
        g = make_small_graph()
        adj = g.to_adj_list()
        assert set(adj.keys()) == {0, 1, 2, 3}

    def test_undirected_both_directions(self):
        g = Graph()
        g.add_node(0, 0)
        g.add_node(10, 0)
        g.add_edge(0, 1, 2.5)
        adj = g.to_adj_list()
        assert (1, 2.5) in adj[0]
        assert (0, 2.5) in adj[1]

    def test_directed_one_direction_only(self):
        g = Graph(directed=True)
        g.add_node(0, 0)
        g.add_node(10, 0)
        g.add_edge(0, 1)
        adj = g.to_adj_list()
        assert any(n == 1 for n, _ in adj[0])
        assert not any(n == 0 for n, _ in adj[1])


class TestMutation:

    def test_remove_node(self):
        g = make_small_graph()
        g.remove_node(0)
        assert 0 not in g.nodes
        assert g.node_count() == 3
        for s, d, _ in g.edges:
            assert s != 0 and d != 0

    def test_remove_edge(self):
        g = make_small_graph()
        g.remove_edge(0, 1)
        assert not g.has_edge(0, 1)

    def test_clear(self):
        g = make_small_graph()
        g.clear()
        assert g.node_count() == 0
        assert g.edge_count() == 0


class TestSampleGraphs:
    """Sanity checks for the sample graphs used in integration tests."""

    def test_small_graph(self):
        g = make_small_graph()
        assert g.node_count() == 4
        assert g.edge_count() == 4
        assert not g.directed

    def test_weighted_graph(self):
        g = make_weighted_graph()
        assert g.weighted
        assert g.directed
        assert g.get_edge_weight(0, 1) == 4.0

    def test_disconnected_graph(self):
        g = make_disconnected_graph()
        # 0 and 3 are in different components
        assert not g.has_edge(0, 3)
        assert not g.has_edge(1, 3)
        assert not g.has_edge(2, 3)

    def test_directed_graph(self):
        g = make_directed_graph()
        assert g.directed
        # Cycle: 1→2→3→4→1
        assert g.has_edge(1, 2)
        assert g.has_edge(4, 1)


# ============================================================
# Algorithm interface smoke tests
# ============================================================

class TestAlgorithmInterfaces:
    """
    These tests verify that each algorithm stub exists and raises
    NotImplementedError (not any other exception).
    """

    def _check_stub(self, fn, graph, source=None):
        with pytest.raises(NotImplementedError):
            fn(graph, source)

    def test_dijkstra_stub(self):
        from algorithms.shortest_path.dijkstra import dijkstra
        self._check_stub(dijkstra, make_weighted_graph(), 0)

    def test_bellman_ford_stub(self):
        from algorithms.shortest_path.bellman_ford import bellman_ford
        self._check_stub(bellman_ford, make_weighted_graph(), 0)

    def test_kruskal_stub(self):
        from algorithms.mst.kruskal import kruskal
        self._check_stub(kruskal, make_weighted_graph())

    def test_prim_stub(self):
        from algorithms.mst.prim import prim
        self._check_stub(prim, make_weighted_graph(), 0)

    def test_bfs_stub(self):
        from algorithms.traversal.bfs import bfs
        self._check_stub(bfs, make_small_graph(), 0)

    def test_dfs_stub(self):
        from algorithms.traversal.dfs import dfs
        self._check_stub(dfs, make_small_graph(), 0)

    def test_connected_components_stub(self):
        from algorithms.components.connected import connected_components
        self._check_stub(connected_components, make_disconnected_graph())

    def test_scc_stub(self):
        from algorithms.components.scc import strongly_connected_components
        self._check_stub(strongly_connected_components, make_directed_graph())

    def test_welsh_powell_stub(self):
        from algorithms.coloring.welsh_powell import welsh_powell
        self._check_stub(welsh_powell, make_small_graph())


# ============================================================
# Registry tests
# ============================================================

class TestRegistry:

    def test_all_algorithms_registered(self):
        from algorithms.registry import ALGORITHMS
        expected = {
            "dijkstra", "bellman_ford", "kruskal", "prim",
            "bfs", "dfs", "connected", "scc", "welsh_powell",
        }
        assert expected.issubset(set(ALGORITHMS.keys()))

    def test_unknown_algorithm_raises(self):
        from algorithms.registry import run_algorithm
        g = make_small_graph()
        with pytest.raises(ValueError):
            run_algorithm("nonexistent_algo", g, 0)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
