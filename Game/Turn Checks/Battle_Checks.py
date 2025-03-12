from Battle import Battle
from Player import Player
from Game.Battle_Control import Battle_Control


class Battle_Checks:
    def __init__(self):
        self.battle_control = Battle_Control()

    def __check_army_health(self, player):
        for army in player.get_army_in_battle():
            if army.get_health() <= 0:
                player.remove_army(army)
                self.battle_control.remove_army_from_battle(army)

    def finish_battle(self, battle: Battle):
        battle.finish_battle()

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

    def battle_checks(self, player: Player):
        self.__check_army_health(player)
