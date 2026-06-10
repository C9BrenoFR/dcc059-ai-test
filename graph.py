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
    #   1. Link da função que ele desenvolver (Também estara no prompt) 
    #   2. Arquivos graph.py, node.py e edge.py 
    #   3. Pasta de instancias ccplib

    # Função Criada por GPT-5.2-Codex 
    def capable_clustering_v1():
        pass

    # Função Criada por Claude Haiku 4.5 
    def capable_clustering_v2(self):
        """
        Resolve o Problema de Clusterização Capacitada (PCC).
        
        Retorna um dicionário contendo:
        - clusters: lista de listas com os nodes de cada cluster
        - cluster_weights: lista com o peso total de cada cluster
        - total_benefit: benefício total (soma das arestas internas)
        - assignment: lista indicando a qual cluster cada nó pertence
        """
        from node import Node
        
        num_nodes = len(self.nodes)
        num_clusters = self.num_clusters
        
        # Determinar os limites de capacidade para cada cluster
        if self.cluster_limits:
            # Usar cluster_limits se disponível (formato geral)
            cluster_capacity = None
            limits_per_cluster = []
            for k in range(num_clusters):
                min_idx = k * 2
                max_idx = k * 2 + 1
                if max_idx < len(self.cluster_limits):
                    limits_per_cluster.append((self.cluster_limits[min_idx], self.cluster_limits[max_idx]))
                else:
                    limits_per_cluster.append((0, float('inf')))
        else:
            # Usar cluster_capacity (instâncias Handover)
            cluster_capacity = self.cluster_capacity
            limits_per_cluster = [(0, cluster_capacity)] * num_clusters
        
        # Inicializar clusters vazios
        clusters = [[] for _ in range(num_clusters)]
        cluster_weights = [0.0] * num_clusters
        assignment = [-1] * num_nodes  # -1 significa não atribuído
        
        # Criar lista de arestas ordenadas por benefício (decrescente)
        edges_sorted = sorted(self.edges, key=lambda e: e.weight, reverse=True)
        
        # Fase 1: Tentar atribuir pares de nós conectados por arestas de alto benefício
        for edge in edges_sorted:
            u, v = edge.origin, edge.destination
            u_weight = self.nodes[u].weight
            v_weight = self.nodes[v].weight
            
            u_assigned = assignment[u] != -1
            v_assigned = assignment[v] != -1
            
            # Se nenhum está atribuído, tenta atribuir ambos ao mesmo cluster
            if not u_assigned and not v_assigned:
                for cluster_id in range(num_clusters):
                    min_cap, max_cap = limits_per_cluster[cluster_id]
                    new_weight = cluster_weights[cluster_id] + u_weight + v_weight
                    
                    # Verificar se cabe no cluster
                    if new_weight <= max_cap and len(clusters[cluster_id]) + 2 <= max_cap:
                        clusters[cluster_id].extend([u, v])
                        assignment[u] = cluster_id
                        assignment[v] = cluster_id
                        cluster_weights[cluster_id] = new_weight
                        break
            
            # Se apenas um está atribuído, tenta adicionar o outro ao mesmo cluster
            elif u_assigned and not v_assigned:
                cluster_id = assignment[u]
                min_cap, max_cap = limits_per_cluster[cluster_id]
                new_weight = cluster_weights[cluster_id] + v_weight
                
                if new_weight <= max_cap:
                    clusters[cluster_id].append(v)
                    assignment[v] = cluster_id
                    cluster_weights[cluster_id] = new_weight
            
            elif v_assigned and not u_assigned:
                cluster_id = assignment[v]
                min_cap, max_cap = limits_per_cluster[cluster_id]
                new_weight = cluster_weights[cluster_id] + u_weight
                
                if new_weight <= max_cap:
                    clusters[cluster_id].append(u)
                    assignment[u] = cluster_id
                    cluster_weights[cluster_id] = new_weight
        
        # Fase 2: Atribuir nós não atribuídos aos clusters com espaço disponível
        unassigned_nodes = [i for i in range(num_nodes) if assignment[i] == -1]
        
        # Ordenar clusters por peso atual (colocar nós em clusters com menos peso)
        for node_id in unassigned_nodes:
            node_weight = self.nodes[node_id].weight
            best_cluster = -1
            min_weight = float('inf')
            
            for cluster_id in range(num_clusters):
                min_cap, max_cap = limits_per_cluster[cluster_id]
                new_weight = cluster_weights[cluster_id] + node_weight
                
                # Se cabe e é o melhor até agora
                if new_weight <= max_cap and new_weight < min_weight:
                    best_cluster = cluster_id
                    min_weight = new_weight
            
            # Se encontrou um cluster disponível, atribuir
            if best_cluster != -1:
                clusters[best_cluster].append(node_id)
                assignment[node_id] = best_cluster
                cluster_weights[best_cluster] = min_weight
            else:
                # Se nenhum cluster tem espaço, colocar no menor (pode violar restrição)
                best_cluster = min(range(num_clusters), 
                                 key=lambda c: cluster_weights[c])
                clusters[best_cluster].append(node_id)
                assignment[node_id] = best_cluster
                cluster_weights[best_cluster] += node_weight
        
        # Fase 3: Calcular o benefício total (soma das arestas com ambos nós no mesmo cluster)
        total_benefit = 0.0
        cluster_edges = [[] for _ in range(num_clusters)]
        
        for edge in self.edges:
            u, v = edge.origin, edge.destination
            if assignment[u] == assignment[v]:
                total_benefit += edge.weight
                cluster_id = assignment[u]
                cluster_edges[cluster_id].append(edge)
        
        # Criar objetos Node para representar os clusters
        cluster_graphs = []
        for cluster_id in range(num_clusters):
            cluster_node_objects = [self.nodes[node_id] for node_id in clusters[cluster_id]]
            cluster_graph = Graph(
                nodes=cluster_node_objects,
                edges=cluster_edges[cluster_id],
                is_directed=self.is_directed,
                is_edge_weighted=self.is_edge_weighted,
                is_node_weighted=self.is_node_weighted,
                num_clusters=1,
                cluster_type=self.cluster_type,
                cluster_limits=self.cluster_limits,
                cluster_capacity=self.cluster_capacity,
            )
            cluster_graphs.append(cluster_graph)
        
        return {
            "clusters": cluster_graphs,
            "cluster_weights": cluster_weights,
            "total_benefit": total_benefit,
            "assignment": assignment,
        }

    # Função Criada por Gemini 3.1 Pro 
    def capable_clustering_v3():
        pass

    # Função Criada por Raptor Mini 
    def capable_clustering_v4():
        pass
