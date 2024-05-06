import random


# Define the Player class
class Player:
    def __init__(self, name):
        self.name = name
        self.provinces = []
        self.armys = []
        self.actions = 0

    def add_province(self, province):
        self.provinces.append(province)

    def remove_province(self, province):
        self.provinces.remove(province)

    def add_army(self, army):
        self.armys.append(army)

    def remove_army(self, army):
        self.armys.remove(army)

    def get_provinces(self):
        return self.provinces

    def action_move_army(self):
        if self.actions >= 0.75:
            self.actions -= 0.75

    def action_upgrade_province(self, province):
        modi = province.terrain_type.terrain_upgrade_modifier
        if self.actions >= round(1.50 * modi, 2):
            self.actions -= round(1.50 * modi, 2)
            return True
        return False

    def action_attack_province(self):
        if self.actions >= 1:
            self.actions -= 1

    def action_heal_army(self):
        if self.actions >= 0.25:
            self.actions -= 0.25

    def can_perform_action(self):
        return self.actions > 0

    def army_creation(self, province):
        army_created = Army(province, self)
        self.add_army(army_created)


# Define the Province class
class Province:
    def __init__(self, name, current_owner, terrain):
        self.name = name
        self.current_owner = current_owner
        self.terrain_type = terrain
        self.neighbor_provinces = []
        self.army_progress = 0
        self.level = 1
        self.level_cap = 5

    def upgrade(self):
        if self.level < self.level_cap:
            self.level += 1

    def produce_army(self):
        self.army_progress += self.level
        if self.army_progress >= 5:
            self.current_owner.army_creation(self)
            self.army_progress = 0


# Define the Army class
class Army:
    def __init__(self, current_province, owner, attack=1, defense=1):
        self.attack = round(attack * (random.uniform(0.80, 1.2)), 2)
        self.defense = round(defense * (random.uniform(0.80, 1.2)), 2)
        self.health = 10
        self.current_province = current_province
        self.owner = owner

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_health(self):
        return self.health

    def get_province(self):
        return self.province

    def heal_army(self, province):
        self.health += province.level * 1.25

    def set_province(self, province):
        self.province = province


class Terrain:
    def __init__(
        self,
        terrain: str,
        move_modifier: float,
        upgrade_modifier: float,
        defence_modifier: float,
    ):
        self.terrain = terrain
        self.terrain_move_modifier = move_modifier
        self.terrain_upgrade_modifier = upgrade_modifier
        self.terrain_defence_modifier = defence_modifier


# Define the Game class
class Game:
    def __init__(self):
        self.players = []
        self.current_player = None

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def start(self):
        # Initialize game state
        self.current_player = self.players[0]

    def end(self):
        # Check if any player has conquered all provinces
        for player in self.players:
            if len(player.provinces) == 0:
                return True
        return False

    def next_turn(self):
        # Switch to the next player
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        self.current_player = self.players[next_index]

    def play(self):
        # Main game loop
        while not self.end():
            # Perform player actions
            for player in self.players:
                self.current_player = player
                player.actions += 3
                self.mapmode = True

                while player.can_perform_action():
                    # Perform action based on player's choice
                    if self.mapmode:
                        self.print_map()
                    action = input("Choose an action: ")
                    if action == "1":
                        self.move_troops(self.current_player)
                    elif action == "2":
                        self.upgrade_province(self.current_player)
                    elif action == "3":
                        self.attack_province()
                    elif action == "0":
                        break
                    else:
                        print("Invalid action. Try again.")

                # Update game state
                self.army_creation(self.current_player)
            self.next_turn()

    def army_creation(self, player_m):
        for province in player_m.provinces:
            province.produce_army()
            if player_m.armys != []:
                print(
                    f"Army created in {province.name} with attack {player_m.armys[-1].attack} and defense {player_m.armys[-1].defense}"
                )

    def move_troops(self, player_m):
        # Implement troop movement logic
        print("A")

    def upgrade_province(self, player_m):
        # Implement province upgrade logic
        index_list = [
            player_m.provinces.index(province) + 1 for province in player_m.provinces
        ]
        up_prov = input(
            f"Selecione a província para ser melhorada: {[f'{province.name} ({player_m.provinces.index(province) + 1})' for province in player_m.provinces]} "
        )
        if int(up_prov) in index_list:
            action = player_m.action_upgrade_province(
                player_m.provinces[index_list.index(int(up_prov))]
            )
            if action:
                player_m.provinces[index_list.index(int(up_prov))].upgrade()
                print(player_m.provinces[index_list.index(int(up_prov))].level)
            else:
                print("Não há pontos de ação suficientes para realizar a ação.")
                self.mapmode = False

    def attack_province(self):
        # Implement province attack logic
        pass

    def print_map(self):
        # Print the map with province ownership and armies
        print("\nMap: \n")
        for player in self.players:
            print(f"Player: {player.name}")
            for province in player.provinces:
                print(
                    f"Province: {province.name} (Level: {province.level}) (Terrain: {province.terrain_type.terrain})"
                )
                if player.armys != []:
                    armies = [
                        army
                        for army in player.armys
                        if army.current_province == province
                    ]
                    for army in armies:
                        print(
                            f"Army: Attack: {army.attack}, Defense: {army.defense}, Health: {army.health}"
                        )
            print()
        print(f"Current Player: {self.current_player.name}")
        print(f"Actions: {self.current_player.actions}\n")


# Create players
player1 = Player("Human")
player2 = Player("AI 1")
player3 = Player("AI 2")
player4 = Player("AI 3")
# Create terrains
terrain1 = Terrain("Plains", 1, 1, 1)
terrain2 = Terrain("Forest", 0.8, 1.25, 0.8)
terrain3 = Terrain("Mountain", 0.6, 1.33, 0.6)
terrain4 = Terrain("Desert", 1.2, 1, 1)
# Create provinces
province1 = Province("Province 1", player1, terrain1)
province2 = Province("Province 2", player2, terrain2)
province3 = Province("Province 3", player3, terrain3)
province4 = Province("Province 4", player4, terrain4)
province_teste = Province("Province Teste", player1, terrain3)

# Add provinces to players
player1.add_province(province1)
player1.add_province(province_teste)
player2.add_province(province2)
player3.add_province(province3)
player4.add_province(province4)


# Create game
game = Game()

# Add players to game
game.add_player(player1)
game.add_player(player2)
game.add_player(player3)
game.add_player(player4)

# Start game
game.start()

# Play game
game.play()


"""
Checklist:
Criação de Exércitos	Check
Criação de Provincias	Check
Criação de Jogadores	Check
Criação de Terrenos     Check
Geração de Exércitos	Check
Criação do Mapa         Check
Funçao para melhorar província	Check
Função para criar exercito em turno    Check

Função para movimentação de tropas

"""
