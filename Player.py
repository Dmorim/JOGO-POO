from Army import Army


class Player:
    def __init__(self, name: str):
        self.name = name
        self.provinces = []
        self.armys = []
        self.actions = 0

    def add_province(self, province: object):
        self.provinces.append(province)

    def remove_province(self, province: object):
        self.provinces.remove(province)

    def add_army(self, army):
        self.armys.append(army)

    def remove_army(self, army):
        self.armys.remove(army)

    def get_provinces(self):
        return self.provinces

    def action_move_army(self):
        if self.actions >= 0.75:
            self.actions -= 0.75

    def action_upgrade_province(self, province: object):
        modi = province.terrain_type.terrain_upgrade_modifier
        if self.actions >= round(1.50 * modi, 2):
            self.actions -= round(1.50 * modi, 2)
            return True
        return False

    def action_attack_province(self):
        if self.actions >= 1:
            self.actions -= 1

    def action_heal_army(self):
        if self.actions >= 0.25:
            self.actions -= 0.25

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
