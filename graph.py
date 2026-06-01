class Graph:
    def __init__(
        self,
        nodes=None,
        edges=None,
        is_directed=False,
        is_edge_weighted=False,
        is_node_weighted=False,
        num_clusters=None,
        cluster_type=None,
        cluster_limits=None,
        cluster_capacity=None,
    ):
        self.nodes = nodes or []
        self.edges = edges or []
        self.is_directed = is_directed
        self.is_edge_weighted = is_edge_weighted
        self.is_node_weighted = is_node_weighted
        self.num_clusters = num_clusters
        self.cluster_type = cluster_type
        self.cluster_limits = cluster_limits or []
        self.cluster_capacity = cluster_capacity

    def get_adjacency_list(self):
        adjacency_list = {}

        for node in self.nodes:
            adjacency_list[node.identifier] = []

        for edge in self.edges:
            adjacency_list[edge.origin].append(edge.destination)
            if (not self.is_directed):
                adjacency_list[edge.destination].append(edge.origin)
        
        return adjacency_list