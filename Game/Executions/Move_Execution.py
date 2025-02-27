

class Movement:
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
