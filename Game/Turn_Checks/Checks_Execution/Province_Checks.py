from Player import Player


class ProvinceChecks:
    def __init__(self):
        pass

    def __update_domination_turns(self, player):
        for province in player.obtain_dominated_provinces():
            province.update_dom_turns()

    def province_checks(self, player: Player):
        self.__update_domination_turns(player)
