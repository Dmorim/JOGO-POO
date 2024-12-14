from Battle import Battle


class Battle_Execution:
    def __init__(self):
        pass

    def add_battle(self, battle):
        self.ongoing_battles.append(battle)

    def remove_battle(self, battle):
        self.ongoing_battles.remove(battle)
        self.finished_battles.append(battle)

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
