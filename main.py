import random
from grafo import GrafoRegiao
from entidades import Pokemon, Item, Treinador, LiderGinasio, EquipeRocket, TreinadorNPC

def espalhar_entidades_no_mapa(mapa):
    cidades = list(mapa.adjacencias.keys())
    # Cria o "inventário de chão" de c2ada cidade garantindo que o mapa possa suportar itens e NPCs simultâneos
    conteudo_cidades = {cidade: {'pokemons': [], 'itens': [], 'lider': None, 'treinadores': []} for cidade in cidades}
    
    # A localização inicial das entidades é determinada pelo acaso usando as quantidades lidas do cabeçalho do arquivo texto
    for _ in range(mapa.num_pokemons):
        conteudo_cidades[random.choice(cidades)]['pokemons'].append(Pokemon())
        
    for _ in range(mapa.num_itens):
        conteudo_cidades[random.choice(cidades)]['itens'].append(Item())
        
    # Sorteia vértices distintos para os Líderes, limitando ao total de cidades disponíveis no mapa para evitar crash
    nomes_lideres = ["Brock", "Misty", "Surge", "Erika", "Koga", "Sabrina", "Blaine", "Giovanni"]
    
    # Cidades especiais (laboratório, centro médico) não fazem sentido temático como sede de ginásio
    cidades_elegiveis = [c for c in cidades if "Lab_Carvalho" not in c and "Centro_Medico" not in c]

    # Descobre se o mapa tem 8 cidades elegíveis ou menos, e pega o menor número
    num_lideres_possiveis = min(8, len(cidades_elegiveis))
    cidades_ginasio = random.sample(cidades_elegiveis, num_lideres_possiveis)
    
    for i in range(num_lideres_possiveis):
        cidade_escolhida = cidades_ginasio[i]
        conteudo_cidades[cidade_escolhida]['lider'] = LiderGinasio(nomes_lideres[i])
        
    # Espalha treinadores NPC pelo mapa, usando a quantidade lida do cabeçalho do arquivo txt
    nomes_npc = ["Joey", "Cheryl", "Mikey", "Vance", "Bianca", "Calvin", "Wade", "Aaron", "Piper", "Todd"]
    treinadores_npc = []
    for i in range(mapa.num_treinadores):
        nome_npc = nomes_npc[i % len(nomes_npc)]
        cidade_npc = random.choice(cidades)
        npc = TreinadorNPC(nome_npc, cidade_npc)
        treinadores_npc.append(npc)
        conteudo_cidades[cidade_npc].setdefault('treinadores', []).append(npc)

    # O retorno é obrigatório para evitar o erro 'NoneType'
    return conteudo_cidades, treinadores_npc

def main():
    mapa = GrafoRegiao()
    mapa.carregar_mapa_arquivo("mapa.txt")
    mundo, treinadores_npc = espalhar_entidades_no_mapa(mapa)

    
    jogador = Treinador(nome="Ash", local_atual="Pallet")
    jogador.receber_kit_inicial()
    
    # Inicializa a Equipe Rocket em uma cidade aleatória do mapa
    cidades_mapa = list(mapa.adjacencias.keys())
    rocket = EquipeRocket(random.choice(cidades_mapa))
    
    while True:
        # A Equipe Rocket só se move e pode ser encontrada enquanto estiver visível
        if rocket.visivel:
            vizinhos_rocket = [cidade for cidade, tempo in mapa.adjacencias[rocket.local_atual]]
            if vizinhos_rocket:
                rocket.local_atual = random.choice(vizinhos_rocket)
        elif jogador.distancia_percorrida >= rocket.distancia_para_reaparecer:
            rocket.visivel = True
            rocket.distancia_para_reaparecer = None
            rocket.local_atual = random.choice(cidades_mapa)
            print(f"\n👀 Rumores indicam que a Equipe Rocket reapareceu em {rocket.local_atual}!")

        jogador.exibir_status()

        # Checa se o jogador e a Equipe Rocket se esbarraram na mesma cidade (só é possível se ela estiver visível)
        if rocket.visivel and jogador.local_atual == rocket.local_atual:
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
            npcs_no_local = mundo[jogador.local_atual].get('treinadores', [])
            npc_disponivel = next((n for n in npcs_no_local if not n.derrotado_hoje), None)
            itens_no_local = mundo[jogador.local_atual]['itens']
            pokemons_no_local = mundo[jogador.local_atual]['pokemons']

            # Monta a lista do que existe na cidade agora, sem deixar nada "escondido" atrás de outra entidade
            opcoes_locais = []
            if lider and not lider.derrotado:
                opcoes_locais.append(('lider', f"Desafiar o Líder de Ginásio {lider.nome}"))
            if npc_disponivel:
                opcoes_locais.append(('npc', f"Desafiar o treinador {npc_disponivel.nome}"))
            if itens_no_local:
                opcoes_locais.append(('itens', f"Pegar itens ({len(itens_no_local)} disponíveis)"))
            if pokemons_no_local:
                opcoes_locais.append(('pokemon', f"Batalhar contra pokémon selvagem ({pokemons_no_local[0].tipo})"))

            if not opcoes_locais:
                print("💨 A área está completamente vazia.")
            else:
                print("\nO que você encontrou aqui:")
                for i, (_, descricao) in enumerate(opcoes_locais):
                    print(f"  {i+1}. {descricao}")
                escolha = input("O que deseja fazer? (número): ").strip()

                if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes_locais):
                    tipo_escolhido, _ = opcoes_locais[int(escolha) - 1]

                    if tipo_escolhido == 'lider':
                        jogador.desafiar_lider(lider)
                    elif tipo_escolhido == 'npc':
                        venceu = jogador.desafiar_treinador(npc_disponivel)
                        if venceu:
                            npc_disponivel.derrotado_hoje = True
                    elif tipo_escolhido == 'itens':
                        for item in itens_no_local:
                            jogador.pegar_item(item)
                        mundo[jogador.local_atual]['itens'] = []
                    elif tipo_escolhido == 'pokemon':
                        p_selvagem = pokemons_no_local[0]
                        jogador.batalhar(p_selvagem)
                        mundo[jogador.local_atual]['pokemons'].pop(0)
                else:
                    print("❌ Escolha inválida.")

if __name__ == "__main__":
    main()
