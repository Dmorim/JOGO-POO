

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
        value = 0


"""
Fatores que influenciam a decisão de fazer um upgrade de província:

- Nível da província
- Nível dos vizinhos
- Modificador de terreno
- Quantidade de províncias vizinhas inimigas
- Quantidade de exército aliado na província
- Quantidade de exército inimigo na província vizinhas

"""
