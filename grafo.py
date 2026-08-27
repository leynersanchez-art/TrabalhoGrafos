class GrafoRegiao:
    def __init__(self):
        self.num_pokemons = 0
        self.num_treinadores = 0
        self.num_itens = 0
        self.soma_pesos = 0

    def adicionar_caminho(self, origem, destino, tempo_percurso):
        if origem not in self.adjacencias:
            self.adjacencias[origem] = []
        if destino not in self.adjacencias:
            self.adjacencias[destino] = []
        
        self.adjacencias[origem].append((destino, tempo_percurso))
        self.adjacencias[destino].append((origem, tempo_percurso))
        
        self.soma_pesos += tempo_percurso

    def carregar_mapa_arquivo(self, caminho_arquivo):
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
            
            quantidades = linhas[0].strip().split()
            self.num_pokemons = int(quantidades[0])
            self.num_treinadores = int(quantidades[1])
            self.num_itens = int(quantidades[2])
            
            for linha in linhas[1:]:
                dados = linha.strip().split()
                if len(dados) == 3:
                    origem = dados[0]
                    destino = dados[1]
                    tempo = int(dados[2])
                    self.adicionar_caminho(origem, destino, tempo)
