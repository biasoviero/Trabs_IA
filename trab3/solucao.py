from typing import Iterable, Set, Tuple
import heapq

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado:str, pai:'Nodo' = None, acao:str = None, custo:int = 0):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao  # acao que foi aplicada ao nó pai para gerar este
        self.custo = custo # path cost: o custo do caminho a partir do estado inicial até este no. Cada acao (aresta do grafo) tem custo 1. Custo de um no = custo do pai + 1
        # self.filhos = filhos # (opcional) referencias para os nos filhos.

    def __eq__(self, outro: object) -> bool:
          """
          Compara dois nodos
          :param outro: O outro nodo a ser comparado.
          :return: True se os nodos sao iguais, False caso contrario.
          """

          if isinstance(outro, Nodo):

            return (
                self.estado == outro.estado and
                self.pai == outro.pai and
                self.acao == outro.acao and
                self.custo == outro.custo
            )
          return False


    def __lt__(self, outro: object) -> bool:
      return ((self.custo, self.estado) < (outro.custo, outro.estado))

    def __hash__(self):
      return hash((self.estado, self.pai, self.acao, self.custo))

    def __repr__(self):
        return (f"\nNodo(estado='{self.estado}', \n pai={self.pai}, \nacao='{self.acao}', \ncusto={self.custo}")

def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # Inicializa set de sucessores
    sucessores = set()

    # Definição dos deslocamentos
    movimentos = {
        'acima': -3,
        'abaixo': 3,
        'esquerda': -1,
        'direita': 1
    }

    # Índice do espaço vazio
    index = estado.index('_')

    # Valida possíveis deslocamentos
    for acao, deslocamento in movimentos.items():
        novo_index = index + deslocamento

        if 0 <= novo_index < 9:  # Se movimento válido
            if (acao == 'esquerda' and index % 3 == 0) or (acao == 'direita' and index % 3 == 2) or (acao == 'acima' and index < 3) or (acao == 'abaixo' and index >= 6):
                continue

            # Cria e troca o estado
            novo_estado = list(estado)  # Transforma o estado em uma lista de caracteres
            novo_estado[index], novo_estado[novo_index] = novo_estado[novo_index], novo_estado[index]  # Troca as posições
            novo_estado = ''.join(novo_estado)  # Transforma a lista de volta em string

            # Adiciona o sucessor ao conjunto
            sucessores.add((acao, novo_estado))

    return sucessores

def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    # inicializa set de nodos
    novos_nodos = set()

    # recupera os sucessores
    sucessores = sucessor(nodo.estado)

    # para cada sucessor, cria um novo nodo e adiciona ao conjunto
    for acao, novo_estado in sucessores:
        novo_nodo = Nodo(novo_estado, nodo, acao, nodo.custo + 1)
        novos_nodos.add(novo_nodo)

    return novos_nodos

def distancia_hamming(estado:str)->int:
  """
  Calcula a distancia de Hamming
  entre o estado atual e o estado objetivo.
  """
  OBJETIVO = "12345678_"
  distancia = 0
  for i in range(len(estado)):
    if estado[i] != OBJETIVO[i] and estado[i] != '-':
      distancia += 1
  return distancia

def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    OBJETIVO = "12345678_"

    expandidos = 0

    # caso o estado recebido ja seja a solucao, retorna lista vazia
    if estado == OBJETIVO:
        return []


    # conjunto de nodos explorados
    X = set()

    nodo_inicial = Nodo(estado)
    # fila de prioridades para a fronteira
    F = [(distancia_hamming(estado), nodo_inicial)]



    while F:
      _, nodo = heapq.heappop(F)
      if nodo.estado == OBJETIVO:
            caminho = []
            while nodo.pai:
                caminho.append(nodo.acao)
                nodo = nodo.pai
            print(f"Expandidos: {expandidos}")
            return list(reversed(caminho))

      if nodo.estado not in X:
        # insere v em x
        X.add(nodo.estado)

        # cria nodo para cada u vizinho de v e insere em F (se ainda nao esta em x)
        expandidos += 1
        for filho in expande(nodo):
            if filho.estado not in X:
                custo_total = filho.custo + distancia_hamming(filho.estado)
                heapq.heappush(F, (custo_total, filho))

    # se nao ha solucao
    print(f"Expandidos: {expandidos}")
    return None

def distancia_manhattan(estado:str)->int:
  """
  Calcula a distancia manhattan
  entre o estado atual e o estado objetivo.
  """
  OBJETIVO = "12345678_"
  distancia = 0

  for i, char in enumerate(estado):
    if char != '_':

      # posicao
      linha, coluna = i // 3, i % 3

      # objetivo
      indice = OBJETIVO.index(char)
      nova_linha, nova_coluna = indice // 3, indice % 3

      # calculo da distancia
      distancia += abs(linha - nova_linha) + abs(coluna - nova_coluna)

  return distancia

def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    OBJETIVO = "12345678_"
    expandidos = 0

    # caso o estado recebido ja seja a solucao, retorna lista vazia
    if estado == OBJETIVO:
        return []


    # conjunto de nodos explorados
    X = set()

    nodo_inicial = Nodo(estado)
    # fila de prioridades para a fronteira
    F = [(distancia_manhattan(estado), nodo_inicial)]

    while F:
      _, nodo = heapq.heappop(F)
      if nodo.estado == OBJETIVO:
            caminho = []
            while nodo.pai:
                caminho.append(nodo.acao)
                nodo = nodo.pai
            print(f"Expandidos: {expandidos}")
            return list(reversed(caminho))

      if nodo.estado not in X:
        # insere v em x
        X.add(nodo.estado)
        # cria nodo para cada u vizinho de v e insere em F (se ainda nao esta em x)

        expandidos += 1
        for filho in expande(nodo):
          if filho.estado not in X:
              custo_total = filho.custo + distancia_manhattan(filho.estado)
              heapq.heappush(F, (filho.custo + custo_total, filho))

    # se nao ha solucao
    print(f"Expandidos: {expandidos}")
    return None

#opcional,extra
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    # raise NotImplementedError

    OBJETIVO = "12345678_"

    # fila de nodos
    F = []

    # conjunto de nodos explorados
    X = set()

    # cria nodo inicial e adiciona a fila
    nodo_inicial = Nodo(estado)
    F.append(nodo_inicial)

    # enquanto a fila nao estiver vazia
    while F:
        # retira o primeiro nodo da fila
        nodo = F.pop(0)
        # se o nodo for o objetivo, retorna a solucao
        if nodo.estado == OBJETIVO:
            caminho = []
            while nodo.pai:
                caminho.append(nodo.acao)
                nodo = nodo.pai
            return list(reversed(caminho))

        # se o nodo nao estiver explorado
        if nodo.estado not in X:
            # adiciona o nodo
            X.add(nodo.estado)
            # para cada filho do nodo
            for filho in expande(nodo):
                # se o filho nao estiver na fila e nao estiver explorado
                if filho.estado not in X and filho not in F:
                    # adiciona o filho a fila
                    F.append(filho)

    return None

#opcional,extra
def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    # raise NotImplementedError

    OBJETIVO = "12345678_"

    # pilha de nodos
    F = []

    # conjunto de nodos explorados
    X = set()

    # cria nodo inicial e adiciona a fila
    nodo_inicial = Nodo(estado)
    F.append(nodo_inicial)

    # enquanto a fila nao estiver vazia
    while F:
        # retira o ultimo nodo da fila
        nodo = F.pop()
        # se o nodo for o objetivo, retorna o caminho
        if nodo.estado == OBJETIVO:
            caminho = []
            while nodo.pai:
                caminho.append(nodo.acao)
                nodo = nodo.pai
            return list(reversed(caminho))

        # se o nodo nao estiver explorado
        if nodo.estado not in X:
            # adiciona o nodo
            X.add(nodo.estado)
            # para cada filho do nodo
            for filho in expande(nodo):
                # se o filho nao estiver na fila e nao estiver explorado
                if filho.estado not in X and filho not in F:
                    # adiciona o filho a fila
                    F.append(filho)

    return None

def new_heuristic(estado:str)->int:
  """
  Calcula a distancia a partir de uma nova heuristica: média entre a distância de manhattan e distância de hamming.
  """

  distancia = floor((distancia_manhattan(estado)+distancia_hamming(estado))/2)
  # substituir a linha abaixo pelo seu codigo
  return distancia

#opcional,extra
def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """

    OBJETIVO = "12345678_"
    expandidos = 0

    # caso o estado recebido ja seja a solucao, retorna lista vazia
    if estado == OBJETIVO:
        return []


    # conjunto de nodos explorados
    X = set()

    nodo_inicial = Nodo(estado)
    # fila de prioridades para a fronteira
    F = [(distancia_manhattan(estado), nodo_inicial)]

    while F:
      _, nodo = heapq.heappop(F)
      if nodo.estado == OBJETIVO:
            caminho = []
            while nodo.pai:
                caminho.append(nodo.acao)
                nodo = nodo.pai
            print(f"Expandidos: {expandidos}")
            return list(reversed(caminho))

      if nodo.estado not in X:
        # insere v em x
        X.add(nodo.estado)
        # cria nodo para cada u vizinho de v e insere em F (se ainda nao esta em x)

        expandidos += 1
        for filho in expande(nodo):
          if filho.estado not in X:
              custo_total = filho.custo + new_heuristic(filho.estado)
              heapq.heappush(F, (filho.custo + custo_total, filho))

    # se nao ha solucao
    print(f"Expandidos: {expandidos}")
    return None
