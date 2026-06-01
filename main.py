import matplotlib.pyplot as plt
import networkx as nx
import sys

from graph import Graph
from node import Node
from edge import Edge


def build_graph():
	if len(sys.argv) < 2:
		raise SystemExit("Usage: python main.py <path-to-ccplib-instance>")
	return build_graph_from_ccplib(sys.argv[1])


def build_graph_from_ccplib(path):
	with open(path, "r", encoding="utf-8") as file:
		content = file.read()

	lines = [line.strip() for line in content.splitlines() if line.strip()]
	if not lines:
		raise ValueError("Instance file is empty")

	header_tokens = lines[0].split()
	if len(header_tokens) >= 3 and header_tokens[2] in ("ss", "ds"):
		return parse_ccplib_general(lines)

	return parse_ccplib_handover(content)


def parse_ccplib_general(lines):
	header = lines[0].split()
	num_nodes = int(header[0])
	num_clusters = int(header[1])
	cluster_type = header[2]
	try:
		w_index = header.index("W")
	except ValueError as exc:
		raise ValueError("Invalid header: missing W separator") from exc

	cluster_limits = [float(value) for value in header[3:w_index]]
	node_weights = [float(value) for value in header[w_index + 1 : w_index + 1 + num_nodes]]
	if len(node_weights) != num_nodes:
		raise ValueError("Invalid header: node weight count mismatch")

	nodes = [Node(index, node_weights[index]) for index in range(num_nodes)]
	edges = []
	for line in lines[1:]:
		parts = line.split()
		if len(parts) != 3:
			continue
		origin, destination, weight = parts
		edges.append(Edge(int(origin), int(destination), float(weight)))

	return Graph(
		nodes,
		edges,
		False,
		True,
		True,
		num_clusters=num_clusters,
		cluster_type=cluster_type,
		cluster_limits=cluster_limits,
	)


def parse_ccplib_handover(content):
	tokens = content.split()
	if len(tokens) < 3:
		raise ValueError("Invalid Handover instance header")

	num_nodes = int(tokens[0])
	num_clusters = int(tokens[1])
	cluster_capacity = float(tokens[2])

	weights_start = 3
	weights_end = weights_start + num_nodes
	if len(tokens) < weights_end:
		raise ValueError("Invalid Handover instance: missing node weights")

	node_weights = [float(value) for value in tokens[weights_start:weights_end]]
	matrix_tokens = tokens[weights_end:]
	expected = num_nodes * num_nodes
	if len(matrix_tokens) < expected:
		raise ValueError("Invalid Handover instance: matrix size mismatch")

	nodes = [Node(index, node_weights[index]) for index in range(num_nodes)]
	edges = []
	idx = 0
	for i in range(num_nodes):
		for j in range(num_nodes):
			weight = float(matrix_tokens[idx])
			idx += 1
			if i < j and weight != 0:
				edges.append(Edge(i, j, weight))

	return Graph(
		nodes,
		edges,
		False,
		True,
		True,
		num_clusters=num_clusters,
		cluster_capacity=cluster_capacity,
	)



def draw_graph(g):
	graph_type = nx.DiGraph if g.is_directed else nx.Graph
	nx_graph = graph_type()
	for node in g.nodes:
		nx_graph.add_node(node.identifier, weight=node.weight)
	for edge in g.edges:
		nx_graph.add_edge(
			edge.origin,
			edge.destination,
			weight=edge.weight,
		)

	pos = nx.spring_layout(nx_graph)
	nx.draw(
		nx_graph,
		pos,
		with_labels=False,
		node_size=1200,
		node_color="#f7d487",
		edge_color="#333333",
		arrows=g.is_directed,
	)

	if g.is_node_weighted:
		node_labels = {
			node: f"{node}\n(w={data['weight']})"
			for node, data in nx_graph.nodes(data=True)
		}
	else:
		node_labels = {node: f"{node}" for node in nx_graph.nodes}

	nx.draw_networkx_labels(
		nx_graph,
		pos,
		labels=node_labels,
		font_weight="bold",
	)

	if g.is_edge_weighted:
		edge_labels = {
			(u, v): f"w={data['weight']}"
			for u, v, data in nx_graph.edges(data=True)
		}
		nx.draw_networkx_edge_labels(
			nx_graph,
			pos,
			edge_labels=edge_labels,
		)
	plt.show()

if __name__ == "__main__":
	g = build_graph()
	print(g.get_adjacency_list())
	draw_graph(g)