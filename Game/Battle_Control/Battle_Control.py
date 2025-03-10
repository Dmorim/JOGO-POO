class BattleControl:
    def __init__(self):
        self.ongoing_battles = {}  # Dicionário para batalhas em andamento
        self.finished_battles = {}  # Dicionário para batalhas finalizadas

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
