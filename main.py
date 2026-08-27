import random
from grafo import GrafoRegiao
from entidades import Pokemon, Item

def espalhar_entidades_no_mapa(mapa):
    cidades = list(mapa.adjacencias.keys())

    conteudo_cidades = {cidade: {'pokemons': [], 'itens': [], 'treinadores': []} for cidade in cidades}
    
    for _ in range(mapa.num_pokemons):
        cidade_aleatoria = random.choice(cidades)
        novo_pokemon = Pokemon()
        conteudo_cidades[cidade_aleatoria]['pokemons'].append(novo_pokemon)
        
    for _ in range(mapa.num_itens):
        cidade_aleatoria = random.choice(cidades)
        novo_item = Item()
        conteudo_cidades[cidade_aleatoria]['itens'].append(novo_item)
        
    return conteudo_cidades

def main():
    mapa = GrafoRegiao()
    mapa.carregar_mapa_arquivo("mapa.txt")
    
    mundo = espalhar_entidades_no_mapa(mapa)
    
    print("--- O QUE TEM EM CADA CIDADE? ---")
    for cidade, conteudo in mundo.items():
        print(f"\n📍 {cidade}:")
        
        for p in conteudo['pokemons']:
            print(f"  - 🐾 {p}")
            
        for i in conteudo['itens']:
            print(f"  - 🎒 {i}")

if __name__ == "__main__":
    main()
