import random

TIPOS_POKEMON = ["Água", "Fogo", "Planta", "Elétrico", "Fantasma", "Venenoso", "Gelo"]

class Pokemon:
    def __init__(self):
        self.tipo = random.choice(TIPOS_POKEMON)
        self.hp = 100 
        self.xp = 0
        self.ap = random.randint(10, 50) 
        self.dp = random.randint(10, 50)
        self.fase_evolucao = 1 

    def __str__(self):
        return f"Pkmn {self.tipo} (HP:{self.hp} XP:{self.xp} AP:{self.ap} DP:{self.dp})"

class Item:
    def __init__(self):
        self.tipo = random.choice(["Ovo", "Erva Medicinal", "Pokebola"])
        
    def __str__(self):
        return f"{self.tipo}"

class Treinador:
    def __init__(self, nome, local_atual):
        self.nome = nome
        self.local_atual = local_atual
        self.xp = 0
        self.pokemons_ativos = []
        self.pokemons_incubadora = []
        self.insignias = 0
        self.inventario = []

    def receber_kit_inicial(self):
        p_agua = Pokemon()
        p_agua.tipo = "Água"
        
        p_fogo = Pokemon()
        p_fogo.tipo = "Fogo"
        
        p_planta = Pokemon()
        p_planta.tipo = "Planta"
        
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
