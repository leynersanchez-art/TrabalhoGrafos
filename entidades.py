import random

TIPOS_POKEMON = ["Água", "Fogo", "Planta", "Elétrico", "Fantasma", "Venenoso", "Gelo"]

ATAQUES_POR_TIPO = {
    "Água": [("Jato d'Água", 5), ("Hidro Bomba", 15), ("Bolha", 0)],
    "Fogo": [("Lança-Chamas", 10), ("Investida de Fogo", 15), ("Brasa", 0)],
    "Planta": [("Chicote de Vinha", 5), ("Folha Navalha", 12), ("Absorver", 0)],
    "Elétrico": [("Choque do Trovão", 10), ("Raio", 15), ("Investida", 0)],
    "Fantasma": [("Sombra Sinistra", 10), ("Bola Sombria", 15), ("Lamber", 0)],
    "Venenoso": [("Investida Venenosa", 8), ("Ataque de Lodo", 14), ("Picada Venenosa", 0)],
    "Gelo": [("Vento Gelado", 8), ("Nevasca", 15), ("Soco Gelado", 0)],
}

ESPECIES_POR_TIPO = {
    "Água": ["Aqualim", "Aquartor", "Aquamestre"],
    "Fogo": ["Flamito", "Flamaroz", "Infernaut"],
    "Planta": ["Folhin", "Folharbusto", "Florestal"],
    "Elétrico": ["Voltin", "Voltrago", "Trovoar"],
    "Fantasma": ["Sombrin", "Sombraz", "Espectral"],
    "Venenoso": ["Toxin", "Toxidral", "Peçonhaz"],
    "Gelo": ["Gelin", "Gelaço", "Glacius"],
}

FORTE_CONTRA = {
    "Água": ["Fogo"],
    "Fogo": ["Planta", "Gelo"],
    "Planta": ["Água"],
    "Elétrico": ["Água"],
    "Fantasma": ["Fantasma"],
    "Venenoso": ["Planta"],
    "Gelo": ["Planta"],
}

FRACO_CONTRA = {
    "Água": ["Planta", "Elétrico"],
    "Fogo": ["Água"],
    "Planta": ["Fogo", "Venenoso", "Gelo"],
    "Elétrico": ["Planta"],
    "Fantasma": [],
    "Venenoso": ["Venenoso", "Fantasma"],
    "Gelo": ["Água", "Fogo"],
}

def obter_multiplicador_tipo(tipo_atacante, tipo_defensor):
    if tipo_defensor in FORTE_CONTRA.get(tipo_atacante, []):
        return 2.0
    if tipo_defensor in FRACO_CONTRA.get(tipo_atacante, []):
        return 0.5
    return 1.0


class Pokemon:
    def __init__(self):
        self.tipo = random.choice(TIPOS_POKEMON)
        self.hp = 100
        self.xp = 0
        self.ap_base = random.randint(10, 50)
        self.dp_base = random.randint(10, 50)
        self.pontos_batalha_ap = 0
        self.pontos_batalha_dp = 0
        self.fase_evolucao = 1
        self.ataques = [{"nome": nome, "bonus": bonus} for nome, bonus in ATAQUES_POR_TIPO[self.tipo]]
        self.especie = ESPECIES_POR_TIPO[self.tipo][0]
        self.ap = 0
        self.dp = 0
        self.cooldown_inconsciente = 0
        self.precisa_pmc = False
        self._atualizar_atributos()

    def _atualizar_atributos(self):
        bonus_xp = round(self.xp * 0.10)
        self.ap = round(self.ap_base + bonus_xp + self.pontos_batalha_ap)
        self.dp = round(self.dp_base + bonus_xp + self.pontos_batalha_dp)

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        self._atualizar_atributos()

    def registrar_resultado_batalha(self, xp_oponente_no_momento):
        if xp_oponente_no_momento >= self.xp:
            self.pontos_batalha_ap += 1
            self.pontos_batalha_dp += 1
        self._atualizar_atributos()

    def evoluir(self):
        if self.fase_evolucao < 3:
            self.fase_evolucao += 1
            self.ap_base = round(self.ap_base * 1.3)
            self.dp_base = round(self.dp_base * 1.3)
            self.especie = ESPECIES_POR_TIPO[self.tipo][self.fase_evolucao - 1]
            self._atualizar_atributos()

    def desmaiar(self):
        self.cooldown_inconsciente = random.randint(10, 50)
        if self.hp < 5:
            self.precisa_pmc = True

    def avancar_tempo(self, distancia):
        if self.cooldown_inconsciente > 0:
            self.cooldown_inconsciente = max(0, self.cooldown_inconsciente - distancia)
        
        if self.cooldown_inconsciente == 0 and not self.precisa_pmc and self.hp < 20 and self.hp >= 5:
            self.hp = 20

    def esta_disponivel(self):
        return self.hp >= 20 and self.cooldown_inconsciente <= 0 and not self.precisa_pmc

    def definir_tipo(self, tipo):
        self.tipo = tipo
        self.ataques = [{"nome": nome, "bonus": bonus} for nome, bonus in ATAQUES_POR_TIPO[tipo]]
        self.especie = ESPECIES_POR_TIPO[tipo][self.fase_evolucao - 1]

    def __str__(self):
        return f"{self.especie} [{self.tipo}] (HP:{self.hp} XP:{self.xp} AP:{self.ap} DP:{self.dp})"


class Item:
    def __init__(self):
        self.tipo = random.choice(["Ovo", "Erva Medicinal", "Pokebola"])

    def __str__(self):
        return f"{self.tipo}"


class LiderGinasio:
    def __init__(self, nome, cidade_natal):
        self.nome = nome
        self.derrotado = False
        self.xp = random.randint(0, 5)
        self.equipe = [Pokemon(), Pokemon(), Pokemon()]
        self.cidade_natal = cidade_natal
        self.local_atual = cidade_natal
        self.passos_fora = 0
        self.passos_parado_no_ginasio = 0
        self.limite_patrulha = random.randint(2, 4)
        self.limite_permanencia = random.randint(3, 6)

    def mover_um_passo(self, mapa):
        if self.local_atual == self.cidade_natal and self.passos_parado_no_ginasio < self.limite_permanencia:
            self.passos_parado_no_ginasio += 1
            return

        if self.passos_fora >= self.limite_patrulha:
            self.local_atual = self.cidade_natal
            self.passos_fora = 0
            self.passos_parado_no_ginasio = 0
            return

        # Filtra apenas vizinhos que não sejam Lab_Carvalho nem Centro_Medico
        vizinhos = [
            cidade for cidade, tempo in mapa.adjacencias[self.local_atual]
            if "Lab_Carvalho" not in cidade and "Centro_Medico" not in cidade
        ]
        
        if vizinhos:
            self.local_atual = random.choice(vizinhos)
            self.passos_fora += 1


class TreinadorNPC:
    def __init__(self, nome, local_atual):
        self.nome = nome
        self.local_atual = local_atual
        self.xp = random.randint(0, 20)
        self.derrotado_hoje = False
        self.equipe = [Pokemon(), Pokemon(), Pokemon()]


class Treinador:
    def __init__(self, nome, local_atual):
        self.nome = nome
        self.local_atual = local_atual
        self.xp = 0
        self.distancia_percorrida = 0
        self.pokemons_ativos = []
        self.pokemons_incubadora = []
        self.pokemons_carvalho = []
        self.insignias = 0
        self.meta_insignias = 8
        self.inventario = []
        self.inscrito_na_liga = False
        self.distancia_pendente_xp = 0
        self.distancia_pendente_hp = 0

    def receber_kit_inicial(self):
        resposta = input("O Professor Carvalho oferece 3 pokémons iniciais (Água, Fogo e Planta). Deseja aceitá-los? (s/n): ").strip().lower()

        if resposta == 's':
            p_agua, p_fogo, p_planta = Pokemon(), Pokemon(), Pokemon()
            p_agua.definir_tipo("Água")
            p_fogo.definir_tipo("Fogo")
            p_planta.definir_tipo("Planta")
            self.pokemons_ativos.extend([p_agua, p_fogo, p_planta])
            print("🎁 Você recebeu os 3 pokémons iniciais!")
        else:
            pokemon_unico = Pokemon()
            self.pokemons_ativos.append(pokemon_unico)
            print(f"🎁 Você recebeu apenas um pokémon aleatório do laboratório: {pokemon_unico.tipo}!")

        self.inventario.append("Encubadora")
        for _ in range(7):
            self.inventario.append("Pokebola")

    def exibir_status(self):
        print(f"\n=== STATUS DO TREINADOR {self.nome.upper()} ===")
        print(f"📍 Local Atual: {self.local_atual}")
        print(f"⭐ XP: {self.xp} | 🏅 Insígnias: {self.insignias}")
        print("🐾 Pokémons Ativos:")
        for i, p in enumerate(self.pokemons_ativos):
            status = ""
            if p.precisa_pmc:
                status = " 🚑 [machucado grave — precisa do PMC]"
            elif p.cooldown_inconsciente > 0:
                status = f" 💤 [desmaiado, recupera em {p.cooldown_inconsciente} de distância]"
            print(f"  {i+1}. {p}{status}")
        print(f"🎒 Inventário: {self.inventario}")
        print("===================================\n")

    def processar_passagem_de_tempo(self, tempo_gasto):
        self.distancia_percorrida += tempo_gasto
        self.distancia_pendente_hp += tempo_gasto
        self.distancia_pendente_xp += tempo_gasto

        recuperacao_hp = self.distancia_pendente_hp // 10
        self.distancia_pendente_hp %= 10

        ganho_xp = self.distancia_pendente_xp // 100
        self.distancia_pendente_xp %= 100

        for p in self.pokemons_ativos:
            p.avancar_tempo(tempo_gasto)

            if p.hp >= 20 and not p.precisa_pmc:
                p.hp = min(100, p.hp + recuperacao_hp)

            p.ganhar_xp(ganho_xp)

            if p.xp >= 1000 and p.fase_evolucao < 3:
                ap_antigo, dp_antigo = p.ap, p.dp
                p.evoluir()
                print(f"🌟 INCRÍVEL! Seu Pokémon {p.tipo} evoluiu para a FASE {p.fase_evolucao}! (AP: {ap_antigo}→{p.ap}, DP: {dp_antigo}→{p.dp})")

        ovos_prontos = []
        for ovo in self.pokemons_incubadora:
            ovo["distancia_restante"] -= tempo_gasto
            if ovo["distancia_restante"] <= 0:
                ovos_prontos.append(ovo)

        for ovo in ovos_prontos:
            self.pokemons_incubadora.remove(ovo)
            novo_pokemon = Pokemon()
            self.pokemons_ativos.append(novo_pokemon)
            print(f"🎉 CHOCOU! Um {novo_pokemon.tipo} nasceu e entrou pra equipe!")

    def mover(self, mapa, destino):
        vizinhos = {cidade: tempo for cidade, tempo in mapa.adjacencias[self.local_atual]}

        if destino in vizinhos:
            tempo_gasto = vizinhos[destino]
            self.local_atual = destino
            print(f"\n🚶 Você viajou para {destino} e percorreu {tempo_gasto} de distância.")
            self.processar_passagem_de_tempo(tempo_gasto)
        else:
            print(f"\n❌ {destino} é longe demais. Você só pode viajar para cidades vizinhas.")

    def pegar_item(self, item):
        if item.tipo == "Pokebola":
            self.inventario.append("Pokebola")
            print("🎒 Você encontrou e guardou uma Pokébola!")

        elif item.tipo == "Erva Medicinal":
            print("🌿 Preparando poção com a Erva Medicinal...")
            for p in self.pokemons_ativos:
                if p.hp >= 20 and not p.precisa_pmc:
                    p.hp = min(100, p.hp + 10)
            print("✨ Todos os pokémons conscientes recuperaram 10 de HP!")

        elif item.tipo == "Ovo":
            total = len(self.pokemons_ativos) + len(self.pokemons_incubadora)
            if total < 7 and "Encubadora" in self.inventario:
                pegar = input("🥚 Você encontrou um Ovo! Deseja pegá-lo? (s/n): ").strip().lower()
                if pegar == 's':
                    self.pokemons_incubadora.append({"distancia_restante": 100})
                    print("🥚 Ovo guardado na Encubadora! Faltam 100 de distância pra ele chocar.")
                else:
                    print("🥚 Você decidiu deixar o Ovo para trás.")
            else:
                print("🥚 Achou um Ovo, mas você não pode carregar mais de 7 itens entre pokémons e ovos.")

    def _escolher_ataque(self, pokemon, controlado_pelo_jogador):
        if not controlado_pelo_jogador:
            return random.choice(pokemon.ataques)

        print(f"\nAtaques disponíveis para {pokemon.tipo}:")
        for i, ataque in enumerate(pokemon.ataques):
            print(f"  {i+1}. {ataque['nome']}")
        escolha = input("Escolha o ataque (número): ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(pokemon.ataques):
            return pokemon.ataques[int(escolha) - 1]
        print("Ataque inválido, usando o primeiro disponível.")
        return pokemon.ataques[0]

    def _executar_ataque(self, atacante, bonus_ap_atacante, defensor, bonus_dp_defensor, controlado_pelo_jogador):
        ataque = self._escolher_ataque(atacante, controlado_pelo_jogador)
        diferenca_xp = abs(atacante.xp - defensor.xp)
        chance_esquiva = min(0.9, diferenca_xp / 1000)
        chance_critico = min(0.9, diferenca_xp / 1000)

        if random.random() < chance_esquiva:
            print(f"💨 {defensor.tipo} esquivou de {ataque['nome']}!")
            return

        ap_efetivo = atacante.ap + bonus_ap_atacante + ataque["bonus"]
        dp_efetivo = defensor.dp + bonus_dp_defensor
        multiplicador = obter_multiplicador_tipo(atacante.tipo, defensor.tipo)

        dano = max(0, ap_efetivo - dp_efetivo)
        dano = round(dano * multiplicador)

        if dano > 0 and random.random() < chance_critico:
            dano *= 2
            print("🎯 ATAQUE CRÍTICO!")

        if multiplicador > 1:
            print("💢 Foi super efetivo!")
        elif multiplicador < 1:
            print("🛡️ Não foi muito efetivo...")

        defensor.hp -= dano
        print(f"💥 {atacante.tipo} usou {ataque['nome']} e causou {dano} de dano! (HP restante: {max(0, defensor.hp)})")

    def batalhar(self, p_selvagem):
        print(f"\n⚔️ UM POKÉMON SELVAGEM APARECEU: {p_selvagem}!")

        p_aliado = next((p for p in self.pokemons_ativos if p.esta_disponivel()), None)
        if not p_aliado:
            print("❌ Sua equipe inteira caiu. Você foge da batalha!")
            self.processar_passagem_de_tempo(1)
            return False

        print(f"👉 Vai, {p_aliado.tipo}!")

        turno_do_selvagem = True
        turnos = 0
        MAX_TURNOS = 200

        while p_aliado.hp >= 20 and p_selvagem.hp >= 20 and turnos < MAX_TURNOS:
            turnos += 1

            if not turno_do_selvagem:
                desistir = input("Deseja continuar a captura ou desistir e deixar o selvagem fugir? (continuar/desistir): ").strip().lower()
                if desistir == 'desistir':
                    print(f"💨 Você desistiu. O {p_selvagem.tipo} foge escondido, ferido pela luta.")
                    self.processar_passagem_de_tempo(1)
                    return False

            if turno_do_selvagem:
                self._executar_ataque(p_selvagem, 0, p_aliado, 0, controlado_pelo_jogador=False)
            else:
                self._executar_ataque(p_aliado, 0, p_selvagem, 0, controlado_pelo_jogador=True)
            turno_do_selvagem = not turno_do_selvagem

        self.processar_passagem_de_tempo(1)

        if p_aliado.hp < 20:
            print(f"💀 Seu {p_aliado.tipo} foi nocauteado!")
            p_aliado.ganhar_xp(3)
            p_aliado.desmaiar()
            return False

        if p_selvagem.hp >= 20:
            print("⏱️ A batalha se arrastou demais e o selvagem fugiu.")
            return False

        print("🏆 Vitória! O pokémon selvagem está inconsciente.")
        p_aliado.registrar_resultado_batalha(p_selvagem.xp)
        p_aliado.ganhar_xp(10)
        self.xp += 10

        if "Pokebola" in self.inventario:
            capturar = input(f"Tentar capturar esse {p_selvagem.tipo}? (s/n): ").strip().lower()
            if capturar == 's':
                self.inventario.remove("Pokebola")
                p_selvagem.hp = 100
                self.pokemons_ativos.append(p_selvagem)

                self.xp += 3
                p_aliado.ganhar_xp(3)
                p_selvagem.ganhar_xp(3)
                print(f"✨ Sucesso! {p_selvagem.tipo} tá no time agora. (+3 XP de bônus de captura)")

                if len(self.pokemons_ativos) > 6:
                    self._enviar_excedente_para_carvalho()
                return True
            else:
                print(f"💨 Você decidiu não capturar. O {p_selvagem.tipo} foge escondido.")
        return False

    def _enviar_excedente_para_carvalho(self):
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

    def _oponente_aceita_desafio(self, oponente):
        if isinstance(oponente, LiderGinasio):
            return True
        return random.random() < 0.85

    def _duelo_3v3(self, oponente):
        meus_conscientes = [p for p in self.pokemons_ativos if p.esta_disponivel()]
        seus_conscientes = [p for p in oponente.equipe if p.esta_disponivel()]

        if len(meus_conscientes) < 3 or len(seus_conscientes) < 3:
            print("❌ Uma das partes não tem pokémons suficientes para o duelo.")
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
        xp_oponente_treinador = oponente.xp
        xp_desafiante_antes_da_luta = self.xp

        turno_do_desafiante = False
        turnos = 0
        MAX_TURNOS = 200

        while time_desafiante and time_oponente and turnos < MAX_TURNOS:
            turnos += 1

            if turno_do_desafiante:
                atacante, bonus_atacante = ativo_desafiante, self.xp
                defensor, bonus_defensor = ativo_oponente, xp_oponente_treinador
            else:
                atacante, bonus_atacante = ativo_oponente, xp_oponente_treinador
                defensor, bonus_defensor = ativo_desafiante, self.xp

            self._executar_ataque(atacante, bonus_atacante, defensor, bonus_defensor,
                                   controlado_pelo_jogador=(atacante is ativo_desafiante))

            if defensor.hp < 20:
                print(f"💀 {defensor.tipo} desmaiou!")
                xp_defensor_no_momento = defensor.xp
                defensor.ganhar_xp(3)
                defensor.desmaiar()
                atacante.registrar_resultado_batalha(xp_defensor_no_momento)
                atacante.ganhar_xp(10)

                if defensor is ativo_desafiante:
                    time_desafiante.remove(ativo_desafiante)
                    if len(time_desafiante) > 1:
                        print("Escolha o próximo pokémon:")
                        for i, p in enumerate(time_desafiante):
                            print(f"  {i+1}. {p}")
                        prox = input("Número do pokémon: ").strip()
                        if prox.isdigit() and 1 <= int(prox) <= len(time_desafiante):
                            ativo_desafiante = time_desafiante[int(prox) - 1]
                        else:
                            ativo_desafiante = time_desafiante[0]
                    elif time_desafiante:
                        ativo_desafiante = time_desafiante[0]
                else:
                    time_oponente.remove(ativo_oponente)
                    if time_oponente:
                        if random.random() < 0.2:
                            print(f"🏳️ {oponente.nome} desistiu da batalha!")
                            time_oponente = []
                        else:
                            ativo_oponente = time_oponente[0]

            turno_do_desafiante = not turno_do_desafiante

        self.processar_passagem_de_tempo(1)

        if not time_desafiante and not time_oponente:
            print("\n⚖️ Ambos os lados ficaram sem pokémons ao mesmo tempo. Sem vencedor.")
            return False
        elif time_desafiante and not time_oponente:
            vitoria = True
        elif time_oponente and not time_desafiante:
            vitoria = False
        else:
            print("\n⏱️ A batalha se arrastou demais e terminou em impasse.")
            return False

        if vitoria:
            print(f"\n🏆 {self.nome} VENCEU A BATALHA CONTRA {oponente.nome}!")
            self.xp += 3 if xp_oponente_treinador >= xp_desafiante_antes_da_luta else 1
        else:
            print(f"\n💀 {self.nome} PERDEU A BATALHA CONTRA {oponente.nome}!")

        return vitoria

    def desafiar_treinador(self, oponente):
        meus_conscientes = [p for p in self.pokemons_ativos if p.esta_disponivel()]
        if len(meus_conscientes) < 3:
            print("❌ Você precisa de ao menos 3 pokémons conscientes para desafiar um treinador!")
            return False

        resposta = input(f"\n⚔️ Deseja desafiar {oponente.nome} para uma batalha? (s/n): ").strip().lower()
        if resposta != 's':
            print("Você optou por não desafiar desta vez.")
            return False

        print(f"{self.nome} desafiou {oponente.nome} para uma batalha!")

        seus_conscientes = [p for p in oponente.equipe if p.esta_disponivel()]
        if len(seus_conscientes) < 3 or not self._oponente_aceita_desafio(oponente):
            print(f"🚫 {oponente.nome} recusou o desafio.")
            return False

        print(f"✅ {oponente.nome} aceitou! A partir de agora você não pode mais desistir da batalha.")
        return self._duelo_3v3(oponente)

    def desafiar_lider(self, lider):
        if lider.derrotado:
            print(f"🏅 Você já derrotou {lider.nome}.")
            return False

        venceu = self.desafiar_treinador(lider)
        if venceu:
            lider.derrotado = True
            self.insignias += 1
            print(f"🏅 Você recebeu a insígnia de {lider.nome}! Total: {self.insignias}/{self.meta_insignias}")
        return venceu

    def enfrentar_rocket(self, rocket, mapa):
        print(f"\n🛑 ALERTA! A EQUIPE ROCKET INTERCEPTOU VOCÊ EM {self.local_atual}!")

        meus_conscientes = [p for p in self.pokemons_ativos if p.esta_disponivel()]
        if len(meus_conscientes) < 3:
            print("❌ Sua equipe não está em condições de lutar! A Equipe Rocket aproveita a fraqueza.")
            self._rocket_rouba_pokemon()
            self._rocket_tornar_invisivel(rocket)
            return False

        vitoria = self._duelo_3v3(rocket)

        if vitoria:
            self._rocket_fugir_para_local_distante(rocket, mapa)
            rocket.equipe = [Pokemon(), Pokemon(), Pokemon()]
        else:
            self._rocket_rouba_pokemon()
            self._rocket_tornar_invisivel(rocket)

        return vitoria

    def _rocket_rouba_pokemon(self):
        if not self.pokemons_ativos:
            print("😮 Você não tinha nenhum pokémon para ser roubado.")
            return
        pokemon_roubado = random.choice(self.pokemons_ativos)
        self.pokemons_ativos.remove(pokemon_roubado)
        print(f"💢 A Equipe Rocket fugiu com seu {pokemon_roubado.tipo}! O roubo é permanente.")

    def _rocket_tornar_invisivel(self, rocket):
        rocket.visivel = False
        rocket.distancia_para_reaparecer = self.distancia_percorrida + 40
        rocket.equipe = [Pokemon(), Pokemon(), Pokemon()]
        print("💨 A Equipe Rocket desapareceu sem deixar rastro...")

    def _rocket_fugir_para_local_distante(self, rocket, mapa):
        cidades = list(mapa.adjacencias.keys())
        vizinhos = [v for v, t in mapa.adjacencias[self.local_atual]]
        cidades_distantes = [c for c in cidades if c != self.local_atual and c not in vizinhos]
        rocket.local_atual = random.choice(cidades_distantes) if cidades_distantes else random.choice(cidades)
        print(f"🏆 Você derrotou a Equipe Rocket! Eles fugiram para {rocket.local_atual}.")

    def tratar_pokemons_pmc(self):
        pokemons_para_tratar = [p for p in self.pokemons_ativos if p.precisa_pmc]
        if not pokemons_para_tratar:
            print("✅ Nenhum dos seus pokémons precisa de tratamento no PMC no momento.")
            return

        print(f"\n🏥 {len(pokemons_para_tratar)} pokémon(s) internados para tratamento (sem fila de espera, em paralelo).")
        tempo_maximo = 0
        for p in pokemons_para_tratar:
            tempo_tratamento = random.randint(10, 50)
            tempo_maximo = max(tempo_maximo, tempo_tratamento)
            p.hp = 100
            p.precisa_pmc = False
            p.cooldown_inconsciente = 0
            print(f"  💊 {p.tipo} tratado em {tempo_tratamento} unidades de tempo. HP restaurado para 100.")

        self.processar_passagem_de_tempo(tempo_maximo)
        print(f"⏱️ Tratamento concluído após {tempo_maximo} unidades de tempo no PMC.")

    def tentar_inscricao_liga(self, prazo_maximo):
        if self.distancia_percorrida > prazo_maximo:
            print("\n❌ O prazo de inscrição na Liga Pokémon já se esgotou. Você está inapto para a competição.")
            return False

        if self.insignias < self.meta_insignias:
            print(f"\n❌ Você ainda não tem insígnias suficientes! ({self.insignias}/{self.meta_insignias})")
            return False

        self.inscrito_na_liga = True
        print(f"\n🏆 PARABÉNS! Com {self.insignias} insígnias e dentro do prazo, você se inscreveu na Liga Pokémon!")
        print("🎉 VOCÊ VENCEU O JOGO!")
        return True


class EquipeRocket:
    def __init__(self, local_inicial):
        self.local_atual = local_inicial
        self.nome = "Equipe Rocket"
        self.xp = random.randint(10, 25)
        self.equipe = [Pokemon(), Pokemon(), Pokemon()]
        self.visivel = True
        self.distancia_para_reaparecer = None