

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

        terrain_modifier = 1 - province.get_terrain().get_upgrade_modifier()
        som_enemy_level = enemy_level_in_neighbors(province)
        


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
