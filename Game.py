from Army import Army_Group
from Battle import Battle


class Game:
    class Moviment:
        def __init__(self, game, enemy_territory_mod=1.60, friendly_territory_mod=1):
            self.enemy_territory_modifier = enemy_territory_mod
            self.friendly_territory_modifier = friendly_territory_mod
            self.game = game

        def army_make_movement(self, selected_army, move_to, destination=None):
            if destination is not None:
                dest_prov = destination
            else:
                dest_prov = selected_army.get_province().get_neighbors()[
                    int(move_to) - 1
                ]
            move_needed = round(
                (
                    selected_army.get_province().get_move_req()
                    * selected_army.get_province().get_terrain().get_move_modifier()
                )
                + (
                    dest_prov.get_move_req()
                    * dest_prov.get_terrain().get_move_modifier()
                    * self.enemy_territory_modifier
                    if dest_prov.get_owner() != selected_army.get_owner()
                    else self.friendly_territory_modifier
                ),
                0,
            )
            move_points = selected_army.get_move_points()
            turns_to_move = round(move_needed / move_points, 0)
            self.game.current_player.action_move_army()
            selected_army.turns_to_move = turns_to_move
            selected_army.dest_province = dest_prov
            selected_army.in_move = True

            print(
                f"Exército em movimento para {selected_army.dest_province.get_name()}. Faltam {
                    selected_army.turns_to_move} turnos para chegar."
            )

        def army_movement(self, player_m, selected_army):
            if selected_army.in_move:
                print(
                    f"Exército em movimento para {selected_army.dest_province.get_name()}. Faltam {
                        selected_army.turns_to_move} turnos para chegar."
                )
                print("Ações disponíveis:\n1 - Cancelar Movimento\n0 - Voltar")
                action = input()
                if action == "1":
                    selected_army.in_move = False
                    selected_army.turns_to_move = None
                    selected_army.dest_province = None
                    print("Movimento cancelado.")
                    self.mapmode = False

                if action == "0":
                    pass
                return

            if selected_army.get_in_healing():
                print("Exército em cura. Não é possível mover.")
                self.mapmode = False
                return

            print("Selecione a província de destino do exército:")
            for neighbor in selected_army.get_province().get_neighbors():
                print(
                    f"{neighbor.get_name()}, {neighbor.get_terrain().get_terrain_name()}: ({
                        selected_army.get_province().get_neighbors().index(neighbor) + 1}) "
                )
            move_to = input()
            if int(move_to) <= len(selected_army.get_province().get_neighbors()) + 1:
                cond = player_m.action_move_army()
                if cond:
                    self.army_make_movement(selected_army, move_to)
                    if player_m.get_player_actions() > 0:
                        self.mapmode = False
            else:
                print("Província inválida")
                self.mapmode = False

        def update_movement_turns(self, player_m):
            for army in player_m.get_army_in_move():
                if self.verify_battle(army):
                    army.turns_to_move -= 1
                    if army.turns_to_move == 0:
                        self.army_into_province(army)

            for province in player_m.provinces:
                if province.get_dom_turns() > 0:
                    province.update_dom_turns()

        def cancel_movement(self, selected_army):
            selected_army.in_move = False
            selected_army.turns_to_move = None
            selected_army.dest_province = None

        def verify_battle(self, selected_army):
            if selected_army.dest_province.get_in_battle():
                for battle in self.game.ongoing_battles:
                    if battle.get_province() == selected_army.dest_province:
                        if (
                            battle.get_off_army_owner() != selected_army.get_owner()
                            and battle.get_def_army_owner() != selected_army.get_owner()
                        ):
                            self.cancel_movement(selected_army)
                            return False
            return True

        def army_into_province(self, selected_army):
            selected_army.in_move = False
            selected_army.current_province = selected_army.dest_province
            if selected_army.dest_province.get_in_battle():
                self.game.check_battles(selected_army)
            elif selected_army.dest_province.get_owner() != selected_army.get_owner():
                self.game.check_battles(selected_army)
            selected_army.dest_province = None
            selected_army.turns_to_move = None

    def __init__(self):
        self.players = []
        self.current_player = None
        self.mapmode = True
        self.turn_count = 0
        self.ongoing_battles = []
        self.finished_battles = []
        self.moviment = self.Moviment(self)
        self.const_army_move_points = 5

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

    def check_battles(self, army):
        if len(self.ongoing_battles) == 0:
            self.create_battle(army)
        else:
            for battle in self.ongoing_battles:
                if battle.province == army.dest_province:
                    if army.get_owner() == battle.off_army_owner:
                        battle.add_off_army(army)
                    else:
                        battle.add_def_army(army)
                else:
                    self.create_battle(army)

    def create_battle(self, army):
        if army.dest_province.get_in_battle():
            return
        battle = Battle(
            army.get_owner(), army.dest_province.get_owner(), army.dest_province
        )
        battle.create_def_army()
        battle.create_off_army()
        battle.province.set_in_battle(True)
        self.add_battle(battle)

    def army_health_check(self):
        for player in self.players:
            for army in player.get_armys():
                if army.get_health() <= 0:
                    player.remove_army(army)

    def unbattle_armys_of_battle(self, battle: object):
        for army in battle.winner.armys:
            if army.get_in_battle():
                army.set_in_battle(False)

    def update_battles(self):
        for battle in self.ongoing_battles:
            if battle.off_army_owner == self.current_player:
                up_bat = battle.battle_going()
                if up_bat is True:
                    self.army_health_check()
                    self.unbattle_armys_of_battle(battle)
                    self.remove_battle(battle)
                    battle.province.set_in_battle(False)
                    if battle.winner == battle.off_army_owner:
                        battle.province.set_current_owner(battle.winner)
                        battle.province.set_dom_turns(3)
                        battle.province.reset_turns_under_control()
                        battle.winner.add_province(battle.province)
                        battle.loser.remove_province(battle.province)

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

    def attack_province(self):
        # Implement province attack logic
        pass

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

                else:
                    self.add_army_to_group(player_m, armies)

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

    def army_split(self, player_m, selected_army):
        if selected_army.get_in_move():
            print("Exército em movimento. Não é possível dividir.")
            return
        if selected_army.get_in_healing():
            print("Exército em cura. Não é possível dividir.")
            return
        if isinstance(selected_army, Army_Group):
            army = selected_army.split_group()
            if army is not None:
                player_m.armys.append(army)
                self.mapmode = False
        else:
            print("Exército não é um grupo.")
            return
        return

    def heal_army(self, selected_army):
        if selected_army.get_in_move():
            print("Exército em movimento. Não é possível curar.")
            self.mapmode = False
            return
        if selected_army.get_in_healing():
            print("Exército já está em cura. Deseja cancelar? (S/N)")
            if input().lower() == "s":
                selected_army.set_in_healing(False)
                print("Cura cancelada.")
            elif input().lower() == "n":
                pass
            else:
                print("Comando inválido.")
            self.mapmode = False
            return
        if selected_army.get_health() == selected_army.get_max_health():
            print("Exército já está com vida máxima.")
            self.mapmode = False
            return
        if selected_army.get_province().get_in_battle():
            print("Exército em batalha, não é possível curar ele")
            self.mapmode = False
            return
        selected_army.set_in_healing(True)
        selected_army.get_owner().action_heal_army()
        print("Exército em cura.")
        self.mapmode = False
        return

    def turn_healing(self, player_m):
        for army in player_m.get_army_in_healing():
            army.heal_army_action()
            if army.get_health() == army.get_max_health():
                army.set_in_healing(False)
