from math import log


from Army import Army_Group


class Heal_Logic:
    def __init__(self, player):
        self.__player = player

    @property
    def player(self):
        return self.__player

    def health_ratio_diferential(self, army):
        return army.get_health() / army.get_max_health()

    def get_province_level_from_army(self, army):
        return army.get_province().get_level()

    def combined_army_status_ratio(self, army):
        return (army.get_attack() + army.get_defense()) / 2

    def in_battle_neighbour_provinces(self, army):
        return any([province.get_in_battle() for province in army.get_province().get_neighbors()])

    def healing_time(self, army):
        if isinstance(army, Army_Group):
            heal_values = army.heal_army_value()
            average_heal_value = sum(heal_values) / len(heal_values)
            avarage_max_health = army.get_max_health() / army.get_army_quant()
            avarage_army_health = army.get_health() / army.get_army_quant()
            average_healing_need = avarage_max_health - avarage_army_health
            return average_healing_need / average_heal_value
        else:
            return army.get_health() / army.heal_army_value()

    def enemy_armys_in_neighbour_provinces(self, army):
        value = 0
        for province in army.get_province().get_neighbors():
            for armie in province.get_armys():
                if armie.get_owner() != army.get_owner():
                    value += armie.get_army_quant()

        return value

    def obtain_log_value(self, value, base):
        if value != 0:
            return log(value, base)
        else:
            return 0

    def get_healing_logic_value(self, army: list):
        army_values = []
        for armie in army:
            army_values.append((armie, self.obtain_healing_logic_value(armie)))
            army_values.sort(key=lambda x: x[1], reverse=True)
        return army_values[0]

    def obtain_healing_logic_value(self, army):
        health_ratio_modifier = 1 - self.health_ratio_diferential(army)
        army_size_modifier = self.obtain_log_value(army.get_army_quant(), 50)
        province_level_modifier = 0.22 * \
            (self.get_province_level_from_army(army))
        army_status_modifier = self.obtain_log_value(
            self.combined_army_status_ratio(army), 50)
        neighbour_battle_modifier = 0.4 if self.in_battle_neighbour_provinces(
            army) else 0
        healing_time_modifier = 1 / (1.25 + self.healing_time(army))
        enemy_armys_modifier = self.obtain_log_value(
            self.enemy_armys_in_neighbour_provinces(army), 50)

        value = health_ratio_modifier + army_size_modifier + province_level_modifier + \
            army_status_modifier + neighbour_battle_modifier + \
            healing_time_modifier + enemy_armys_modifier

        return value


"""
Fatores a serem considerados:
- Diferença entre vida atual e vida máxima
- Tamanho do exército a ser curado
- Nível da província atual
- Combinação dos status de ataque e defesa
- Província vizinha em batalha
- Tempo necessário para curar o exército
- Quantidade de exércitos inimigos nas províncias vizinhas.

"""
