from entidades import Pokemon, Treinador
from grafo import Grafo

def main():
    mapa = Grafo()
    mapa.carregar_mapa_arquivo("Aqui o caminho do seu arquivo")

    treinador = Treinador("Ash")
    print("Iniciando a Jornada pokemon: ")

if __name__ == "__main__":
    main()
