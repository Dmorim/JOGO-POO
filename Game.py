from collections import defaultdict
from Army import Army_Group


class Game:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.mapmode = True
        self.turn_count = 0
        self.move_on = False

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_turn_count(self):
        return self.turn_count

    def start(self):
        # Initialize game state
        self.current_player = self.players[0]

    def end(self):
        # Check if any player has conquered all provinces
        for player in self.players:
            if len(player.provinces) == 0:
                return True
        return False

    def update_movement_turns(self):
        for player in self.players:
            for army in player.armys:
                if army.in_move:
                    army.turns_to_move -= 1
                    if army.turns_to_move == 0:
                        army.in_move = False
                        army.current_province = army.dest_province
                        army.dest_province = None
                        army.turns_to_move = None

    def next_turn(self):
        # Switch to the next player
        self.update_movement_turns()
        current_index = self.players.index(self.current_player)
        next_index = (current_index + 1) % len(self.players)
        self.current_player = self.players[next_index]
        self.turn_count += 1

    def play(self):
        # Main game loop
        while not self.end():
            # Perform player actions
            for player in self.players:
                self.current_player = player
                player.actions += 3
                self.mapmode = True
                self.army_move_points()

                while player.can_perform_action():
                    # Perform action based on player's choice
                    if self.mapmode:
                        self.print_map()
                    action = input("Escolha uma opção: ")
                    if action == "1":
                        self.army_actions(self.current_player)
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

    def army_move_points(self):
        for army in self.current_player.get_armys():
            army.move_points = 4
            if army.in_move:
                army.move_points = 0

    def army_creation(self, player_m):
        for province in player_m.get_player_province():
            province.produce_army()
            if player_m.armys:
                print(
                    f"Exército criado em: {province.name} com {player_m.armys[-1].attack} de ataque e {player_m.armys[-1].defense} de defesa"
                )

    def army_actions(self, player_m):
        # Implement troop movement logic
        if player_m.get_armys():
            print("Exércitos disponíveis: ")
            for army in player_m.get_armys():
                if isinstance(army, Army_Group):
                    print(
                        f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}, Província: {army.current_province.name}, ({player_m.armys.index(army) + 1})"
                    )
                else:
                    print(
                        f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Vida: {army.get_health()}. Província: {army.get_province().get_name()}, ({player_m.get_armys().index(army) + 1})"
                    )
            selected_army = input()
            if int(selected_army) <= len(player_m.armys) + 1:
                selected_army = player_m.armys[int(selected_army) - 1]
                print(
                    f"Província atual: {selected_army.get_province().get_name()}, Vizinhos: {[neighbor.get_name() for neighbor in selected_army.get_province().get_neighbors()]}"
                )

                print("Ações disponíveis:\n1 - Mover Exército")
                army_actions = input()
                if army_actions == "1":
                    self.army_movement(player_m, selected_army)
        else:
            print("Não há exércitos disponíveis.")

    def upgrade_province(self, player_m):
        # Implement province upgrade logic
        index_list = [
            player_m.get_player_province().index(province) + 1
            for province in player_m.provinces
        ]
        up_prov = input(
            f"Selecione a província para ser melhorada: {[f'{province.get_name()} ({player_m.get_player_province().index(province) + 1})' for province in player_m.get_player_province()]} "
        )
        if int(up_prov) in index_list:
            action = player_m.action_upgrade_province(
                player_m.get_player_province()[index_list.index(int(up_prov))]
            )
            if action:
                player_m.get_player_province()[index_list.index(int(up_prov))].upgrade()
                print(
                    player_m.get_player_province()[index_list.index(int(up_prov))].level
                )
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
            print(f"Jogador: {player.get_player_name()}")
            for province in player.get_player_province():
                print(
                    f"Província: {province.get_name()}, Terreno: {province.get_terrain().get_terrain_name()}. (Nível: {province.get_level()})\nVizinhos: {', '.join(neighbor.get_name() for neighbor in province.get_neighbors())}"
                )
                if player.get_armys():
                    armies = [
                        army
                        for army in player.get_armys()
                        if army.get_province() == province
                    ]
                    for army in armies:
                        if isinstance(army, Army_Group):
                            print(
                                f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}. {'(' if army.in_move == True else ''}{army.turns_to_move if army.in_move == True else ''} {'Turnos para chegar em' if army.in_move == True else ''} {army.dest_province.name if army.in_move == True else ''}{')' if army.in_move == True else ''}"
                            )
                        else:
                            print(
                                f"Exército: Ataque: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}. {'(' if army.in_move == True else ''}{army.turns_to_move if army.in_move == True else ''} {'Turnos para chegar em' if army.in_move == True else ''} {army.dest_province.name if army.in_move == True else ''}{')' if army.in_move == True else ''}"
                            )
            print()
        print(f"Jogador Atual: {self.current_player.get_player_name()}")
        print(f"Pontos de Ação: {self.current_player.get_player_actions()}\n")

    def group_army(self, player_m):
        for province in player_m.provinces:
            armies = [
                army for army in player_m.armys if army.get_province() == province
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
                army for army in player_m.armys if army.get_province() == province
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
        for province in player_m.get_player_province():
            for army in player_m.get_armys():
                if isinstance(army, Army_Group):
                    a_grp = army
                    if a_grp.get_province() == province:
                        for army in player_m.armys:
                            if (
                                army.get_province() == province
                                and army not in a_grp.get_armys()
                                and army != a_grp
                            ):
                                a_grp.add_army(army)
                                player_m.armys.remove(army)
        return

    def army_movement(self, player_m, selected_army):
        print("Selecione a província de destino do exército:")
        for neighbor in selected_army.get_province().get_neighbors():
            print(
                f"{neighbor.get_name()}, {neighbor.get_terrain().get_terrain_name()}: ({selected_army.get_province().get_neighbors().index(neighbor) + 1}) "
            )
        move_to = input()
        if int(move_to) <= len(selected_army.get_province().get_neighbors()) + 1:
            cond = player_m.action_move_army()
            if cond:
                self.army_make_movement(selected_army, move_to)
        else:
            print("Província inválida")

    def army_make_movement(self, selected_army, move_to):
        dest_prov = selected_army.get_province().get_neighbors()[int(move_to) - 1]
        move_needed = round(
            selected_army.get_province().get_move_req()
            * selected_army.get_province().get_terrain().get_move_modifier()
            + (dest_prov.get_move_req() * dest_prov.get_terrain().get_move_modifier()),
            0,
        )
        move_points = selected_army.get_move_points()
        turns_to_move = round(move_needed / move_points, 0)
        selected_army.turns_to_move = turns_to_move
        selected_army.dest_province = dest_prov
        selected_army.in_move = True
