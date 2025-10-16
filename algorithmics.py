from collections import deque
from typing import List, Dict
from graph_abc import Graph


class GraphAlgorithms:
    """
    A collection of algorithms operating on Graph objects.
    NOTE: all algorithms are left as TODO stubs.
    They must utilize the representation methods implemented in Graph:
      - get_adjacency_list() - MUST be used
      - get_adjacency_matrix() - not required (but can be used for exta credit)
      - get_incidence_matrix() - not required (but can be used for extra credit)
    """

    @staticmethod
    def bfs(graph: Graph, start: int) -> List[int]:
        """
        Implementation steps:
            1) Validate start: ensure 0 <= start < graph.vertices.
               Raise IndexError if invalid.
            2) Obtain the adjacency list: adj = graph.get_adjacency_list().
               It is expected that the neighbors of each vertex are already sorted.
            3) Implement standard BFS:
               - Use a queue (FIFO).
               - Maintain a visited array/list of size n.
               - Process neighbors in ascending order.
            4) Return a list of vertices in the order they are dequeued
               (visit order).

        Args:
            graph (Graph): the graph on which the traversal is performed.
            start (int): the starting vertex.

        Returns:
            List[int]: the order in which vertices are visited by BFS.

        Hints:
            - Use deque from collections for the queue.
            - Mark vertices as visited at the time of enqueueing,
              not when dequeued — this avoids duplicates.
        """
        n = graph.vertices
        if not (0 <= start < n):
            raise IndexError("start vertex out of range")

        adj = graph.get_adjacency_list()
        visited = [False] * n
        order = []
        q = deque([start])
        visited[start] = True

        while q:
            u = q.popleft()
            order.append(u)
            for v, i in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    q.append(v)
        return order

    @staticmethod
    def dfs(graph: Graph, start: int) -> List[int]:
        """
        TODO: Depth-First Search (DFS) starting from vertex start.

        Implementation steps:
            1) Validate start: ensure 0 <= start < graph.vertices.
               Raise IndexError if invalid.
            2) Obtain the adjacency list: adj = graph.get_adjacency_list().
               Neighbors should already be sorted in ascending order.
            3) Implement DFS (recursive or iterative with a stack):
               - Mark the vertex as visited upon entering it.
               - Visit neighbors in ascending order.
            4) Return the list of vertices in preorder (first-time visits).

        Args:
            graph (Graph): the graph on which the traversal is performed.
            start (int): the starting vertex.

        Returns:
            List[int]: order of vertices visited by DFS.

        Hints:
            - Recursion is simpler, but watch recursion depth for large graphs.
            - In the iterative version, the order of adding neighbors to the stack
              affects determinism.
        """
        n = graph.vertices
        if not (0 <= start < n):
            raise IndexError("start vertex out of range")

        adj = graph.get_adjacency_list()
        visited = [False] * n
        order = []

        def dfs_visit(u: int):
            visited[u] = True
            order.append(u)
            for v, i in adj[u]:
                if not visited[v]:
                    dfs_visit(v)

        dfs_visit(start)
        return order

    @staticmethod
    def connected_components(graph: Graph) -> List[List[int]]:
        """
        Implementation steps:
            1) Get adjacency list: adj = graph.get_adjacency_list().
            2) If the graph is undirected:
               - Compute standard connected components.
            3) If the graph is directed:
               - Compute WEAKLY connected components (ignore edge directions).
                 You can build a temporary undirected adjacency list:
                 for each (u -> v), add both u-v and v-u.
            4) Traverse the graph (BFS or DFS) starting from unvisited vertices,
               collecting vertices of each component into a list.
            5) Sort vertices within each component in ascending order.
            6) Sort the list of components by the smallest vertex in each
               (deterministic ordering).

        Args:
            graph (Graph): the graph for which to compute connected components.

        Returns:
            List[List[int]]: list of components; each component is a sorted
            list of vertex indices.

        Hints:
            - Use a shared visited array to prevent revisiting vertices.
            - For directed graphs, build a temporary dict[int, List[int]]
              with symmetric edges, then perform BFS/DFS over it.
        """
        n = graph.vertices
        adj = graph.get_adjacency_list()

        # Build undirected adjacency for directed graph
        if graph.directed:
            undirected_adj = {i: set() for i in range(n)}
            for u in range(n):
                for v, _ in adj[u]:
                    undirected_adj[u].add(v)
                    undirected_adj[v].add(u)
            adj = {u: [(v, 1.0) for v in sorted(neighbors)] for u, neighbors in undirected_adj.items()}

        visited = [False] * n
        components = []

        def dfs_collect(u: int, comp: List[int]):
            visited[u] = True
            comp.append(u)
            for v, i in adj[u]:
                if not visited[v]:
                    dfs_collect(v, comp)

        for v in range(n):
            if not visited[v]:
                comp = []
                visited[u] = True
                comp.append(u)
                for v, i in adj[u]:
                    if not visited[v]:
                        dfs_collect(v, comp)
                components.append(sorted(comp))

        components.sort(key=lambda c: c[0]) # sort by smallest vertex
        return components

    @staticmethod
    def components_with_stats(graph: Graph) -> List[Dict[str, object]]:
        """
        TODO: Return statistics for each connected component.

        Implementation steps:
            1) Obtain components: comps = GraphAlgorithms.connected_components(graph).
            2) For each component, compute:
               - vertices: the sorted list of vertices.
               - node_count: number of vertices.
               - edge_count:
                   * For undirected graphs: count each edge once.
                     You can iterate over adj and only consider pairs (u, v)
                     where u < v.
                   * For directed graphs: count directed edges (u -> v)
                     where both endpoints are in the same component.
               - smallest_vertex: the smallest vertex (vertices[0]).
            3) Return a list of dictionaries (one per component) and SORT it by:
               (-node_count, -edge_count, smallest_vertex)
               i.e., larger components first, then those with more edges,
               then by smallest vertex ascending.

        Result element format:
            {
                "vertices": List[int],
                "node_count": int,
                "edge_count": int,
                "smallest_vertex": int
            }

        Args:
            graph (Graph): the graph for which to compute component statistics.

        Returns:
            List[Dict[str, object]]: sorted list of component statistics.

        Hints:
            - Build a vertex -> component_index mapping for quick lookup.
            - For undirected graphs, use u < v (or a set of pairs) to avoid
              double-counting edges.
        """
        comps = GraphAlgorithms.connected_components(graph)
        adj = graph.get_adjacency_list()

        # Map vertex to component index
        v2c = {}
        for i, comp in enumerate(comps):
            for v in comp:
                v2c[v] = i

        comp_edges = [0] * len(comps)

        if graph.directed:
            for u in range(graph.vertices):
                for v, _ in adj[u]:
                    if v2c[u] == v2c[v]:
                        comp_edges[v2c[u]] += 1
        else:
            counted = set()
            for u in range(graph.vertices):
                for v, i in adj[u]:
                    if v2c[u] == v2c[v]:
                        e = tuple(sorted((u, v)))
                        if e not in counted:
                            counted.add(e)
                            comp_edges[v2c[u]] += 1

        stats = []
        for i, comp in enumerate(comps):
            stats.append({
                "vertices": comp,
                "node_count": len(comp),
                "edge_count": comp_edges[i],
                "smallest_vertex": comp[0]
            })

        stats.sort(key=lambda s: (-s["node_count"], -s["edge_count"], s["smallest_vertex"])) # let's sort it by components and size
        return stats
