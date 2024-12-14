# Classe responsável pela lógica de movimentação da IA
class IA_Move_Logic():

    def __init__(self, player) -> None:  # Construtor da classe
        self.__player = player  # Define o jogador

    @property
    def player(self):  # Propriedade do jogador
        return self.__player

    def obtain_move_requisition_turns_value(self, army, province):
        province_army_move_requisition = army.get_province().get_move_req() * \
            army.get_province().get_terrain().get_move_modifier()

        destination_province_move_requisition = (province.get_move_req(
        ) * province.get_terrain().get_move_modifier()) * 1.6 if province.get_owner() != self.player else 1

        total_requisition = province_army_move_requisition + \
            destination_province_move_requisition
        turns_to_move = round(total_requisition / army.get_move_points(), 0)

        return turns_to_move

    def neighbor_threat_armies(self, army):
        """
        Verifica se o exército está em ameaça por exércitos inimigos com mais quantidade.

        Args:
            army (Object): E exército a ser analisado.

        Returns:
            Boolean: Verdadeiro se o exército estiver em ameaça, falso caso contrário.
        """

        # Define a província atual do exército
        current_province = army.get_province()

        # Verifica se a província atual do exército é nula
        if current_province is None:
            return False

        # Define as províncias vizinhas da província atual do exército
        neighbors = current_province.get_neighbors()

        # Itera sobre as províncias vizinhas
        for province in neighbors:
            # Verifica se a província é inimiga
            if province.get_owner() != self.player:
                # Itera sobre os exércitos na província
                for enemy_army in province.get_armys():
                    # Verifica se o exército é inimigo
                    if enemy_army.get_owner() != self.player:
                        # Verifica se a quantidade de exércitos inimigos é maior que a quantidade do exército
                        if enemy_army.get_army_quant() > army.get_army_quant():
                            # Retorna verdadeiro se o exército estiver em ameaça
                            return True

        # Retorna falso se o exército não estiver em ameaça
        return False

    def get_army_value(self, army_list):
        """
        Avalia uma lista de exércitos e retorna o exército com o maior valor calculado.
        O valor de cada exército é determinado por uma combinação de sua saúde, ataque, defesa 
        e quantidade. O cálculo considera o seguinte:
        - Modificador de saúde: Inversamente proporcional à saúde atual do exército.
        - Modificador de estatísticas: Baseado na soma do ataque e defesa do exército.
        - Modificador de tamanho: Inversamente proporcional à quantidade do exército.
        O exército retornado é tido como o melhor exército para ser movido.
        Args:
            army_list (list): Uma lista de objetos de exército, cada um tendo métodos 
                              get_health(), get_max_health(), get_attack(), get_defense() 
                              e get_army_quant().
        Retorna:
            object: O objeto de exército com o maior valor calculado.


        Evaluates a list of armies and returns the army with the highest calculated value.
        The value of each army is determined by a combination of its health, attack, defense, 
        and quantity. The calculation considers the following:
        - Health modifier: Inversely proportional to the army's current health.
        - Stats modifier: Based on the sum of the army's attack and defense.
        - Size modifier: Inversely proportional to the army's quantity.
        The returned army is considered the best army to be moved.
        Args:
            army_list (list): A list of army objects, each having methods get_health(), 
                              get_max_health(), get_attack(), get_defense(), and get_army_quant().
        Returns:
            object: The army object with the highest calculated value.
        """
        def sum_val(army):
            """
            Calcula o valor de uma instância de Army com base na pontuação de vida, ataque, defesa e quantidade.
            A logica de cálculo é a seguinte:
                - Modificador de vida = O inverso da divisão da vida atual pela vida máxima do exército.
                    Assim o modificador entra negativo para o calculo, desencorajando a IA a escolher exércitos com baixa vida.
                - Modificador de estatísticas = A soma do ataque e defesa do exército dividido por 10.
                    A IA terá prioridade para escolher exércitos com estatísticas mais altas. A divisão por 10 é para reduzir o peso do modificador.
                - Modificador de quantidade = O inverso da quantidade do exército dividido por 100 dividido por 10.
                    A IA terá prioridade para escolher exércitos com maior quantidade. O modificador é dividido para evitar que a quantidade tenha uma progressão de influência muito alta.
                - Modificador de ameaça = 0.05 + Escalamento com a quantidade de exércitos na província.
                    Esse modificador é ativado quando o exército está vizinho a uma provicia inimica com maior quantidade de exércitos que o próprio, evitando a IA de mover exércitos ameaçados e dando prioridade para aqueles que podem reforçar o local.
            Args:
                army (object): Instância de Army.

            Returns:
                calc_val: float: Resultado do cálculo do valor do exército.
            """

            # Define o valor de 100 para balanceamento dos valores calculados
            percent = 100

            # Valores atribuidos a saúde do exército
            ratio_of_health = (army.get_health() / army.get_max_health())

            # Valores atribuidos de ataque e defesa do exército
            sum_of_army_stats = army.get_attack() + army.get_defense()
            mean_of_army_stats = (sum_of_army_stats / 2)
            modifier_of_army_stats = 0.25

            # Valores atribuidos a quantidade do exército
            army_quant = army.get_army_quant() if army.get_army_quant(
            ) != 100 else 101  # Evita divisão por zero

            # Modificadores a serem calculados
            army_health_modifier = 1 - ratio_of_health  # Modificador de saúde

            army_stats_modifier = (sum_of_army_stats +  # Modificador de estatísticas
                                   (mean_of_army_stats * modifier_of_army_stats)) / percent

            # Modificador de tamanho de exército
            army_size_modifier = 1 / (1 - (army_quant / percent)) / 10

            # Modificador de ameaça de exército
            army_threat_modifier = (0.05 + (0.010 * army_quant)) if self.neighbor_threat_armies(
                army) else 0

            # Calcula o valor do exército
            calc_val = (
                0 - army_health_modifier + army_stats_modifier +
                army_size_modifier - army_threat_modifier
            )
            return calc_val

        max_val = float("-inf")  # Define o valor máximo como negativo infinito
        best_army = None  # Define o melhor exército como nulo

        for army in army_list:  # Itera sobre a lista de exércitos
            current_value = sum_val(army)  # Calcula o valor do exército

            if current_value > max_val:  # Verifica se o valor calculado é maior que o valor máximo
                max_val = current_value  # Define o valor máximo como o valor calculado
                best_army = army  # Define o melhor exército como o exército atual)
        # Retorna o melhor exército
        return best_army

    def get_province_value(self, army):
        """
        Avalia as províncias vizinhas da localização do exército selecionado.
        Os parâmetros diferem caso a província seja aliada ou inimiga.
        Os modificadores que interferem na decisão da IA são:
            - Quantidade de exércitos na província.
            - Saúde dos exércitos na província.
            - Estatísticas dos exércitos na província.

        A função contém funções internas que são responsáveis por fazer o cálculo enquanto a função principal organiza e retorna a com maior valor.

        Args:
            army (object): Instância de Army.

        Retorna:
            object: O objeto de província com o maior valor calculado.
        """

        def calc_base_weight(province, province_army_health, province_army_max_health, province_allied_armys_quant) -> float:
            """Essa função calcula o valor base de uma província com base nas estatíscias de exércitos presentes nela
            e em modificadores estacionarios situacionais.

            Args:
                province (Object): Instânca da provincia analisada
                province_army_health (Integer): Vida atual dos exércitos localizados na província
                province_army_max_health (Integer): Vida máxima dos exércitos localizados na província
                province_allied_armys_quant (Integer): Quantidade de exércitos aliados na província

            Returns:
                float: Valor base da província
            """

            # Razão do total de ezércitos na provícia
            army_ratio = (1 / (1 + sum(army.get_army_quant(
            ) for army in province.get_armys())) * 0.90)

            # Razão da vida dos exércitos na província
            army_health_ratio = province_army_health / province_army_max_health

            # Razão dos exércitos aliados na província
            allied_army_ratio = (1 / (1 + sum(army.get_army_quant(
            ) for army in province.get_armys() if army.get_owner() == self.player)) * 0.90)

            # Média das razões dos exércitos
            armys_ratio = (army_ratio + allied_army_ratio) / 2

            distance_modifier = 0.25 * \
                self.obtain_move_requisition_turns_value(army, province)

            # Modificador de batalha
            battle_modifier = 0.3 if province.get_in_battle() else 0.0

            # Modificador de provincia vazia
            no_army_modifier = 1.0 if province_allied_armys_quant == 0 else 0.0

            # Peso base da província
            base_weight = (
                (armys_ratio / 10)
                + army_health_ratio
                + battle_modifier
                + no_army_modifier
                - distance_modifier
            )

            return base_weight

        def calc_enemy_modifier(province, province_army_defence, province_army_health, province_army_quant, allied_army) -> float:
            """Essa função calcula o valor de uma província caso seja inimiga.

            Args:
                province (object): Provincia usada
                province_army_defence (float): Pontuação de defesa dos exércitos na província
                province_army_health (float): Pontuação de vida dos exércitos na província
                province_army_quant (integer): Pontuação de quantidade dos exércitos na província
                allied_army (object): Exército aliado

            Returns:
                float: Valor calculado
            """

            # Modificador de defesa
            defense_modifier = 1 - province.get_defence_modifier()

            # Valor de defesa dos exércitos na província
            army_defence_value = province_army_defence / 100

            # Modificador de ataque e defesa
            attack_defence_modifier = (
                allied_army.get_attack() / province_army_defence) / 10

            # Modificador de vida
            attack_health_modifier = (
                allied_army.get_health() / province_army_health) / 10

            # Modificador de quantidade de exércitos
            army_quant_modifier = (
                allied_army.get_army_quant() / province_army_quant) / 10

            # Modificador de terreno
            terrain_modifier = 1 - province.get_terrain().get_defence_modifier()

            # Calcula o valor total
            total_modifier = (
                defense_modifier
                + army_defence_value
                + attack_defence_modifier
                + attack_health_modifier
                + army_quant_modifier
                + terrain_modifier
            )

            return total_modifier

        def calc_ally_modifier(province, province_allied_army_defence, province_allied_armys_quant, province_allied_army_health, province_allied_max_health, province_armys_quant) -> float:
            """
            Calcula o valor de uma província aliada.

            Args:
                province (Object): Província analisada
                province_allied_army_defence (float): Valor de defesa dos exércitos aliados na província
                province_allied_armys_quant (integer): Quantidade de exércitos aliados na província
                province_allied_army_health (float): Vida dos exércitos aliados na província
                province_allied_max_health (float): Vida máxima dos exércitos aliados na província
                province_armys_quant (integer): Quantidade de exércitos na província

            Returns:
                float: Valor calculado
            """

            def get_enemy_army_quantities(province, owner):
                """
                Função interna que retorna a quantidade de exércitos inimigos nas províncias vizinhas.

                Returns:
                    province (Objetct): Província analisada
                    owner (Object): Dono da província
                """

                return [
                    # Retorna uma lista com as quantidades de exércitos inimigos em províncias vizinhas
                    army.get_army_quant()
                    for neighbor in province.get_neighbors()
                    if neighbor.get_owner() != owner and neighbor.get_armys()
                    for army in neighbor.get_armys()
                ]

            def has_larger_army(army_quantity, enemy_army_quantities):
                """
                Função interna que verifica se o exército aliado é maior que os exércitos inimigos.

                Args:
                    army_quantity (integer): Quantidade de exércitos aliados
                    enemy_army_quantities (List): Lista com as quantidades de exércitos inimigos

                Returns:
                    Boolean: Verdadeiro se o exército aliado for maior que os inimigos, falso caso contrário
                """

                # Verifica se a quantidade de exércitos aliados é maior que a quantidade de exércitos inimigos
                return any(army_quantity > enemy_quantity for enemy_quantity in enemy_army_quantities)

            # Define o dono da província
            owner = province.get_owner()

            # Valor do modificador de defesa -por nível- da província
            defense_modifier = (1 - province.get_defence_modifier()) / 3

            # Razão da estatística de defesa dos exércitos aliados na província
            allied_defence_modifier = 1 / \
                (1 + province_allied_army_defence) / 10

            # Razão da quantidade de exércitos aliados na província
            allied_armys_quant_modifier = 1 / \
                (1 + province_allied_armys_quant) / 10

            # Razão da vida dos exércitos aliados na província
            allied_health_modifier = 1 - \
                (1 - (province_allied_army_health / province_allied_max_health))

            # Modificador de defesa do terreno da província
            terrain_modifier = (
                1 - province.get_terrain().get_defence_modifier()) / 3

            # Variável que armazena a lista com as quantidades de exércitos inimigos nas províncias vizinhas
            enemy_army_quantities = get_enemy_army_quantities(province, owner)

            # Modificador de comparação de tamanho de exércitos
            army_size_comparer_modifier = 0.3 if has_larger_army(
                province_allied_armys_quant, enemy_army_quantities) else 0.0

            # Calcula o valor total
            total_modifier = (
                defense_modifier
                + allied_defence_modifier
                + allied_armys_quant_modifier
                + allied_health_modifier
                + terrain_modifier
                + army_size_comparer_modifier
            )

            # Retorna o valor calculado
            return total_modifier

        def sum_val(province, allied_army):
            """
            Função responsável por obter os valores a serem usados nos cáculos de valor da província, chamar a função
            correta de acordo com o dono da província e retornar o valor final.

            Args:
                province (Object): Província analisada
                allied_army (Object): Exército aliado

            Returns:
                float: Valor calculado
            """

            def army_health(army, owner, origin):
                """
                Função interna que calcula a vida total e a vida atual dos exércitos na província.

                Args:
                    army (Object): Exércitos na província
                    owner (Object): Dono da província
                    origin (String): Origem da chamada da função

                Returns:
                    float: Vida atual e máxima dos exércitos na província
                """
                match origin:
                    case "allied":
                        # Calcula a vida total e a vida atual dos exércitos na província
                        total_health = sum(armies.get_max_health()
                                           for armies in army if armies.get_owner() == owner)
                        actual_health = sum(armies.get_health()
                                            for armies in army if armies.get_owner() == owner)
                    case "enemy":
                        total_health = sum(armies.get_max_health()
                                           for armies in army if armies.get_owner() != owner)
                        actual_health = sum(armies.get_health()
                                            for armies in army if armies.get_owner() != owner)
                    case "all":
                        total_health = sum(armies.get_max_health()
                                           for armies in army)
                        actual_health = sum(armies.get_health()
                                            for armies in army)

                # Retorna a vida atual e a vida total
                return actual_health, total_health

            def defence_val(army, owner):
                """
                Função interna que calcula a defesa total dos exércitos na província.

                Args:
                    army (Object): Exércitos na província
                    owner (Object): Dono da província

                Returns:
                    int: Valor de defesa total
                """
                return sum(armies.get_defense() for armies in army if armies.get_owner() == owner)

            # Define o dono da província
            owner = province.get_owner()

            # Define os exércitos na província
            province_army = province.get_armys()

            # Calcula a vida total e a vida atual dos exércitos na província
            province_army_health, province_army_max_health = army_health(
                province_army, self.player, 'all')

            # Calcula a quantidade de exércitos na província
            province_allied_army_health, province_allied_max_health = army_health(
                province_army, self.player, 'allied')

            # Calcula a quantidade de exércitos inimigos na província
            province_armys_quant = sum(army.get_army_quant(
            ) for army in province.get_armys() if army.get_owner() != self.player)

            # Calcula a quantidade de exércitos aliados na província
            province_allied_armys_quant = sum(army.get_army_quant(
            ) for army in province.get_armys() if army.get_owner() == self.player)

            # Calcula a defesa dos exércitos na província
            province_army_defence = defence_val(province_army, owner)

            # Calcula a defesa dos exércitos aliados na província
            province_allied_army_defence = defence_val(
                province_army, self.player)

            # Calcula o valor base da província
            base_weight = calc_base_weight(
                province=province,
                province_army_health=province_army_health,
                province_army_max_health=province_army_max_health,
                province_allied_armys_quant=province_allied_armys_quant,
            )

            # Verifica se a província é inimiga e chama a função correta
            if owner != self.player:
                enemy_province_weight = calc_enemy_modifier(
                    province=province,
                    province_army_defence=province_army_defence,
                    allied_army=allied_army,
                    province_army_quant=province_armys_quant,
                    province_army_health=province_army_health,
                )
                value = 1 + base_weight + enemy_province_weight

            # Caso a província seja aliada, chama a função correta
            else:
                allied_province_weight = calc_ally_modifier(
                    province=province,
                    province_allied_army_defence=province_allied_army_defence,
                    province_allied_armys_quant=province_allied_armys_quant,
                    province_allied_army_health=province_allied_army_health,
                    province_allied_max_health=province_allied_max_health,
                    province_armys_quant=province_armys_quant,
                )

                value = 1 + base_weight + allied_province_weight

            # Retorna o valor calculado
            return value

        # Define a província atual do exército
        neighbors = army.get_province().get_neighbors()

        # Define o valor máximo como negativo infinito
        max_value = float("-inf")

        # Define a melhor província como nula
        best_province = None

        # Itera sobre as províncias vizinhas
        for province in neighbors:
            # Calcula o valor da província
            current_value = sum_val(province, army)
            if current_value > max_value:
                # Define o valor máximo como o valor calculado se for maior que o valor anteiror, também define a melhor província como a província atual
                max_value = current_value
                best_province = province

        # Retorna a melhor província
        return best_province, army, max_value
