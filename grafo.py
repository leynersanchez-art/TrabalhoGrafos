class GrafoRegiao:
    def __init__(self):
        # A estrutura base do mapa precisa ser feita na mão com dicionários, já que o projeto proíbe bibliotecas prontas como NetworkX
        self.adjacencias = {}
        self.num_pokemons = 0
        self.num_treinadores = 0
        self.num_itens = 0
        self.soma_pesos = 0

    def adicionar_caminho(self, origem, destino, tempo_percurso):
        # Inicializa a cidade no dicionário caso seja a primeira vez que ela aparece no arquivo
        if origem not in self.adjacencias:
            self.adjacencias[origem] = []
        if destino not in self.adjacencias:
            self.adjacencias[destino] = []
        
        # Como as rotas permitem ida e volta, adicionamos o caminho para os dois lados da rua
        self.adjacencias[origem].append((destino, tempo_percurso))
        self.adjacencias[destino].append((origem, tempo_percurso))
        
        self.soma_pesos += tempo_percurso

    def carregar_mapa_arquivo(self, caminho_arquivo):
        # Lê o txt original ignorando problemas de formatação de caracteres regionais (utf-8)
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            
            # A primeira linha dita exatamente quanto de cada entidade a gente vai espalhar aleatoriamente depois
            quantidades = linhas[0].strip().split()
            self.num_pokemons = int(quantidades[0])
            self.num_treinadores = int(quantidades[1])
            self.num_itens = int(quantidades[2])
            
            # Da segunda linha para baixo é apenas a estrutura de conexões e distâncias do mapa
            for linha in linhas[1:]:
                dados = linha.strip().split()
                if len(dados) == 3:
                    origem = dados[0]
                    destino = dados[1]
                    tempo = int(dados[2])
                    self.adicionar_caminho(origem, destino, tempo)

    def calcular_caminho_minimo(self, origem, destinos_alvo):
        # Implementação manual do Algoritmo de Dijkstra para encontrar a rota de emergência mais rápida para o hospital
        distancias = {vertice: float('inf') for vertice in self.adjacencias}
        distancias[origem] = 0
        visitados = set()
        caminho_anterior = {vertice: None for vertice in self.adjacencias}

        # O laço roda até avaliarmos o peso de todas as cidades conectadas no mapa
        while len(visitados) < len(self.adjacencias):
            vertice_atual = None
            menor_dist = float('inf')
            for v in self.adjacencias:
                if v not in visitados and distancias[v] < menor_dist:
                    menor_dist = distancias[v]
                    vertice_atual = v
            
            if vertice_atual is None:
                break
                
            visitados.add(vertice_atual)
            
            # Compara se a nova rota somada é mais rápida do que a rota que conhecíamos antes
            for vizinho, tempo in self.adjacencias[vertice_atual]:
                nova_dist = distancias[vertice_atual] + tempo
                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    caminho_anterior[vizinho] = vertice_atual
                    
        # Filtra entre as opções de destino (ex: vários PMCs no mapa) qual está com o menor tempo total acumulado
        destino_mais_proximo = None
        menor_dist_final = float('inf')
        
        for alvo in destinos_alvo:
            if alvo in distancias and distancias[alvo] < menor_dist_final:
                menor_dist_final = distancias[alvo]
                destino_mais_proximo = alvo
                
        # Faz o rastreio reverso montando a lista de cidades pelas quais o jogador terá que passar
        rota = []
        atual = destino_mais_proximo
        while atual is not None:
            rota.insert(0, atual)
            atual = caminho_anterior[atual]
            
        return destino_mais_proximo, menor_dist_final, rota

    def calcular_prazo_inscricao(self):
        # Define os limites de tempo do jogo para evitar que o jogador fique farmando xp infinitamente sem penalidade
        prazo_min = 10 * self.soma_pesos
        prazo_max = 15 * self.soma_pesos
        return prazo_min, prazo_max
