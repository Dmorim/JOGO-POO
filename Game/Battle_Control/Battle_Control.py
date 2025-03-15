from Battle import Battle


class BattleControl:
    _isInstance = None

    def __new__(cls):
        if cls._isInstance is None:
            cls._isInstance = super().__new__(cls)
        return cls._isInstance

    def __init__(self):
        self.__ongoing_battles = {}  # Dicionário para batalhas em andamento
        self.__finished_battles = {}  # Dicionário para batalhas finalizadas

    @property
    def ongoing_battles(self):
        return self.__ongoing_battles

    @property
    def finished_battles(self):
        return self.__finished_battles

    def __army_into_battle(self, province, army):
        battle = self.get_ongoing_battle(province)
        if battle.get_off_army_owner() == army.get_owner():
            battle.add_off_army(army)
        else:
            battle.add_def_army(army)
        return print(
            f"Exército de {army.get_owner().get_player_name()} entrou em batalha em {province.get_name()}")

    def __create_battle(self, province, army):
        battle = Battle(army.get_owner(), province.get_owner(), province)
        battle.start_battle()
        self.add_ongoing_battle(province, battle)

    def __return_battle_owner(self, province, army):
        battle = self.get_ongoing_battle(province)
        if battle.get_off_army_owner() == army.get_owner():
            return battle.get_off_army_owner()
        return battle.get_def_army_owner()

    def add_ongoing_battle(self, province, battle):
        if province in self.ongoing_battles:
            raise ValueError("Provincia já está em batalha")
        self.ongoing_battles[province] = battle

    def finish_battle(self, province):
        battle = self.ongoing_battles.pop(province, None)
        if battle:
            if province not in self.finished_battles:
                self.finished_battles[province] = []
            self.finished_battles[province].append(battle)
        province.set_in_battle(False)

    def get_ongoing_battle(self, province):
        return self.ongoing_battles.get(province)

    def get_finished_battles(self, province):
        return self.finished_battles.get(province, [])

    def is_battle_ongoing(self, province):
        return province in self.ongoing_battles

    def is_battle_finished(self, province):
        return province in self.finished_battles

    def handle_battle(self, province, army):
        if self.is_battle_ongoing(province):
            return self.__army_into_battle(province, army)

        self.__create_battle(province, army)

    def remove_army_from_battle(self, province, army):
        """
        Remove um exército de uma batalha em andamento na província especificada.

        Args:
            province (Province): A província onde a batalha está ocorrendo.
            army (Army): O exército que está sendo removido da batalha.

        Returns:
            None
        """
        battle = self.get_ongoing_battle(province)
        if battle is None:
            raise ValueError(
                "Nenhuma batalha em andamento na província especificada")

        owner = self.__return_battle_owner(province, army)

        if owner == battle.get_off_army_owner():
            if army in battle.get_off_army():
                battle.remove_off_army(army)
            else:
                raise ValueError(
                    "O exército não está na lista de exércitos atacantes")
        else:
            if army in battle.get_def_army():
                battle.remove_def_army(army)
            else:
                raise ValueError(
                    "O exército não está na lista de exércitos defensores")
