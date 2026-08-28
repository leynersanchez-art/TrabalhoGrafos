import random
from grafo import GrafoRegiao
from entidades import Pokemon, Item, Treinador, LiderGinasio, EquipeRocket

def espalhar_entidades_no_mapa(mapa):
    cidades = list(mapa.adjacencias.keys())
    # Cria o "inventário de chão" de cada cidade garantindo que o mapa possa suportar itens e NPCs simultâneos
    conteudo_cidades = {cidade: {'pokemons': [], 'itens': [], 'lider': None} for cidade in cidades}
    
    # A localização inicial das entidades é determinada pelo acaso usando as quantidades lidas do cabeçalho do arquivo texto
    for _ in range(mapa.num_pokemons):
        conteudo_cidades[random.choice(cidades)]['pokemons'].append(Pokemon())
        
    for _ in range(mapa.num_itens):
        conteudo_cidades[random.choice(cidades)]['itens'].append(Item())
        
    # Sorteia vértices distintos para os Líderes, limitando ao total de cidades disponíveis no mapa para evitar crash
    nomes_lideres = ["Brock", "Misty", "Surge", "Erika", "Koga", "Sabrina", "Blaine", "Giovanni"]
    
    # Descobre se o mapa tem 8 cidades ou menos, e pega o menor número
    num_lideres_possiveis = min(8, len(cidades)) 
    cidades_ginasio = random.sample(cidades, num_lideres_possiveis) 
    
    for i in range(num_lideres_possiveis):
        cidade_escolhida = cidades_ginasio[i]
        conteudo_cidades[cidade_escolhida]['lider'] = LiderGinasio(nomes_lideres[i])
        
    # O retorno é obrigatório para evitar o erro 'NoneType'
    return conteudo_cidades

def main():
    mapa = GrafoRegiao()
    mapa.carregar_mapa_arquivo("mapa.txt")
    mundo = espalhar_entidades_no_mapa(mapa)
    
    jogador = Treinador(nome="Ash", local_atual="Pallet")
    jogador.receber_kit_inicial()
    
    # Inicializa a Equipe Rocket em uma cidade aleatória do mapa
    cidades_mapa = list(mapa.adjacencias.keys())
    rocket = EquipeRocket(random.choice(cidades_mapa))
    
    while True:
        # Movimentação autônoma da Equipe Rocket (um vértice por vez)
        vizinhos_rocket = [cidade for cidade, tempo in mapa.adjacencias[rocket.local_atual]]
        if vizinhos_rocket:
            rocket.local_atual = random.choice(vizinhos_rocket)
            
        jogador.exibir_status()
        
        # Checa se o jogador e a Equipe Rocket se esbarraram na mesma cidade
        if jogador.local_atual == rocket.local_atual:
            jogador.enfrentar_rocket(rocket, mapa)
        
        print("📍 CIDADES VIZINHAS:")
        for cidade, tempo in mapa.adjacencias[jogador.local_atual]:
            print(f" - {cidade} (Leva {tempo})")
            
        print("\n🎮 OPÇÕES:")
        print("1. Viajar para outra cidade")
        print("2. Explorar local atual (Ginásio/Itens/Batalha)")
        print("3. GPS: Caminho para o Centro Médico")
        print("4. Sair do jogo")
        
        comando = input("Escolha uma opção: ").strip()
        
        if comando == '4':
            print("Salvando e saindo do jogo...")
            break
            
        elif comando == '1':
            destino = input("Para qual cidade deseja ir? ").strip()
            jogador.mover(mapa, destino)
            
        elif comando == '3':
            pmcs = [cidade for cidade in mapa.adjacencias.keys() if "Centro_Medico" in cidade]
            if not pmcs:
                print("❌ Não há Centros Médicos cadastrados neste mapa!")
            else:
                pmc_prox, tempo_total, rota = mapa.calcular_caminho_minimo(jogador.local_atual, pmcs)
                if pmc_prox:
                    print(f"\n🚑 ROTA DE EMERGÊNCIA:")
                    print(f"Destino: {pmc_prox} | Tempo total: {tempo_total}")
                    print(f"Caminho: {' -> '.join(rota)}")
                else:
                    print("❌ Caminho bloqueado ou inexistente!")
                    
        elif comando == '2':
            print(f"\n🔍 Explorando {jogador.local_atual}...")
            
            lider = mundo[jogador.local_atual]['lider']
            if lider and not lider.derrotado:
                jogador.desafiar_lider(lider)
            else:
                itens_no_local = mundo[jogador.local_atual]['itens']
                if itens_no_local:
                    for item in itens_no_local:
                        jogador.pegar_item(item)
                    mundo[jogador.local_atual]['itens'] = []
                
                pokemons_no_local = mundo[jogador.local_atual]['pokemons']
                if pokemons_no_local:
                    p_selvagem = pokemons_no_local[0]
                    jogador.batalhar(p_selvagem)
                    mundo[jogador.local_atual]['pokemons'].pop(0)
                
                if not itens_no_local and not pokemons_no_local and not lider:
                    print("💨 A área está completamente vazia.")

if __name__ == "__main__":
    main()
