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
    def capable_clustering_v1(self):
        """
        Solve the capacitated clustering problem with a greedy + local search.

        Returns a dict with:
            clusters: Graph with only intra-cluster edges (each component is a cluster)
            assignment: dict mapping node_id -> cluster_index
            cluster_weights: list of total weights per cluster
            total_benefit: sum of edge weights within clusters
        """
        if self.num_clusters is None:
            raise ValueError("num_clusters is not set on the graph")

        if not self.nodes:
            return {
                "clusters": [[] for _ in range(self.num_clusters)],
                "assignment": {},
                "cluster_weights": [0.0 for _ in range(self.num_clusters)],
                "total_benefit": 0.0,
            }

        def build_cluster_bounds():
            if self.cluster_limits:
                if len(self.cluster_limits) >= 2 * self.num_clusters:
                    bounds = []
                    for idx in range(self.num_clusters):
                        min_cap = float(self.cluster_limits[idx * 2])
                        max_cap = float(self.cluster_limits[idx * 2 + 1])
                        bounds.append((min_cap, max_cap))
                    return bounds
                if len(self.cluster_limits) == 2:
                    min_cap = float(self.cluster_limits[0])
                    max_cap = float(self.cluster_limits[1])
                    return [(min_cap, max_cap) for _ in range(self.num_clusters)]
                raise ValueError("cluster_limits does not match num_clusters")

            if self.cluster_capacity is not None:
                max_cap = float(self.cluster_capacity)
                return [(0.0, max_cap) for _ in range(self.num_clusters)]

            return [(0.0, float("inf")) for _ in range(self.num_clusters)]

        cluster_bounds = build_cluster_bounds()
        cluster_mins = [bound[0] for bound in cluster_bounds]
        cluster_maxs = [bound[1] for bound in cluster_bounds]
        for idx, (min_cap, max_cap) in enumerate(cluster_bounds):
            if min_cap > max_cap:
                raise ValueError(f"Invalid cluster_limits for cluster {idx}")

        node_weights = {
            node.identifier: float(node.weight) if self.is_node_weighted else 1.0
            for node in self.nodes
        }

        total_min = sum(cluster_mins)
        total_weight = sum(node_weights.values())
        if total_weight + 1e-9 < total_min:
            raise ValueError("Total node weight is below minimum cluster limits")

        for node_id, weight in node_weights.items():
            if all(weight > max_cap + 1e-9 for max_cap in cluster_maxs):
                raise ValueError(f"Node {node_id} exceeds all cluster max limits")

        adjacency = {node.identifier: [] for node in self.nodes}
        for edge in self.edges:
            adjacency[edge.origin].append((edge.destination, float(edge.weight)))
            adjacency[edge.destination].append((edge.origin, float(edge.weight)))

        def is_adjacent_to_cluster(node_id, cluster_members):
            if not cluster_members:
                return True
            for neighbor_id, _ in adjacency[node_id]:
                if neighbor_id in cluster_members:
                    return True
            return False

        def is_cluster_connected(members):
            if len(members) <= 1:
                return True
            start = next(iter(members))
            visited = {start}
            stack = [start]
            while stack:
                current = stack.pop()
                for neighbor_id, _ in adjacency[current]:
                    if neighbor_id in members and neighbor_id not in visited:
                        visited.add(neighbor_id)
                        stack.append(neighbor_id)
            return len(visited) == len(members)

        def gain_to_cluster(node_id, cluster_id, cluster_members):
            gain = 0.0
            for neighbor_id, weight in adjacency[node_id]:
                if neighbor_id in cluster_members:
                    gain += weight
            return gain

        node_scores = {
            node_id: sum(weight for _, weight in neighbors)
            for node_id, neighbors in adjacency.items()
        }
        node_order = sorted(node_weights.keys(), key=lambda n: (-node_scores[n], n))

        clusters = [[] for _ in range(self.num_clusters)]
        cluster_members = [set() for _ in range(self.num_clusters)]
        cluster_weights = [0.0 for _ in range(self.num_clusters)]
        assignment = {}

        unassigned = set(node_weights.keys())

        isolated_nodes = [node_id for node_id, neighbors in adjacency.items() if not neighbors]
        if len(isolated_nodes) > self.num_clusters:
            raise ValueError("Too many isolated nodes to keep clusters connected")

        seed_order = isolated_nodes + [
            node_id for node_id in node_order if node_id not in isolated_nodes
        ]

        seed_index = 0
        for cluster_id in range(self.num_clusters):
            if not unassigned:
                break
            selected = None
            while seed_index < len(seed_order):
                candidate = seed_order[seed_index]
                seed_index += 1
                if candidate in unassigned:
                    if node_weights[candidate] <= cluster_maxs[cluster_id] + 1e-9:
                        selected = candidate
                        break
            if selected is None:
                continue
            clusters[cluster_id].append(selected)
            cluster_members[cluster_id].add(selected)
            cluster_weights[cluster_id] += node_weights[selected]
            assignment[selected] = cluster_id
            unassigned.remove(selected)

        def pick_best_for_needed():
            needed_clusters = [
                idx
                for idx in range(self.num_clusters)
                if cluster_weights[idx] + 1e-9 < cluster_mins[idx]
            ]
            if not needed_clusters:
                return None, None

            best_node = None
            best_cluster = None
            best_gain = None
            best_need = None

            for node_id in list(unassigned):
                node_weight = node_weights[node_id]
                for cluster_id in needed_clusters:
                    if cluster_weights[cluster_id] + node_weight > cluster_maxs[cluster_id] + 1e-9:
                        continue
                    if not is_adjacent_to_cluster(node_id, cluster_members[cluster_id]):
                        continue
                    gain = gain_to_cluster(node_id, cluster_id, cluster_members[cluster_id])
                    need = cluster_mins[cluster_id] - cluster_weights[cluster_id]
                    if best_gain is None or gain > best_gain + 1e-9:
                        best_gain = gain
                        best_node = node_id
                        best_cluster = cluster_id
                        best_need = need
                    elif abs(gain - best_gain) <= 1e-9 and need > (best_need or 0.0) + 1e-9:
                        best_node = node_id
                        best_cluster = cluster_id
                        best_need = need
            return best_node, best_cluster

        while True:
            node_id, cluster_id = pick_best_for_needed()
            if node_id is None:
                break
            clusters[cluster_id].append(node_id)
            cluster_members[cluster_id].add(node_id)
            cluster_weights[cluster_id] += node_weights[node_id]
            assignment[node_id] = cluster_id
            unassigned.remove(node_id)

        for idx in range(self.num_clusters):
            if cluster_weights[idx] + 1e-9 < cluster_mins[idx]:
                raise ValueError("Failed to satisfy minimum cluster limits")

        for node_id in list(unassigned):
            node_weight = node_weights[node_id]
            best_cluster = None
            best_gain = None
            for cluster_id in range(self.num_clusters):
                if cluster_weights[cluster_id] + node_weight > cluster_maxs[cluster_id] + 1e-9:
                    continue
                if not is_adjacent_to_cluster(node_id, cluster_members[cluster_id]):
                    continue
                gain = gain_to_cluster(node_id, cluster_id, cluster_members[cluster_id])
                if best_gain is None or gain > best_gain + 1e-9:
                    best_gain = gain
                    best_cluster = cluster_id
            if best_cluster is None:
                raise ValueError("No feasible cluster keeps connectivity for node assignment")
            clusters[best_cluster].append(node_id)
            cluster_members[best_cluster].add(node_id)
            cluster_weights[best_cluster] += node_weights[node_id]
            assignment[node_id] = best_cluster
            unassigned.remove(node_id)

        max_passes = 6
        for _ in range(max_passes):
            improved = False
            for node_id in node_order:
                current_cluster = assignment[node_id]
                node_weight = node_weights[node_id]
                if cluster_weights[current_cluster] - node_weight < cluster_mins[current_cluster] - 1e-9:
                    continue
                if len(cluster_members[current_cluster]) <= 1:
                    continue

                current_gain = gain_to_cluster(
                    node_id,
                    current_cluster,
                    cluster_members[current_cluster],
                )
                best_cluster = current_cluster
                best_delta = 0.0

                for cluster_id in range(self.num_clusters):
                    if cluster_id == current_cluster:
                        continue
                    if cluster_weights[cluster_id] + node_weight > cluster_maxs[cluster_id] + 1e-9:
                        continue
                    if not is_adjacent_to_cluster(node_id, cluster_members[cluster_id]):
                        continue
                    gain = gain_to_cluster(node_id, cluster_id, cluster_members[cluster_id])
                    delta = gain - current_gain
                    if delta > best_delta + 1e-9:
                        best_delta = delta
                        best_cluster = cluster_id

                if best_cluster != current_cluster:
                    remaining_members = cluster_members[current_cluster] - {node_id}
                    if not is_cluster_connected(remaining_members):
                        continue
                    cluster_members[current_cluster].remove(node_id)
                    cluster_members[best_cluster].add(node_id)
                    clusters[current_cluster].remove(node_id)
                    clusters[best_cluster].append(node_id)
                    cluster_weights[current_cluster] -= node_weight
                    cluster_weights[best_cluster] += node_weight
                    assignment[node_id] = best_cluster
                    improved = True

            if not improved:
                break

        total_benefit = 0.0
        for edge in self.edges:
            if assignment[edge.origin] == assignment[edge.destination]:
                total_benefit += float(edge.weight)

        cluster_edges = [
            edge
            for edge in self.edges
            if assignment[edge.origin] == assignment[edge.destination]
        ]
        clusters_graph = Graph(
            list(self.nodes),
            cluster_edges,
            self.is_directed,
            self.is_edge_weighted,
            self.is_node_weighted,
            num_clusters=self.num_clusters,
            cluster_type=self.cluster_type,
            cluster_limits=self.cluster_limits,
            cluster_capacity=self.cluster_capacity,
        )

        return {
            "clusters": clusters_graph,
            "assignment": assignment,
            "cluster_weights": cluster_weights,
            "total_benefit": total_benefit,
        }

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

    def capable_clustering_v3(self):
        import random
        from graph import Graph
        from edge import Edge

        num_clusters = self.num_clusters
        limits = []
        for i in range(1, num_clusters + 1):
            idx_min = (i - 1) * 2
            idx_max = idx_min + 1
            lim_min = self.cluster_limits[idx_min] if idx_min < len(self.cluster_limits) else 0
            lim_max = self.cluster_limits[idx_max] if idx_max < len(self.cluster_limits) else float('inf')
            limits.append((lim_min, lim_max))

        adj = {}
        for edge in self.edges:
            if edge.origin not in adj: adj[edge.origin] = {}
            if edge.destination not in adj: adj[edge.destination] = {}
            adj[edge.origin][edge.destination] = edge.weight
            adj[edge.destination][edge.origin] = edge.weight

        best_assignment = None
        best_benefit = -1
        best_weights = []

        for _ in range(100):
            nodes_sorted = sorted(self.nodes, key=lambda n: n.weight, reverse=True)
            assignment = {}
            cluster_weights = [0] * num_clusters
            
            valid = True
            for node in nodes_sorted:
                valid_clusters = [c for c in range(num_clusters) if cluster_weights[c] + node.weight <= limits[c][1]]
                if not valid_clusters:
                    valid_clusters = list(range(num_clusters)) # Fallback if too tight

                c_benefits = []
                for c in valid_clusters:
                    b = sum(adj.get(node.identifier, {}).get(other.identifier, 0) 
                            for other in assignment if assignment[other] == c)
                    c_benefits.append((b, c))
                
                c_benefits.sort(key=lambda x: x[0], reverse=True)
                max_b = c_benefits[0][0]
                rcl = [c for b, c in c_benefits if b >= max_b * 0.8]
                chosen = random.choice(rcl) if rcl else random.choice(valid_clusters)
                
                assignment[node] = chosen
                cluster_weights[chosen] += node.weight

            improved = True
            while improved:
                improved = False
                nodes_list = list(assignment.keys())
                random.shuffle(nodes_list)
                for i in range(len(nodes_list)):
                    n1 = nodes_list[i]
                    c1 = assignment[n1]
                    for j in range(i + 1, len(nodes_list)):
                        n2 = nodes_list[j]
                        c2 = assignment[n2]
                        if c1 == c2:
                            continue
                        
                        new_w1 = cluster_weights[c1] - n1.weight + n2.weight
                        new_w2 = cluster_weights[c2] - n2.weight + n1.weight
                        
                        if new_w1 <= limits[c1][1] and new_w2 <= limits[c2][1]:
                            loss_c1 = sum(adj.get(n1.identifier, {}).get(other.identifier, 0) for other in assignment if assignment[other] == c1 and other != n1)
                            gain_c1 = sum(adj.get(n2.identifier, {}).get(other.identifier, 0) for other in assignment if assignment[other] == c1 and other != n1)
                            
                            loss_c2 = sum(adj.get(n2.identifier, {}).get(other.identifier, 0) for other in assignment if assignment[other] == c2 and other != n2)
                            gain_c2 = sum(adj.get(n1.identifier, {}).get(other.identifier, 0) for other in assignment if assignment[other] == c2 and other != n2)
                            
                            delta = gain_c1 - loss_c1 + gain_c2 - loss_c2
                            if delta > 0:
                                assignment[n1] = c2
                                assignment[n2] = c1
                                cluster_weights[c1] = new_w1
                                cluster_weights[c2] = new_w2
                                c1, c2 = c2, c1
                                improved = True

            total_benefit = sum(adj.get(n1.identifier, {}).get(n2.identifier, 0) 
                              for n1 in assignment for n2 in assignment 
                              if n1.identifier < n2.identifier and assignment[n1] == assignment[n2])
            
            if total_benefit > best_benefit:
                best_benefit = total_benefit
                best_assignment = assignment.copy()
                best_weights = cluster_weights.copy()

        cluster_graphs = []
        if best_assignment:
            for c in range(num_clusters):
                c_nodes = [n for n in best_assignment if best_assignment[n] == c]
                c_edges = []
                for i, n1 in enumerate(c_nodes):
                    for j in range(i + 1, len(c_nodes)):
                        n2 = c_nodes[j]
                        if n2.identifier in adj.get(n1.identifier, {}):
                            c_edges.append(Edge(n1.identifier, n2.identifier, adj[n1.identifier][n2.identifier]))
                cg = Graph(c_nodes, c_edges, self.is_directed, self.is_edge_weighted, self.is_node_weighted, num_clusters=1)
                cluster_graphs.append(cg)

        return {
            "cluster_weights": best_weights,
            "total_benefit": best_benefit,
            "clusters": cluster_graphs
        }

    # Função Criada por Raptor Mini 
    def capable_clustering_v4():
        pass
