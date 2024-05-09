import random

class Army:
    def __init__(self, current_province, owner, attack=1, defense=1):
        self.attack = round(attack * (random.uniform(0.80, 1.2)), 2)
        self.defense = round(defense * (random.uniform(0.80, 1.2)), 2)
        self.health = 10
        self.current_province = current_province
        self.owner = owner

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_health(self):
        return self.health

    def get_province(self):
        return self.current_province

    def heal_army(self, province):
        self.health += province.level * 1.25

    def set_province(self, province):
        self.current_province = province


class Army_Group(Army):
    def __init__(self, current_province, owner, attack=1, defense=1):
        super().__init__(current_province, owner, attack, defense)
        self.armys = []

    def add_army(self, army):
        self.armys.append(army)

    def get_attack(self):
        return round(sum([army.attack for army in self.armys]), 2)

    def get_defense(self):
        return round(sum([army.defense for army in self.armys]), 2)

    def get_health(self):
        return sum([army.health for army in self.armys])

    def remove_army(self, army):
        self.armys.remove(army)
        return army
