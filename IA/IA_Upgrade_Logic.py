from math import log


class Upgrade_Logic:
    def __init__(self, player) -> None:
        self.player = player

    def get_province_value(self, provinces):
        provinces_value = []
        for province in provinces:
            provinces_value.append(
                (province, self.obtain_province_value(province))
            )
        provinces_value.sort(key=lambda x: x[1], reverse=True)
        return provinces_value[0]

    def obtain_province_value(self, province):
        def get_neighbors_value(province) -> int:
            neighbors = province.get_neighbors()
            value = 0
            for neighbor in neighbors:
                if neighbor.get_owner() != self.player:
                    value += 1
            return value

        def neighbors_enemy_level_comparison(province) -> bool:
            neighbors = province.get_neighbors()
            for neighbor in neighbors:
                if neighbor.get_owner() != self.player:
                    if neighbor.get_level() > province.get_level():
                        return True
            return False

        def enemy_army_in_neighbors(province) -> int:
            neighbors = province.get_neighbors()
            value = 0
            for neighbor in neighbors:
                if neighbor.get_owner() != self.player:
                    if neighbor.get_armys():
                        for army in neighbor.get_armys():
                            value += army.get_army_quant()
            return value

        def enemy_level_in_neighbors(province) -> int:
            neighbors = province.get_neighbors()
            value = 0
            for neighbor in neighbors:
                if neighbor.get_owner() != self.player:
                    value += neighbor.get_level()
            return value

        def calculate_enemy_army_modifier(province):
            enemy_army_count = enemy_army_in_neighbors(province)
            if enemy_army_count != 0:
                return log(enemy_army_count, 50)
            else:
                return 0

        province_level_modifier = 1 / province.get_level()
        neighbors_enemy_level_modifier = 0.15 * \
            enemy_level_in_neighbors(province)
        terrain_modifier = 1 - province.get_terrain().get_upgrade_modifier()
        neighbors_province_count_modifier = 0.25 * \
            get_neighbors_value(province)
        enemy_army_in_neighbors_modifier = calculate_enemy_army_modifier(
            province)
        highest_level_neighbor_modifier = 0.50 if neighbors_enemy_level_comparison(
            province) else 0

        value = province_level_modifier + neighbors_enemy_level_modifier + terrain_modifier + \
            neighbors_province_count_modifier + \
            enemy_army_in_neighbors_modifier + highest_level_neighbor_modifier

        return value


"""
Fatores que influenciam a decisão de fazer um upgrade de província:

- Nível da província (check)
- Nível dos vizinhos (check)
- Modificador de terreno (check)
- Quantidade de províncias vizinhas inimigas (check)
- Quantidade de exército aliado na província (check)
- Quantidade de exército inimigo na província vizinhas

Inverso do modificador de terreno(Quanto maior o modificador, menor a pontuação)
Progressivo ao número de provícias inimigas vizinhas
Progressivo ao número de exércitos inimigos na província vizinha
Inverso a quantidade de exércitos aliados na província
Progressivo ao nível da província
"""
