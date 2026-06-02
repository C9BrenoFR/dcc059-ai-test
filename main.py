import sys
import time

from utils import draw_graph, build_graph_from_ccplib

def menu(g) :
	while True:
		print("+-------------------------------------+")
		print("|          AÇÕES DISPONIVEIS          |")
		print("+-------------------------------------+")
		print("| (1) Imprimir lista de adjacencia    |")
		print("| (2) Desenhar Grafo                  |")
		print("| (3) Imprimir configurações do Grafo |")
		print("| (4) PCC (GPT)                       |")
		print("| (5) PCC (Gemini)                    |")
		print("| (6) PCC (Calude)                    |")
		print("| (7) PCC (Raptor)                    |")
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

				print(f"\nPeso dos clusters: {pcc["cluster_weights"]}")
				print(f"Beneficio total: {pcc["total_benefit"]}")
				print(f"Tempo de execução: {(end - start) * 1000:.3f} ms")
				draw_graph(pcc["clusters"])
			case _:
				print("Opção inválida")

		

if __name__ == "__main__":
	if len(sys.argv) < 2:
		raise SystemExit("Utilização: python main.py <caminho-para-instancia-ccplib>")
	
	print(f"Inicializando Grafo {sys.argv[1]} ...")
	g = build_graph_from_ccplib(sys.argv[1])

	menu(g)