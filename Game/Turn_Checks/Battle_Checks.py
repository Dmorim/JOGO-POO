from Battle import Battle
from Player import Player



class BattleChecks:
    def __init__(self, battle_control, battle_finisher, army_health_checker, battle_updater):
        self.battle_control = battle_control
        self.battle_finisher = battle_finisher
        self.army_health_checker = army_health_checker
        self.battle_updater = battle_updater

    def battle_checks(self, player: Player):
        self.army_health_checker.check_army_health(player)
        self.battle_updater.update_battles(player)
