from Battle import Battle


class BattleUpdater:
    def __init__(self, battle_control, battle_finisher):
        self.battle_control = battle_control
        self.battle_finisher = battle_finisher

    def check_owner_battle_update(self, battle: Battle, player):
        if battle.get_province().get_owner() == player:
            return self.battle_turn(battle)

    def battle_turn(self, battle: Battle):
        return battle.battle_going()

    def update_battles(self, player):
        for battle in self.battle_control.get_ongoing_battles():
            update_battle = self.check_owner_battle_update(battle, player)
            if update_battle is True:
                self.battle_control.finish_battle(battle.get_province())
                self.battle_finisher.finish_battle(battle)
