import random

TIPOS_POKEMON = ["Água", "Fogo", "Planta", "Elétrico", "Fantasma", "Venenoso", "Gelo"]

class Pokemon:
    def __init__(self):
        self.tipo = random.choice(TIPOS_POKEMON)
        # O HP inicial deve ser sempre 100, configurando o teto máximo de saúde para as curas
        self.hp = 100 
        self.xp = 0
        # Pontos de Ataque (AP) e Defesa (DP) gerados aleatoriamente para garantir variação de força entre os Pokemons
        self.ap = random.randint(10, 50) 
        self.dp = random.randint(10, 50)
        # O limite imposto pelo projeto para a progressão do pokémon é de 3 fases evolutivas
        self.fase_evolucao = 1 

    def __str__(self):
        return f"Pkmn {self.tipo} (HP:{self.hp} XP:{self.xp} AP:{self.ap} DP:{self.dp})"

class Item:
    def __init__(self):
        self.tipo = random.choice(["Ovo", "Erva Medicinal", "Pokebola"])
        
    def __str__(self):
        return f"{self.tipo}"

class LiderGinasio:
    def __init__(self, nome):
        self.nome = nome
        self.derrotado = False
        # Para representar um desafio de alto nível que exige preparo, a equipe do líder recebe um bônus de 20 pontos nos atributos
        self.xp = random.randint(50, 120)
        self.equipe = [Pokemon(), Pokemon(), Pokemon()]

class TreinadorNPC:
    def __init__(self, nome, local_atual):
        self.nome = nome
        self.local_atual = local_atual
        self.xp = random.randint(0, 50)
        self.derrotado_hoje = False
        self.derrotado = False  # necessário para reaproveitar desafiar_lider() provisoriamente
        # NPCs comuns têm equipes menores e mais fracas que líderes de ginásio
        self.equipe = [Pokemon(), Pokemon(), Pokemon()]

class Treinador:
    def __init__(self, nome, local_atual):
        self.nome = nome
        self.local_atual = local_atual
        self.xp = 0
        self.distancia_percorrida = 0
        # A equipe de combate ativa é rigorosamente limitada a um máximo de 6 pokémons simultâneos
        self.pokemons_ativos = [] 
        self.pokemons_incubadora = [] 
        # Pokémons excedentes (capturados com a equipe já cheia) ficam sob estudo do Prof. Carvalho
        self.pokemons_carvalho = []
        # O objetivo central é acumular 8 insígnias derrotando líderes para validar a inscrição na Liga
        self.insignias = 0 
        self.inventario = []

    def receber_kit_inicial(self):
        # O jogador já começa com os 3 tipos iniciais distintos para ter vantagem tática contra diferentes selvagens
        p_agua, p_fogo, p_planta = Pokemon(), Pokemon(), Pokemon()
        p_agua.tipo, p_fogo.tipo, p_planta.tipo = "Água", "Fogo", "Planta"
        self.pokemons_ativos.extend([p_agua, p_fogo, p_planta])
        
        self.inventario.append("Encubadora")
        for _ in range(7):
            self.inventario.append("Pokebola")
            
    def exibir_status(self):
        print(f"\n=== STATUS DO TREINADOR {self.nome.upper()} ===")
        print(f"📍 Local Atual: {self.local_atual}")
        print(f"⭐ XP: {self.xp} | 🏅 Insígnias: {self.insignias}")
        print("🐾 Pokémons Ativos:")
        for i, p in enumerate(self.pokemons_ativos):
            print(f"  {i+1}. {p}")
        print(f"🎒 Inventário: {self.inventario}")
        print("===================================\n")

    def mover(self, mapa, destino):
        # A movimentação é restrita a vértices adjacentes diretos para impedir saltos irreais no mapa
        vizinhos = {cidade: tempo for cidade, tempo in mapa.adjacencias[self.local_atual]}
        
        if destino in vizinhos:
            tempo_gasto = vizinhos[destino]
            self.local_atual = destino
            self.distancia_percorrida += tempo_gasto
            print(f"\n🚶 Você viajou para {destino} e percorreu {tempo_gasto} de distância.")
            
            # A recuperação de HP ocorre à taxa de 1 unidade por 10 de distância viajada
            recuperacao_hp = tempo_gasto // 10
            # O ganho passivo de experiência exige 100 de distância para render 1 único XP
            ganho_xp = tempo_gasto // 100 
            
            for p in self.pokemons_ativos:
                # Pokémons com HP inferior a 20 são considerados desmaiados e o projeto proíbe a cura passiva deles
                if p.hp >= 20: 
                    p.hp = min(100, p.hp + recuperacao_hp) 
                
                p.xp += ganho_xp
                
                # Atingir 1000 XP aciona a evolução, melhorando os atributos, desde que não ultrapasse a 3ª e última fase
                if p.xp >= 1000 and p.fase_evolucao < 3:
                    p.fase_evolucao += 1
                    p.xp = 0 
                    # Conforme o enunciado: AP e DP são acrescidos de 30% em relação à forma anterior (multiplicativo, não fixo)
                    ap_antigo, dp_antigo = p.ap, p.dp
                    p.ap = round(p.ap * 1.3)
                    p.dp = round(p.dp * 1.3)
                    print(f"🌟 INCRÍVEL! Seu Pokémon {p.tipo} evoluiu para a FASE {p.fase_evolucao}! (AP: {ap_antigo}→{p.ap}, DP: {dp_antigo}→{p.dp})")

            ovos_prontos = []
            for ovo in self.pokemons_incubadora:
                ovo["distancia_restante"] -= tempo_gasto
                # O ovo choca automaticamente após deduzir 100 unidades de distância de viagem do jogador
                if ovo["distancia_restante"] <= 0:
                    ovos_prontos.append(ovo)
            
            for ovo in ovos_prontos:
                self.pokemons_incubadora.remove(ovo)
                # O recém-nascido só integra a equipe se houver vaga no limite estrutural de 6 pokémons
                if len(self.pokemons_ativos) < 6:
                    novo_pokemon = Pokemon()
                    self.pokemons_ativos.append(novo_pokemon)
                    print(f"🎉 CHOCOU! Um {novo_pokemon.tipo} nasceu e entrou pra equipe!")
                else:
                    print("🎉 O ovo chocou, mas você já carrega 6 Pokémons. O recém-nascido foi enviado pro Professor Carvalho.")
        else:
            print(f"\n❌ {destino} é longe demais. Você só pode viajar para cidades vizinhas.")

    def pegar_item(self, item):
        if item.tipo == "Pokebola":
            self.inventario.append("Pokebola")
            print("🎒 Você encontrou e guardou uma Pokébola!")
            
        elif item.tipo == "Erva Medicinal":
            print("🌿 Preparando poção com a Erva Medicinal...")
            # A erva medicinal restaura 10 HPs exclusivamente de pokémons que ainda estão conscientes na party
            for p in self.pokemons_ativos:
                if p.hp >= 20:
                    p.hp = min(100, p.hp + 10)
            print("✨ Todos os pokémons conscientes recuperaram 10 de HP!")
            
        elif item.tipo == "Ovo":
            # A coleta do ovo é bloqueada se o jogador não tiver encubadora ou se o limite global (ativos + ovos) atingir 7
            total = len(self.pokemons_ativos) + len(self.pokemons_incubadora)
            if total < 7 and "Encubadora" in self.inventario:
                # O treinador pode optar por não pegar o ovo; uma vez aceito, não pode mais abandoná-lo
                pegar = input("🥚 Você encontrou um Ovo! Deseja pegá-lo? (s/n): ").strip().lower()
                if pegar == 's':
                    self.pokemons_incubadora.append({"distancia_restante": 100})
                    print("🥚 Ovo guardado na Encubadora! Faltam 100 de distância pra ele chocar.")
                else:
                    print("🥚 Você decidiu deixar o Ovo para trás.")
            else:
                print("🥚 Achou um Ovo, mas sua equipe tá lotada ou falta a encubadora.")

    def batalhar(self, p_selvagem):
        print(f"\n⚔️ UM POKÉMON SELVAGEM APARECEU: {p_selvagem.tipo} (HP:{p_selvagem.hp} AP:{p_selvagem.ap} DP:{p_selvagem.dp})!")
        
        # A batalha exige ao menos um pokémon na equipe com HP 20 ou superior para iniciar a trocação
        p_aliado = next((p for p in self.pokemons_ativos if p.hp >= 20), None)
        
        if not p_aliado:
            print("❌ Sua equipe inteira caiu. Você foge da batalha!")
            return False
            
        print(f"👉 Vai, {p_aliado.tipo}! (AP:{p_aliado.ap} DP:{p_aliado.dp})")
        
        # A métrica de dano do projeto é crua: subtrai a Defesa do alvo do Ataque de quem desfere o golpe
        dano_no_selvagem = max(0, p_aliado.ap - p_selvagem.dp)
        dano_no_aliado = max(0, p_selvagem.ap - p_aliado.dp)
        
        p_selvagem.hp -= dano_no_selvagem
        print(f"💥 {p_aliado.tipo} atacou causando {dano_no_selvagem} de dano!")
        
        if p_selvagem.hp > 0:
            p_aliado.hp -= dano_no_aliado
            print(f"💥 O selvagem revidou causando {dano_no_aliado} de dano!")
            
        if p_aliado.hp < 20:
            print(f"💀 Seu {p_aliado.tipo} foi nocauteado!")
            # A derrota rende um bônus mínimo de consolação de 3 XP conforme as regras
            p_aliado.xp += 3 
            return False
        else:
            print(f"🏆 Vitória!")
            # A vitória em combate garante um ganho de 10 XP para o pokémon lutador e para o treinador
            p_aliado.xp += 10 
            self.xp += 10
            
            # A captura é validada apenas pela posse de pokébola — o enunciado permite capturar mesmo com a equipe cheia,
            # bastando escolher depois quais 6 pokémons permanecem ativos
            if "Pokebola" in self.inventario:
                capturar = input(f"Tentar capturar esse {p_selvagem.tipo}? (s/n): ").strip().lower()
                if capturar == 's':
                        self.inventario.remove("Pokebola")
                        p_selvagem.hp = 100 # Pokémons recém-capturados têm a vida totalmente restaurada
                        self.pokemons_ativos.append(p_selvagem)

                        # Bônus de captura: +3 XP extra para o treinador e para os pokémons envolvidos na batalha
                        self.xp += 3
                        p_aliado.xp += 3
                        p_selvagem.xp += 3
                        print(f"✨ Sucesso! {p_selvagem.tipo} tá no time agora. (+3 XP de bônus de captura)")

                        if len(self.pokemons_ativos) > 6:
                            self._enviar_excedente_para_carvalho()
                        return True
        return False


        def _enviar_excedente_para_carvalho(self):
            # Sempre que a equipe ultrapassa 6, o treinador escolhe quem fica; o resto vai pro laboratório
            print("\n📦 Sua equipe ultrapassou 6 pokémons! Escolha quais 6 permanecem com você.")
            for i, p in enumerate(self.pokemons_ativos):
                print(f"  {i+1}. {p}")

            escolhidos = []
            while len(escolhidos) < 6:
                escolha = input(f"Escolha o pokémon {len(escolhidos)+1}/6 (número): ").strip()
                if escolha.isdigit() and 1 <= int(escolha) <= len(self.pokemons_ativos):
                    idx = int(escolha) - 1
                    pokemon = self.pokemons_ativos[idx]
                    if pokemon not in escolhidos:
                        escolhidos.append(pokemon)
                    else:
                        print("❌ Esse pokémon já foi escolhido.")
                else:
                    print("❌ Escolha inválida.")

            excedente = [p for p in self.pokemons_ativos if p not in escolhidos]
            self.pokemons_ativos = escolhidos
            self.pokemons_carvalho.extend(excedente)
            print(f"📮 {len(excedente)} pokémon(s) foram enviados para estudo do Professor Carvalho.")

    def desafiar_treinador(self, oponente, chance_aceitar=1.0, mostrar_desafio=True):
        """
        Batalha 3v3 contra outro treinador (NPC, líder de ginásio, etc).
        'oponente' precisa ter: nome, equipe (lista de Pokemon) e, opcionalmente, xp.
        Retorna True se quem chamou o método (self) venceu; False em qualquer outro caso (perda, recusa, empate).
        """
        if mostrar_desafio:
            print(f"\n⚔️ {self.nome} DESAFIA {oponente.nome} PARA UMA BATALHA!")

        if random.random() > chance_aceitar:
            print(f"🚫 {oponente.nome} recusou o desafio.")
            return False

        meus_conscientes = [p for p in self.pokemons_ativos if p.hp >= 20]
        seus_conscientes = [p for p in oponente.equipe if p.hp >= 20]

        if len(meus_conscientes) < 3:
            print("❌ Você precisa de ao menos 3 pokémons conscientes para desafiar um treinador!")
            return False
        if not seus_conscientes:
            print(f"❌ {oponente.nome} não tem pokémons em condição de lutar.")
            return False

        print("\nEscolha 3 pokémons para a batalha:")
        for i, p in enumerate(meus_conscientes):
            print(f"  {i+1}. {p}")

        time_desafiante = []
        indices_usados = set()
        while len(time_desafiante) < 3:
            escolha = input(f"Pokémon {len(time_desafiante)+1}/3 (número): ").strip()
            if escolha.isdigit() and int(escolha) not in indices_usados and 1 <= int(escolha) <= len(meus_conscientes):
                indices_usados.add(int(escolha))
                time_desafiante.append(meus_conscientes[int(escolha) - 1])
            else:
                print("❌ Escolha inválida, tente novamente.")

        time_oponente = seus_conscientes[:3]

        ativo_desafiante = time_desafiante[0]
        ativo_oponente = time_oponente[0]
        xp_oponente_treinador = getattr(oponente, 'xp', 0)

        # O treinador desafiado começa atacando
        turno_do_desafiante = False
        turnos = 0
        MAX_TURNOS = 200  # rede de segurança contra loop infinito caso nenhum lado consiga causar dano

        while time_desafiante and time_oponente and turnos < MAX_TURNOS:
            turnos += 1

            if turno_do_desafiante:
                atacante, bonus_atacante = ativo_desafiante, self.xp
                defensor, bonus_defensor = ativo_oponente, xp_oponente_treinador
            else:
                atacante, bonus_atacante = ativo_oponente, xp_oponente_treinador
                defensor, bonus_defensor = ativo_desafiante, self.xp

            # Cada pokémon recebe AP/DP a mais equivalente ao XP do seu treinador durante a disputa
            ap_efetivo = atacante.ap + bonus_atacante
            dp_efetivo = defensor.dp + bonus_defensor

            diferenca_xp = abs(atacante.xp - defensor.xp)
            # Probabilidades proporcionais à diferença de XP; teto de 90% para nunca serem garantia absoluta
            chance_esquiva = min(0.9, diferenca_xp / 1000)
            chance_critico = min(0.9, diferenca_xp / 1000)

            if random.random() < chance_esquiva:
                print(f"💨 {defensor.tipo} esquivou do ataque de {atacante.tipo}!")
            else:
                dano = max(0, ap_efetivo - dp_efetivo)
                if dano > 0 and random.random() < chance_critico:
                    dano *= 2
                    print("🎯 ATAQUE CRÍTICO!")
                defensor.hp -= dano
                print(f"💥 {atacante.tipo} atacou {defensor.tipo} causando {dano} de dano! (HP restante: {max(0, defensor.hp)})")

            if defensor.hp < 20:
                print(f"💀 {defensor.tipo} desmaiou!")
                if defensor is ativo_desafiante:
                    time_desafiante.remove(ativo_desafiante)
                    if time_desafiante:
                        if len(time_desafiante) > 1:
                            print("Escolha o próximo pokémon:")
                            for i, p in enumerate(time_desafiante):
                                print(f"  {i+1}. {p}")
                            prox = input("Número do pokémon: ").strip()
                            if prox.isdigit() and 1 <= int(prox) <= len(time_desafiante):
                                ativo_desafiante = time_desafiante[int(prox) - 1]
                            else:
                                ativo_desafiante = time_desafiante[0]
                        else:
                            ativo_desafiante = time_desafiante[0]
                else:
                    time_oponente.remove(ativo_oponente)
                    if time_oponente:
                        ativo_oponente = time_oponente[0]

            turno_do_desafiante = not turno_do_desafiante

        # Cada batalha consome o equivalente a 1 unidade de tempo/distância percorrida
        self.distancia_percorrida += 1

        if time_desafiante and not time_oponente:
            vitoria = True
        elif time_oponente and not time_desafiante:
            vitoria = False
        else:
            # Limite de turnos atingido sem um vencedor claro (raro, mas possível)
            print("\n⏱️ A batalha se arrastou demais e terminou em impasse. Ambos os lados recuam.")
            return False

        if vitoria:
            print(f"\n🏆 {self.nome} VENCEU A BATALHA CONTRA {oponente.nome}!")
            self.xp += 3 if self.xp >= xp_oponente_treinador else 1
        else:
            print(f"\n💀 {self.nome} PERDEU A BATALHA CONTRA {oponente.nome}!")

        return vitoria

    def desafiar_lider(self, lider):
        if lider.derrotado:
            print(f"🏅 Você já derrotou {lider.nome}.")
            return False

        venceu = self.desafiar_treinador(lider, chance_aceitar=1.0)
        if venceu:
            lider.derrotado = True
            self.insignias += 1
            print(f"🏅 Você recebeu a insígnia de {lider.nome}! Total: {self.insignias}/8")
        return venceu
        
class EquipeRocket:
    def __init__(self, local_inicial):
        self.local_atual = local_inicial
        # A Equipe Rocket carrega Pokémons mais fortes para dificultar a exploração
        self.equipe = [Pokemon(), Pokemon()]
        for p in self.equipe:
            p.ap += 15
            p.dp += 15
