import sys

from utils import draw_graph, build_graph_from_ccplib

def menu(g) :
	while True:
		print("+-----------------------------------+")
		print("|         AÇÕES DISPONIVEIS         |")
		print("+-----------------------------------+")
		print("| (1) Imprimir lista de adjacencia  |")
		print("| (2) Desenhar Grafo                |")
		print("| (0) Sair                          |")
		print("+-----------------------------------+")

		selected = int(input("\nDigite o código da ação: "))

		match selected:
			case 0:
				print ("Encerrando...")
				break
			case 1:
				print(g.get_adjacency_list())
			case 2:
				draw_graph(g)
			case _:
				print("Opção inválida")

		

if __name__ == "__main__":
	if len(sys.argv) < 2:
		raise SystemExit("Utilização: python main.py <caminho-para-instancia-ccplib>")
	
	print(f"Inicializando Grafo {sys.argv[1]} ...")
	g = build_graph_from_ccplib(sys.argv[1])

	menu(g)