from collections import defaultdict
from Army import Army_Group


class Game:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.mapmode = True

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
                self.group_army(self.current_player)
            self.next_turn()

    def army_creation(self, player_m):
        for province in player_m.provinces:
            province.produce_army()
            if player_m.armys:
                print(
                    f"Exército criado em: {province.name} com {player_m.armys[-1].attack} de ataque e {player_m.armys[-1].defense} de defesa"
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
        print("\nMapa: \n")
        for player in self.players:
            print(f"Jogador: {player.name}")
            for province in player.provinces:
                print(
                    f"Província: {province.name} (Nível: {province.level}) (Terreno: {province.terrain_type.terrain})"
                )
                if player.armys:
                    armies = [
                        army
                        for army in player.armys
                        if army.current_province == province
                    ]
                    for army in armies:
                        if isinstance(army, Army_Group):
                            print(
                                f"Grupo com: {len(army.armys)} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}"
                            )
                        else:
                            print(
                                f"Exército: Ataque: {army.attack}, Defesa: {army.defense}, Vida: {army.health}"
                            )
            print()
        print(f"Jogador Atual: {self.current_player.name}")
        print(f"Pontos de Ação: {self.current_player.actions}\n")

    def group_army(self, player_m):
        for province in player_m.provinces:
            armies = [
                army for army in player_m.armys if army.current_province == province
            ]
            if len(armies) > 1:
                for army in armies:
                    if isinstance(army, Army_Group):
                        self.add_army_to_group(player_m)
                    else:
                        self.create_group_army(player_m)
        return

    def create_group_army(self, player_m):
        for province in player_m.provinces:
            armies = [
                army for army in player_m.armys if army.current_province == province
            ]
            if len(armies) > 1:
                player_m.armys.append(
                    Army_Group(
                        province,
                        player_m,
                    )
                )
                for army in armies:
                    player_m.armys[-1].add_army(army)
                    player_m.armys.remove(army)

        return

    def add_army_to_group(self, player_m):
        # Check if there is an existing Army_Group
        for province in player_m.provinces:
            for army in player_m.armys:
                if isinstance(army, Army_Group):
                    a_grp = army
                    if a_grp.current_province == province:
                        for army in player_m.armys:
                            if (
                                army.current_province == province
                                and army not in a_grp.armys
                                and army != a_grp
                            ):
                                a_grp.add_army(army)
                                player_m.armys.remove(army)
        return

