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

    def print_config(self):
        print(f"É direcionado?:          {"Sim" if self.is_directed else "Não"}")
        print(f"É ponderado no vértice?: {"Sim" if self.is_node_weighted else "Não"}")
        print(f"É ponderado na aresta?:  {"Sim" if self.is_edge_weighted else "Não"}")
        print(f"Numero de clusters:      {self.num_clusters}")
        print(f"Tipo de cluster:         {self.cluster_type}")
        print(f"Capacidade do cluster:   {self.cluster_capacity}")
        print(f"Limites de cluster:      {self.cluster_limits}")

    def get_adjacency_list(self):
        adjacency_list = {}

        for node in self.nodes:
            adjacency_list[node.identifier] = []

        for edge in self.edges:
            adjacency_list[edge.origin].append(edge.destination)
            if (not self.is_directed):
                adjacency_list[edge.destination].append(edge.origin)
        
        return adjacency_list
    

    # Teste de resolução: Problema de Clusterização Capacitada
    #
    # Todos os modelos de IA vão ser usados no modo high,
    # esse modo é o mais lento, porém com maior profundidade cognitiva
    #
    # Para melhor teste, quando um modelo de IA for criar sua resolução do problema, 
    # as outras implementações serão apagadas
    #
    # Todos os modelos receberão o mesmo contexto:
    #   1. Pasta de instancias ccplib
    #   2. Arquivos graph.py, node.py e edge.py 

    # Função Criada por GPT-5.2-Codex 
    def capable_clustering_v1():
        pass

    # Função Criada por Claude Haiku 4.5 
    def capable_clustering_v2():
        pass

    # Função Criada por Gemini 3.1 Pro 
    def capable_clustering_v3():
        pass

    # Função Criada por Raptor Mini 
    def capable_clustering_v4():
        pass
