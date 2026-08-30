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
    
    lideres = []
    for i in range(num_lideres_possiveis):
        cidade_escolhida = cidades_ginasio[i]
        lider = LiderGinasio(nomes_lideres[i], cidade_escolhida)
        conteudo_cidades[cidade_escolhida]['lider'] = lider
        lideres.append(lider)

    # A região só exige 8 insígnias se houver mais de 8 líderes cadastrados;
    # caso contrário, a meta é vencer todos os líderes existentes
    meta_insignias = 8 if num_lideres_possiveis > 8 else num_lideres_possiveis
        
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
    return conteudo_cidades, treinadores_npc, lideres, meta_insignias

def main():
    mapa = GrafoRegiao()
    mapa.carregar_mapa_arquivo("mapa.txt")
    mundo, treinadores_npc, lideres, meta_insignias = espalhar_entidades_no_mapa(mapa)

    prazo_min, prazo_max = mapa.calcular_prazo_inscricao()
    prazo_maximo_jogo = random.randint(prazo_min, prazo_max)

    jogador = Treinador(nome="Ash", local_atual="Pallet")
    jogador.meta_insignias = meta_insignias
    jogador.receber_kit_inicial()

    print(f"\n📜 Você tem até {prazo_maximo_jogo} unidades de distância percorrida para se inscrever na Liga Pokémon!")
        
    # Inicializa a Equipe Rocket em uma cidade aleatória do mapa
    cidades_mapa = list(mapa.adjacencias.keys())
    rocket = EquipeRocket(random.choice(cidades_mapa))
    
    while True:
        if jogador.distancia_percorrida > prazo_maximo_jogo and not jogador.inscrito_na_liga:
            print(f"\n⏰ O prazo de {prazo_maximo_jogo} unidades de distância se esgotou! Você não se inscreveu a tempo.")
            print("💀 FIM DE JOGO: você está inapto para a Liga Pokémon, mesmo que tenha conquistado insígnias.")
            break

        # Movimentação de patrulha dos líderes de ginásio (não derrotados) entre as cidades
        for lider in lideres:
            if lider.derrotado:
                continue
            cidade_antiga = lider.local_atual
            lider.mover_um_passo(mapa)
            if lider.local_atual != cidade_antiga:
                mundo[cidade_antiga]['lider'] = None
                mundo[lider.local_atual]['lider'] = lider

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
            print("Saindo do jogo...")
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
            if "Liga_Pokemon" in jogador.local_atual:
                opcoes_locais.append(('liga', "Inscrever-se na Liga Pokémon"))
            if "Centro_Medico" in jogador.local_atual:
                opcoes_locais.append(('pmc', "Tratar pokémons machucados no PMC"))
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

                    if tipo_escolhido == 'liga':
                        venceu_jogo = jogador.tentar_inscricao_liga(prazo_maximo_jogo)
                        if venceu_jogo:
                            return
                    elif tipo_escolhido == 'pmc':
                        jogador.tratar_pokemons_pmc()
                    elif tipo_escolhido == 'lider':
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

