from Army import Army


class Player:
    def __init__(self, name: str):
        self.name = name
        self.provinces = []
        self.armys = []
        self.actions = 0
        self.ia = None

    def add_province(self, province: object):
        self.provinces.append(province)

    def remove_province(self, province: object):
        self.provinces.remove(province)

    def add_army(self, army):
        self.armys.append(army)

    def remove_army(self, army):
        self.armys.remove(army)

    def get_player_province(self):
        return self.provinces

    def get_player_name(self):
        return self.name

    def get_player_actions(self):
        return self.actions

    def get_armys(self):
        return self.armys

    def get_no_move_armys(self):
        return [army for army in self.armys if not army.get_in_move()]

    def action_move_army(self):
        if self.actions >= 0.75:
            self.actions -= 0.75
            return True
        return False

    def action_upgrade_province(self, province):
        modi = self.get_upgrade_cost(province)
        if self.actions >= modi:
            self.actions -= modi
            return True
        return False

    def get_upgrade_cost(self, province):
        modi = province.get_terrain().get_upgrade_modifier()
        return round(2 * modi, 2)

    def action_heal_army(self):
        if self.actions >= 0.75:
            self.actions -= 0.75

    def can_perform_action(self):
        return self.actions > 0

    def army_creation(self, province: object):
        army_created = Army(province, self)
        self.add_army(army_created)

    def remove_army_from_group(self, army_group: object, armies: list):
        for army in armies:
            removed = army_group.remove_army(army)
            if removed is not None:
                self.add_army(army)

    def no_battle_province(self):
        pov = []
        for province in self.provinces:
            if province.get_in_battle() is False:
                pov.append(province)
        return pov

    def wound_army(self):
        return [
            army
            for army in self.armys
            if army.get_health() != army.get_max_health()
            and not army.get_in_healing()
            and not army.get_in_move()
            and not army.get_province().get_in_battle()
        ]

    def get_ia(self):
        return self.ia

    def set_ia(self, ia):
        self.ia = ia

    def no_battle_armies(self):
        return [army for army in self.armys if not army.get_province().get_in_battle()]

    def get_army_in_move(self):
        return [army for army in self.armys if army.get_in_move()]

    def get_army_in_healing(self):
        return [
            army
            for army in self.armys
            if army.get_in_healing()
            and not army.get_in_move()
            and not army.get_in_battle()
        ]

    def get_available_army(self):
        return [
            army
            for army in self.armys
            if not army.get_in_move() and not army.get_in_battle()
        ]

    def get_available_province(self):
        return [
            province
            for province in self.provinces
            if not province.get_in_battle()
            and province.get_owner() == self
            and province.get_dom_turns() == 0
            and province.get_level() < province.get_level_cap()
        ]

    def get_no_healing_armys(self):
        return [army for army in self.armys if not army.get_in_healing()]
