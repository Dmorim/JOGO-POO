from Battle import Battle
from statistics import mean


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

    def predict_battle_winner(self, province):
        if not self.is_battle_ongoing(province):
            return "Nenhuma batalha em andamento nesta província.", ""
        battle = self.get_ongoing_battle(province)
        off_mean = mean(
            battle.off_damage_history) if battle.off_damage_history else 0
        def_mean = mean(
            battle.def_damage_history) if battle.def_damage_history else 0
        if off_mean == def_mean:
            return "A batalha está empatada no momento.", ""
        winner, loser = (
            (battle.get_off_army_owner(), battle.get_def_army_owner())
            if off_mean > def_mean else
            (battle.get_def_army_owner(), battle.get_off_army_owner())
        )
        return (
            f'Previsão: O vencedor provável é {winner.get_player_name()}',
            f'Previsão: O perdedor provável é {loser.get_player_name()}'
        )

    def handle_battle(self, province, army):
        if self.is_battle_ongoing(province):
            return self.__army_into_battle(province, army)

        self.__create_battle(province, army)
