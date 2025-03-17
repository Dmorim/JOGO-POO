from Player import Player
from Army import Army_Group


class ArmyGroupCheck:
    def __init__(self):
        pass

    def __army_creation(self, player):
        for province in player.get_player_province():
            province.produce_army()

    def __create_groups_of_armys(self, player):
        for province in player.get_player_province():
            if province.get_available_armys() > 1:
                armies = province.get_available_armys()
                army_group = self.__find_or_create_army_group(province, armies)
                self.__add_armies_to_group(army_group, armies)

    def __add_armies_to_group(self, army_group: Army_Group, armies: list):
        for army in armies:
            if not isinstance(army, Army_Group):
                army_group.add_army(army)
                army.get_owner().remove_army(army)

    def __find_or_create_army_group(self, province, armies):
        for army in armies:
            if isinstance(army, Army_Group):
                return army
        return Army_Group(province, armies[0].get_owner())
    
    def group_checks(self, player: Player):
        self.__army_creation(player)
        self.__create_groups_of_armys(player)
