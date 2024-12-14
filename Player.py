from Army import Army


class Player:
    def __init__(self, name: str, move_base_modifier=1.2, upgrade_base_modifier=2.0, heal_base_modifier=0.75):
        self.name = name
        self.provinces = []
        self.armys = []
        self.actions = 0
        self.ia = None
        self.move_base_modifier = move_base_modifier
        self.upgrade_base_modifier = upgrade_base_modifier
        self.heal_base_modifier = heal_base_modifier

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

    def obtain_move_modifier(self):
        return self.move_base_modifier

    def action_move_army(self):
        if self.actions >= self.move_base_modifier:
            self.actions -= self.move_base_modifier
            return True
        return False

    def obtain_upgrade_modifier(self):
        return self.upgrade_base_modifier

    def action_upgrade_province(self, province):
        upgrade_cost = self.get_upgrade_cost(province)
        if self.actions >= upgrade_cost:
            self.actions -= upgrade_cost
            return True
        return False

    def get_upgrade_cost(self, province):
        cost = province.get_terrain().get_upgrade_modifier()
        return round(self.upgrade_base_modifier * cost, 2)

    def obtain_heal_modifier(self):
        return self.heal_base_modifier

    def action_heal_army(self):
        if self.actions >= self.heal_base_modifier:
            self.actions -= self.heal_base_modifier

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

    def get_armys_in_province(self, province):
        return [army for army in self.armys if army.get_province() == province]

    def get_upgrade_province(self):
        return [
            province
            for province in self.provinces
            if province.get_owner() == self
            and province.is_upgradeable()
        ]
