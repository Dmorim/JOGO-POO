class ArmyHealthChecker:
    def check_army_health(self, player):
        for army in player.get_army_in_battle():
            if army.get_health() <= 0:
                player.remove_army(army)