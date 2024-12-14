from Army import Army_Group
from Battle import Battle
from Game.Move_Execution import Movement


class Game:

    def __init__(self):
        self.players = []
        self.current_player = None
        self.mapmode = True
        self.turn_count = 0
        self.ongoing_battles = []
        self.finished_battles = []
        self.movement = Movement(self)
        self.const_army_move_points = 5

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
            if len(player.get_player_province()) == 0:
                return True
        return False

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

                while self.current_player.can_perform_action():
                    if self.current_player.get_ia() is None:
                        # Perform action based on player's choice
                        if self.mapmode:
                            self.print_map()
                        print(
                            f"{'='*25}\nJogador Atual: {self.current_player.get_player_name()}"
                        )
                        print(
                            f"Pontos de Ação: {
                                round(self.current_player.get_player_actions(), 2)}\n"
                        )
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
                    else:
                        act, var = self.current_player.ia.act_do()
                        if act == "Move":
                            province = var[0][0]
                            army = var[0][1]
                            self.moviment.army_make_movement(
                                army, None, province)
                            print(f"Exército movido para {
                                  province.get_name()}")
                        elif act == "Up_Prov":
                            prov = var[0]
                            self.current_player.action_upgrade_province(prov)
                            self.upgrade_province(self.current_player, prov)
                            print(f"Província {prov.get_name()} melhorada")
                        elif act == "Heal":
                            heal_army = var[0]
                            self.heal_army(heal_army)
                        elif act == "Skip":
                            break

                # Update game state

                self.army_creation(self.current_player)
                self.moviment.update_movement_turns(self.current_player)
                self.update_battles()
                self.group_army(self.current_player)
                self.turn_healing(self.current_player)
                for province in self.current_player.get_player_province():
                    province.increment_turns_under_control()
            self.next_turn()

    def army_move_points(self):
        for army in self.current_player.get_armys():
            army.move_points = self.const_army_move_points
            if army.in_move:
                army.move_points = 0

    def army_creation(self, player_m):
        for province in player_m.get_player_province():
            province.produce_army()

    def army_actions(self, player_m):
        selected_army: str
        # Implement troop movement logic
        if player_m.get_available_army():
            print("Exércitos disponíveis: ")
            for army in player_m.get_available_army():
                if isinstance(army, Army_Group):
                    if army.get_in_healing():
                        print(
                            f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {
                                army.get_health()}, Província: {army.get_province().get_name()} {'(Em Cura)' if army.get_in_healing() else ''}"
                        )
                    else:
                        print(
                            f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}, Província: {
                                army.get_province().get_name()}, ({player_m.get_available_army().index(army) + 1}) {'(Em movimento)' if army.get_in_move() else ''}"
                        )
                else:
                    if army.get_in_healing():
                        print(
                            f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Vida: {army.get_health(
                            )}. Província: {army.get_province().get_name()} {'(Em Cura)' if army.get_in_healing() else ''}"
                        )
                    else:
                        print(
                            f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Vida: {army.get_health()}. Província: {army.get_province(
                            ).get_name()}, ({player_m.get_available_army().index(army) + 1}) {'(Em movimento)' if army.get_in_move() else ''}"
                        )

            selected_army = input()
            if int(selected_army) <= len(player_m.get_available_army()) + 1:
                selected_army = player_m.armys[int(selected_army) - 1]
                print(
                    f"Província atual: {selected_army.get_province().get_name()}, Vizinhos: {
                        [neighbor.get_name() for neighbor in selected_army.get_province().get_neighbors()]}"
                )

                print(
                    "Ações disponíveis:\n1 - Mover Exército\n2 - Dividir Exército\n3 - Curar Exército\n0 - Voltar"
                )
                army_actions = input()
                if army_actions == "1":
                    self.moviment.army_movement(player_m, selected_army)
                elif army_actions == "2":
                    self.army_split(player_m, selected_army)
                elif army_actions == "3":
                    self.heal_army(selected_army)
                elif army_actions == "0":
                    pass

        else:
            print("Não há exércitos disponíveis.")
            self.mapmode = False

    def upgrade_province(self, player_m, province=None):
        if province == None:
            index_list = [
                player_m.get_available_province().index(province) + 1
                for province in player_m.get_available_province()
            ]
            up_prov = input(
                f"Selecione a província para ser melhorada: {[f'{province.get_name()} ({player_m.get_upgrade_cost(province)}), [{
                    player_m.get_available_province().index(province) + 1}]' for province in player_m.get_available_province()]} "
            )
            if int(up_prov) in index_list:
                action = player_m.action_upgrade_province(
                    player_m.get_available_province(
                    )[index_list.index(int(up_prov))]
                )
                if action:
                    player_m.get_available_province()[
                        index_list.index(int(up_prov))
                    ].upgrade()
                else:
                    print("Não há pontos de ação suficientes para realizar a ação.")
                    self.mapmode = False
        else:
            province.upgrade()

    def print_map(self):
        # Print the map with province ownership and armies
        print(f"\nTurno: {self.get_turn_count()}")
        print("\nMapa:")
        for player in self.players:
            print(f"{'-'*110}\nJogador: {player.get_player_name()}\n{'-'*110}")
            for province in player.get_player_province():
                print(
                    f"Província: {province.get_name()}, Terreno: {province.get_terrain().get_terrain_name()}. (Nível: {
                        province.get_level()}) Vizinhos: {', '.join(neighbor.get_name() for neighbor in province.get_neighbors())}"
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
                                        f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense(
                                        )}, Saúde: {army.get_health()}. ({army.turns_to_move} Turnos para chegar em {army.dest_province.name})\n"
                                    )
                                else:
                                    print(
                                        f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {
                                            army.get_defense()}, Saúde: {army.get_health()}. Pertencente a: {army.get_owner().get_player_name()}\n"
                                    )
                        else:
                            if army.get_in_move():
                                print(
                                    f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {
                                        army.get_health()}. ({army.turns_to_move} Turnos para chegar em {army.dest_province.name})\n"
                                )
                            else:
                                print(
                                    f"Exército: Ataque: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {
                                        army.get_health()}. Pertencente a: {army.get_owner().get_player_name()}\n"
                                )
            print()
        if self.ongoing_battles:
            print(f"{'='*25}\nBatalhas em andamento:\n{'='*25}")
            for i, battle in enumerate(self.ongoing_battles):
                print(
                    f"Batalha {i} em {battle.get_province().get_name()} entre {battle.get_off_army_owner().get_player_name()} e {battle.get_def_army_owner().get_player_name()}.\nExército atacante: Quantidade: {battle.total_off_army()}, Ataque: {battle.get_off_total_attack()}, Defesa: {battle.get_off_total_defense()}, Vida: {round(
                        battle.get_off_actual_health(), 2)}, {battle.get_off_army_owner().get_player_name()}\nExército defensor: Quantidade: {battle.total_def_army()}, Ataque: {battle.get_def_total_attack()}, Defesa: {battle.get_def_total_defense()}, Vida: {round(battle.get_def_actual_health(), 2)}, {battle.get_def_army_owner().get_player_name()}"
                )
                print(f"{'='*78}")
                print(battle.get_last_off_damage())
                print(f"{battle.get_last_def_damage()}\n")
                if self.ongoing_battles.index(battle) != len(self.ongoing_battles) - 1:
                    print(f"{'='*78}\n")

    def turn_healing(self, player_m):
        for army in player_m.get_army_in_healing():
            army.heal_army_action()
            if army.get_health() == army.get_max_health():
                army.set_in_healing(False)
