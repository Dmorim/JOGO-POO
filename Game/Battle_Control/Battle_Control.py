class BattleControl:
    def __init__(self):
        self.__ongoing_battles = {}  # Dicionário para batalhas em andamento
        self.__finished_battles = {}  # Dicionário para batalhas finalizadas

    @property
    def ongoing_battles(self):
        return self.__ongoing_battles

    @property
    def finished_battles(self):
        return self.__finished_battles

    def __check_battle_owner(self, province, army):
        battle = self.battle_control.get_ongoing_battle(
            province)
        if battle is not None:
            return True if (battle.get_off_army_owner() != army.get_owner() and battle.get_def_army_owner() != army.get_owner()) else False
        return False

    def __army_cancel_movement(self, army):
        army.cancel_movement()
        print(
            f"Movimento cancelado, devido a batalha em {army.get_destination_province().get_name()}, exército retornou para {army.get_province().get_name()}")

    def __army_into_battle(self, province, army):
        battle = self.get_ongoing_battle(province)
        if battle.get_off_army_owner() == army.get_owner():
            battle.add_off_army(army)
        else:
            battle.add_def_army(army)
        return print(
            f"Exército de {army.get_owner().get_player_name()} entrou em batalha em {province.get_name()}")

    def __create_battle(self, province, army):
        pass

    def add_ongoing_battle(self, province, battle):
        if province in self.ongoing_battles:
            raise ValueError("Provincia já está em batalha")
        self.ongoing_battles[province] = battle

    def finish_battle(self, province):
        battle = self.ongoing_battles.pop(province, None)
        if battle:
            self.finished_battles[province] = battle

    def get_ongoing_battle(self, province):
        return self.ongoing_battles.get(province)

    def get_finished_battle(self, province):
        return self.finished_battles.get(province)

    def is_battle_ongoing(self, province):
        return province in self.ongoing_battles

    def is_battle_finished(self, province):
        return province in self.finished_battles

    def check_battle(self, province, army):
        if self.__check_battle_owner(province, army):
            return self.__army_cancel_movement(army)

        if self.is_battle_ongoing(province):
            return self.__army_into_battle(province, army)

        self.__create_battle(province, army)
