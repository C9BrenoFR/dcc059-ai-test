import sys
import time

from utils import draw_graph, draw_graphs, build_graph_from_ccplib

def menu(g) :
	while True:
		print("\n+-------------------------------------+")
		print("|          AÇÕES DISPONIVEIS          |")
		print("+-------------------------------------+")
		print("| (1) Imprimir lista de adjacencia    |")
		print("| (2) Desenhar Grafo                  |")
		print("| (3) Imprimir configurações do Grafo |")
		print("| (4) PCC (GPT)                       |")
		print("| (5) PCC (Gemini)                    |")
		print("| (6) PCC (Calude)                    |")
		print("| (7) PCC (Raptor)                    |")
		print("| (8) Benchmark de comparação         |")
		print("| (0) Sair                            |")
		print("+-------------------------------------+")

		selected = int(input("\nDigite o código da ação: "))

		match selected:
			case 0:
				print ("Encerrando...")
				break
			case 1:
				print(g.get_adjacency_list())
			case 2:
				draw_graph(g)
			case 3:
				g.print_config()
			case 4:
				start = time.perf_counter()
				pcc = g.capable_clustering_v1()
				end = time.perf_counter()

				print(f"\nPeso dos clusters:   {pcc["cluster_weights"]}")
				print(f"Beneficio total:     {pcc["total_benefit"]}")
				print(f"Tempo de execução:   {(end - start) * 1000:.3f} ms")
				draw_graph(pcc["clusters"])
			case 5:
				print("WIP...")
			case 6:
				start = time.perf_counter()
				pcc = g.capable_clustering_v2()
				end = time.perf_counter()

				print(f"\nPeso dos clusters: {pcc["cluster_weights"]}")
				print(f"Beneficio total:   {pcc["total_benefit"]}")
				print(f"Tempo de execução: {(end - start) * 1000:.3f} ms")
				
				draw_graphs(pcc["clusters"])

			case 7:
				print("WIP...")
			case 8:
				start = time.perf_counter()
				gpt_pcc = g.capable_clustering_v1()
				end = time.perf_counter()

				gpt_benchmark = (end - start) * 1000
				
				start = time.perf_counter()
				claude_pcc = g.capable_clustering_v2()
				end = time.perf_counter()

				claude_benchmark = (end - start) * 1000

				print("\n+---------------------------------------------------------------+")
				print("| Algoritmo | Tempo (ms)     | Beneficio Total | Nº de Clusters |")
				print("+-----------+----------------+-----------------+----------------+")
				print(f"| GPT       | {gpt_benchmark:14.3f} | {gpt_pcc["total_benefit"]:15.5f} | {len(gpt_pcc["cluster_weights"]):14d} |")
				print(f"| Claude    | {claude_benchmark:14.3f} | {claude_pcc["total_benefit"]:15.5f} | {len(claude_pcc["cluster_weights"]):14d} |")
				print("+-----------+----------------+-----------------+----------------+")
			case _:
				print("Opção inválida")

		

if __name__ == "__main__":
	if len(sys.argv) < 2:
		raise SystemExit("Utilização: python main.py <caminho-para-instancia-ccplib>")
	
	print(f"Inicializando Grafo {sys.argv[1]} ...")
	g = build_graph_from_ccplib(sys.argv[1])

	menu(g)