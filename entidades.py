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
        self.equipe = [Pokemon(), Pokemon(), Pokemon()]
        for p in self.equipe:
            p.ap += 20
            p.dp += 20

class Treinador:
    def __init__(self, nome, local_atual):
        self.nome = nome
        self.local_atual = local_atual
        self.xp = 0
        self.distancia_percorrida = 0
        # A equipe de combate ativa é rigorosamente limitada a um máximo de 6 pokémons simultâneos
        self.pokemons_ativos = [] 
        self.pokemons_incubadora = [] 
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
                    p.ap += random.randint(10, 20) 
                    p.dp += random.randint(10, 20) 
                    print(f"🌟 INCRÍVEL! Seu Pokémon {p.tipo} evoluiu para a FASE {p.fase_evolucao}!")

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
                self.pokemons_incubadora.append({"distancia_restante": 100})
                print("🥚 Ovo guardado na Encubadora! Faltam 100 de distância pra ele chocar.")
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
            
            # A tentativa de captura é validada mediante posse de pokébola no inventário e espaço na equipe
            if "Pokebola" in self.inventario and len(self.pokemons_ativos) < 6:
                capturar = input(f"Tentar capturar esse {p_selvagem.tipo}? (s/n): ").strip().lower()
                if capturar == 's':
                    self.inventario.remove("Pokebola")
                    p_selvagem.hp = 100 # Pokémons recém-capturados têm a vida totalmente restaurada
                    self.pokemons_ativos.append(p_selvagem)
                    print(f"✨ Sucesso! {p_selvagem.tipo} tá no time agora.")
                    return True
        return False

    def desafiar_lider(self, lider):
        print(f"\n⚠️ O LÍDER DE GINÁSIO {lider.nome.upper()} DESAFIA VOCÊ!")
        
        meus_vivos = [p for p in self.pokemons_ativos if p.hp >= 20]
        lider_vivos = [p for p in lider.equipe if p.hp >= 20]
        
        if not meus_vivos:
            print("❌ Sua equipe está sem condições de lutar. Cure-os no Centro Médico primeiro!")
            return False
            
        meu_lutador = meus_vivos[0]
        lutador_lider = lider_vivos[0]
        
        print(f"👉 Você enviou {meu_lutador.tipo} | O Líder enviou {lutador_lider.tipo}!")
        
        dano_no_lider = max(0, meu_lutador.ap - lutador_lider.dp)
        dano_em_mim = max(0, lutador_lider.ap - meu_lutador.dp)
        
        lutador_lider.hp -= dano_no_lider
        meu_lutador.hp -= dano_em_mim
        print(f"💥 Seu ataque causou {dano_no_lider} de dano! Você recebeu {dano_em_mim} de dano!")
        
        if meu_lutador.hp < 20:
            print("💀 Seu pokémon desmaiou! O Líder venceu esta rodada.")
            meu_lutador.xp += 3
            return False
        elif lutador_lider.hp < 20:
            print(f"🏆 VOCÊ DERROTOU O LÍDER {lider.nome.upper()}!")
            # A derrota definitiva do líder concede a cobiçada insígnia, passo vital para zerar o jogo
            self.insignias += 1
            lider.derrotado = True
            meu_lutador.xp += 30 
            print(f"🏅 Você recebeu uma INSÍGNIA! Total: {self.insignias}/8")
            return True
        else:
            print("⚔️ Batalha empatada. Ambos os pokémons continuam de pé!")
            return False
        
    def enfrentar_rocket(self, rocket, mapa):
        print(f"\n🛑 ALERTA! A EQUIPE ROCKET INTERCEPTOU VOCÊ EM {self.local_atual}!")
        
        meus_vivos = [p for p in self.pokemons_ativos if p.hp >= 20]
        rocket_vivos = [p for p in rocket.equipe if p.hp >= 20]
        
        if not meus_vivos:
            print("❌ Seus pokémons estão desmaiados. A Equipe Rocket roubou um item seu e fugiu!")
            if self.inventario:
                self.inventario.pop() # Punição: perde um item aleatório
            return False
            
        meu_lutador = meus_vivos[0]
        lutador_rocket = rocket_vivos[0]
        
        print(f"👉 Você enviou {meu_lutador.tipo} | Rocket enviou {lutador_rocket.tipo}!")
        
        dano_no_rocket = max(0, meu_lutador.ap - lutador_rocket.dp)
        dano_em_mim = max(0, lutador_rocket.ap - meu_lutador.dp)
        
        lutador_rocket.hp -= dano_no_rocket
        meu_lutador.hp -= dano_em_mim
        print(f"💥 Você causou {dano_no_rocket} de dano e recebeu {dano_em_mim}!")
        
        if meu_lutador.hp < 20:
            print("💀 Você perdeu! A Equipe Rocket foge rindo.")
            meu_lutador.xp += 3
            return False
        elif lutador_rocket.hp < 20:
            print("🏆 VOCÊ DERROTOU A EQUIPE ROCKET!")
            meu_lutador.xp += 20
            
            cidades = list(mapa.adjacencias.keys())
            vizinhos = [v for v, t in mapa.adjacencias[self.local_atual]]
            # Filtra cidades que não são a atual e nem vizinhas diretas
            cidades_distantes = [c for c in cidades if c != self.local_atual and c not in vizinhos]
            
            rocket.local_atual = random.choice(cidades_distantes) if cidades_distantes else random.choice(cidades)
                
            print(f"💨 Eles usaram uma bomba de fumaça e fugiram para {rocket.local_atual}!")
            
            # Gera uma equipe nova para o próximo encontro
            rocket.equipe = [Pokemon(), Pokemon()]
            for p in rocket.equipe:
                p.ap += 15
                p.dp += 15
            return True
        else:
            print("⚔️ A batalha continua acirrada. Ninguém caiu ainda!")
            return False
        
class EquipeRocket:
    def __init__(self, local_inicial):
        self.local_atual = local_inicial
        # A Equipe Rocket carrega Pokémons mais fortes para dificultar a exploração
        self.equipe = [Pokemon(), Pokemon()]
        for p in self.equipe:
            p.ap += 15
            p.dp += 15
