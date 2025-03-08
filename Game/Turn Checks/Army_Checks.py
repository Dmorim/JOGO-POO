from Player import Player
from Army import Army_Group


class ArmyChecks:
    def __init__(self):
        self.constant_army_move_points = 5

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

    def __army_move_points(self, player):
        for army in player.get_armys():
            army.set_moving_points(self.constant_army_move_points)

    def __turn_healing(self, player):
        for army in player.get_army_in_healing():
            army.heal_army_action()

    def update_movement_turns(self, player_m):
        for army in player_m.get_army_in_move():
            if self.verify_battle(army):
                army.turns_to_move -= 1
                if army.turns_to_move == 0:
                    self.army_into_province(army)

        for province in player_m.provinces:
            if province.get_dom_turns() > 0:
                province.update_dom_turns()

    def verify_battle(self, selected_army):
        if selected_army.dest_province.get_in_battle():
            for battle in self.game.ongoing_battles:
                if battle.get_province() == selected_army.dest_province:
                    if (
                        battle.get_off_army_owner() != selected_army.get_owner()
                        and battle.get_def_army_owner() != selected_army.get_owner()
                    ):
                        selected_army.cancel_movement()
                        return False
        return True


    def army_checks(self, player: Player):
        self.__army_creation(player)
        self.__create_groups_of_armys(player)
        self.__army_move_points(player)
        self.__turn_healing(player)
