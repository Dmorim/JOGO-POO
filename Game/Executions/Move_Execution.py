from multipledispatch import dispatch


class Movement:
    def __init__(self, game, enemy_territory_mod=1.60, friendly_territory_mod=1):
        self.enemy_territory_modifier = enemy_territory_mod
        self.friendly_territory_modifier = friendly_territory_mod
        self.game = game

    def __calculate_necessary_movement(self, selected_army, dest_prov) -> float:
        """
        A função calcula quantos pontos são necessários para mover um exército de uma província para outra.
        Utiliza a fórmula: (movimento necessário da província de origem * modificador de terreno da província de origem) + (movimento necessário da província de destino * modificador de terreno da província de destino * modificador de território inimigo se a província de destino não pertencer ao jogador)

        Args:
            selected_army (army): Exército selecionado para se mover
            dest_prov (province): Província de destino

        Returns:
            float: Pontuação total arredondada.
        """
        score = round(
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
        return score

    def __calculate_turns_to_move(self, selected_army, dest_prov) -> float:
        """
        Função responsável por calcular quantos turnos são necessários para mover um exército de uma província para outra.
        Divide o movimento necessário pelo número de pontos de movimento do exército.
        Args:
            selected_army (army): Exército selecionado para se mover
            dest_prov (province): Província de destino

        Returns:
            float: Numero total de turnos arredondado.
        """
        move_needed = self.__calculate_necessary_movement(
            selected_army, dest_prov)
        move_points = selected_army.get_move_points()
        turns_to_move = round(move_needed / move_points, 0)
        return turns_to_move

    def __set_army_in_move(self, selected_army, dest_prov, turns_to_move):
        """
        Realiza os procedimentos para setar um exército em movimento dentro do jogo.
        Deduz os pontos de ação do jogador, seta a província de destino, os turnos necessários para chegar e o status de movimento do exército.
        Args:
            selected_army (army): Exército selecionado para se mover
            dest_prov (province): Província de destino
            turns_to_move (integer): Quantidade de turnos necessários para chegar na província de destino
        """
        selected_army.get_owner().action_move_army()
        selected_army.initiate_movement(dest_prov, turns_to_move)

    def army_make_movement(self, selected_army, dest_prov):
        """Função chamada para mover um exército de uma província para outra.

        Args:
            selected_army (army): Exército selecionado para se mover
            dest_prov (province): Província de destino
        """
        turns_to_move = self.__calculate_turns_to_move(
            selected_army, dest_prov)
        self.__set_army_in_move(selected_army, dest_prov, turns_to_move)
        print(
            f"Exército em movimento para {selected_army.dest_province.get_name()}. Faltam {
                selected_army.turns_to_move} turnos para chegar."
        )

    def cancel_army_movement(self, selected_army):
        """Função chamada para cancelar o movimento de um exército.

        Args:
            selected_army (army): Exército selecionado para cancelar o movimento
        """
        selected_army.cancel_movement()
        self.game.mapmode = False
        print("Movimento cancelado.")

    def forced_march(self):
        print("Em Desenvolvimento")

    def update_movement_turns(self, player_m):
        for army in player_m.get_army_in_move():
            if self.verify_battle(army):
                army.turns_to_move -= 1
                if army.turns_to_move == 0:
                    self.army_into_province(army)

        for province in player_m.provinces:
            if province.get_dom_turns() > 0:
                province.update_dom_turns()

    def verify_battle(self, selected_army):
        if selected_army.dest_province.get_in_battle():
            for battle in self.game.ongoing_battles:
                if battle.get_province() == selected_army.dest_province:
                    if (
                        battle.get_off_army_owner() != selected_army.get_owner()
                        and battle.get_def_army_owner() != selected_army.get_owner()
                    ):
                        selected_army.cancel_movement()
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
