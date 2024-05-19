from collections import defaultdict
from Army import Army_Group


class Game:
    def __init__(self):
        self.players = []
        self.current_player = None
        self.mapmode = True
        self.turn_count = 0
        self.move_on = False
        self.ongoing_battles = []
        self.finished_battles = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def add_battle(self, battle):
        self.ongoing_battles.append(battle)

    def remove_battle(self, battle):
        self.ongoing_battles.remove(battle)
        self.finished_battles.append(battle)

    def get_turn_count(self):
        return self.turn_count

    def start(self):
        # Initialize game state
        self.current_player = self.players[0]

    def end(self):
        # Check if any player has conquered all provinces
        for player in self.players:
            if len(player.get_player_province()) == 0:
                return True
        return False

    def update_movement_turns(self, player_m):
        for army in player_m.armys:
            if army.in_move:
                army.turns_to_move -= 1
                if army.turns_to_move == 0:
                        
                    army.in_move = False
                    army.current_province = army.dest_province
                    army.dest_province = None
                    army.turns_to_move = None

    def next_turn(self):
        # Switch to the next player
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
                self.update_movement_turns(self.current_player)
                self.group_army(self.current_player)
            self.next_turn()

    def army_move_points(self):
        for army in self.current_player.get_armys():
            army.move_points = 5
            if army.in_move:
                army.move_points = 0

    def army_creation(self, player_m):
        for province in player_m.get_player_province():
            vax = province.produce_army()
            if vax:
                print(
                    f"Exército criado em: {province.get_name()} com {player_m.get_armys()[-1].attack} de ataque e {player_m.get_armys()[-1].defense} de defesa"
                )

    def army_actions(self, player_m):
        # Implement troop movement logic
        if player_m.get_armys():
            print("Exércitos disponíveis: ")
            for army in player_m.get_armys():
                if isinstance(army, Army_Group):
                    print(
                        f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}, Província: {army.get_province().get_name()}, ({player_m.armys.index(army) + 1})"
                    )
                else:
                    print(
                        f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Vida: {army.get_health()}. Província: {army.get_province().get_name()}, ({player_m.get_armys().index(army) + 1})"
                    )
            selected_army = input()
            if int(selected_army) <= len(player_m.get_armys()) + 1:
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
            for province in player_m.get_player_province()
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
        print(f"\nTurno: {self.get_turn_count()}")
        print("\nMapa: \n")
        for player in self.players:
            print(f"Jogador: {player.get_player_name()}")
            for province in player.get_player_province():
                print(
                    f"Província: {province.get_name()}, Terreno: {province.get_terrain().get_terrain_name()}. (Nível: {province.get_level()}) Vizinhos: {', '.join(neighbor.get_name() for neighbor in province.get_neighbors())}"
                )
                if player.get_armys():
                    armies = [
                        army
                        for army in player.get_armys()
                        if army.get_province() == province
                    ]
                    for army in armies:
                        if isinstance(army, Army_Group):
                            if len(army.get_armys()) > 0:
                                if army.get_in_move():
                                    print(
                                        f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}. ({army.turns_to_move} Turnos para chegar em {army.dest_province.name})\n"
                                    )
                                else:
                                    print(
                                        f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}. Pertencente a: {army.get_owner().get_player_name()}\n"
                                    )
                        else:
                            if army.get_in_move():
                                print(
                                    f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}. ({army.turns_to_move} Turnos para chegar em {army.dest_province.name})\n"
                                )
                            else:
                                print(
                                    f"Exército: Ataque: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}. Pertencente a: {army.get_owner().get_player_name()}\n"
                                )
            print()
        print(f"Jogador Atual: {self.current_player.get_player_name()}")
        print(f"Pontos de Ação: {self.current_player.get_player_actions()}\n")

    def group_army(self, player_m):
        for province in player_m.provinces:
            armies = [
                army
                for army in player_m.armys
                if army.get_province() == province and army.get_in_move() == False
            ]

            if len(armies) > 1:
                group = None
                for army in armies:
                    if isinstance(army, Army_Group):
                        group = army
                        break

                if group is None:
                    self.create_group_army(player_m, armies)
                    print("Grupo criado")

                else:
                    self.add_army_to_group(player_m, armies)
                    print("Exército adicionado ao grupo")

    def create_group_army(self, player_m, armies):
        army_group = armies[0].group_army()
        player_m.armys.append(army_group)
        for army in armies:
            army_group.add_army(army)
            player_m.armys.remove(army)

    def add_army_to_group(self, player_m, armies):
        # Check if there is an existing Army_Group
        for army in armies:
            if isinstance(army, Army_Group):
                group = army
                break
        for army in armies:
            if army != group:
                if army not in group.get_armys():
                    if not isinstance(army, Army_Group):
                        group.add_army(army)
                        player_m.armys.remove(army)
                    else:
                        army.transfer_army(group)
                        player_m.armys.remove(army)
        return

    def army_movement(self, player_m, selected_army):
        if selected_army.in_move:
            print(
                f"Exército em movimento para {selected_army.dest_province.get_name()}. Faltam {selected_army.turns_to_move} turnos para chegar."
            )
            print("Ações disponíveis:\n1 - Cancelar Movimento\n0 - Voltar")
            action = input()
            if action == "1":
                selected_army.in_move = False
                selected_army.turns_to_move = None
                selected_army.dest_province = None
                print("Movimento cancelado.")

            if action == "0":
                pass
            return

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
            self.mapmode = False

    def army_make_movement(self, selected_army, move_to):
        dest_prov = selected_army.get_province().get_neighbors()[int(move_to) - 1]
        move_needed = round(
            (
                selected_army.get_province().get_move_req()
                * selected_army.get_province().get_terrain().get_move_modifier()
            )
            + (
                dest_prov.get_move_req()
                * dest_prov.get_terrain().get_move_modifier()
                * 1.75
                if dest_prov.get_owner() != selected_army.get_owner()
                else 1
            ),
            0,
        )
        move_points = selected_army.get_move_points()
        turns_to_move = round(move_needed / move_points, 0)
        selected_army.turns_to_move = turns_to_move
        selected_army.dest_province = dest_prov
        selected_army.in_move = True
