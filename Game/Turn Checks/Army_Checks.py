from Player import Player


class ArmyChecks:
    def __init__(self):
        pass

    def __army_creation(self, player):
        for province in player.get_player_province():
            province.produce_army()
            
    def __create_groups_of_armys(self, player):
        for province in player.get_player_province():
            if province.armys_in_province() > 1:
                province.group_army()

    def army_checks(self, player: Player):
        self.__army_creation(player)
