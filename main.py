from grafo import GrafoRegiao

def main():
    mapa = GrafoRegiao()
    
    print("--- DADOS DA REGIÃO ---")
    print(f"Pokémons espalhados: {mapa.num_pokemons}")
    print(f"Treinadores espalhados: {mapa.num_treinadores}")
    print(f"Itens extras: {mapa.num_itens}")
    
    prazo_min = 10 * mapa.soma_pesos
    prazo_max = 15 * mapa.soma_pesos
    print(f"Prazo para a Liga Pokémon: entre {prazo_min} e {prazo_max} unidades de tempo")
    
    print("\n--- ROTAS DO MAPA (LISTA DE ADJACÊNCIA) ---")
    for local, rotas in mapa.adjacencias.items():
        print(f"{local} se conecta com: {rotas}")

if __name__ == "__main__":
    main()
