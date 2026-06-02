# DCC059 AI Test (Grafos CCP)

Este projeto le instancias do ccplib e monta um grafo com pesos de nos e arestas. O programa oferece um menu simples para imprimir a lista de adjacencia ou desenhar o grafo.

## Requisitos

- Python 3.10+ (testado com 3.12)
- Pacotes Python:
  - matplotlib
  - networkx

## Instalacao

Crie e ative um ambiente virtual (opcional, mas recomendado):

```
python -m venv .venv
source .venv/bin/activate
```

Instale as dependencias:

```
pip install matplotlib networkx
```

## Uso

Execute informando o caminho para uma instancia do ccplib:

```
python main.py ccplib/RanReal240/RanReal240_02.txt
```

Ao iniciar, o programa exibe um menu:

- (1) Imprimir lista de adjacencia
- (2) Desenhar grafo
- (0) Sair

## Observacoes sobre os arquivos ccplib

- RanReal e Sparse: a primeira linha contem M, C, tipo de cluster (ss/ds), limites de cluster, o separador W e os pesos dos nos. As linhas seguintes contem as arestas no formato "origem destino peso".
- Handover: os tres primeiros valores sao N, C e a capacidade do cluster. Em seguida vem N pesos de nos e depois a matriz N x N de pesos das arestas.

Veja detalhes em ccplib/instance_format.txt.
