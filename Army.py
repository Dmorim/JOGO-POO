import random


class Army:
    def __init__(self, current_province, owner, attack=1, defense=1):
        self.attack = round(attack * (random.uniform(0.80, 1.2)), 2)
        self.defense = round(defense * (random.uniform(0.80, 1.2)), 2)
        self.health = 10
        self.max_health = 10
        self.current_province = current_province
        self.owner = owner
        self.move_points = 0
        self.in_move = False
        self.in_healing = False
        self.in_battle = False

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_health(self):
        return round(self.health, 2)

    def get_province(self):
        return self.current_province

    def heal_army_value(self):
        healing_value = round(self.get_province().get_level() * 1.25, 2)
        if healing_value >= self.get_health() / 2:
            healing_value = self.get_health() / 2
        if healing_value + self.get_health() >= self.max_health:
            healing_value = self.max_health - self.get_health()
        return healing_value

    def heal_army_action(self):
        self.health += self.heal_army_value()

    def set_province(self, province):
        self.current_province = province

    def get_move_points(self):
        return self.move_points

    def set_move_points(self, move_points):
        self.move_points = move_points

    def group_army(self):
        return Army_Group(self.current_province, self.owner)

    def get_in_move(self):
        return self.in_move

    def get_owner(self):
        return self.owner

    def get_max_health(self):
        return self.max_health

    def health_damage(self, damage):
        self.health -= round(damage, 2)

    def get_in_healing(self):
        return self.in_healing

    def set_in_healing(self, healing):
        self.in_healing = healing

    def get_in_battle(self):
        return self.in_battle

    def set_in_battle(self, battle: bool):
        self.in_battle = battle

    def get_army_quant(self):
        return 1


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
        return round(sum([army.health for army in self.armys]), 2)

    def get_max_health(self):
        return round(sum([army.max_health for army in self.armys]), 2)

    def remove_army(self, army):
        self.armys.remove(army)
        return

    def get_armys(self):
        return self.armys

    def transfer_army(self, army_group):
        army_group.armys.extend(self.get_armys())
        self.armys = []

    def health_damage(self, damage):
        for army in self.armys:
            army.health -= round(damage, 2)

    def split_group(self):
        print("Informe a quantidade de exércitos que deseja dividir: ")
        quant = int(input())
        if quant >= len(self.armys):
            print("Quantidade de exércitos maior que a quantidade atual.")
            return
        if quant <= 0:
            print("Quantidade de exércitos inválida.")
            return
        new_group = Army_Group(self.current_province, self.owner)
        for i in range(quant):
            new_group.add_army(self.armys.pop())

        return new_group

    def heal_army_value(self):
        heal_army_value = []
        for army in self.armys:
            healing_value = round(self.get_province().get_level() * 1.25, 2)
            if healing_value >= army.get_health() / 2:
                healing_value = army.get_health() / 2
            if healing_value + army.get_health() >= army.max_health:
                healing_value = army.max_health - army.get_health()
            heal_army_value.append(healing_value)
        return heal_army_value

    def heal_army_action(self):
        for i, army in enumerate(self.armys):
            army.health += self.heal_army_value()[i]

    def get_neighbours_provinces(self):
        return self.current_province.get_neighbors()

    def get_army_quant(self):
        quant = 0
        for army in self.armys:
            quant += army.get_army_quant()
        return quant
