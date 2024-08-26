import random


class IA:
    def __init__(self, name, player) -> None:
        self.name = name
        self.player = player
        self.acoes_custo = {"mover": 0.75, "Up_Prov": 1.5, "curar": 0.75, "pular": 0.0}
        self.acoes_weight = {"mover": 1, "Up_Prov": 1, "curar": 1, "pular": 0.5}

    def get_army_value(self, army_list):
        def sum_val(army):
            army_health_modifier = 1 - (army.get_health() / army.get_max_health())
            army_stats_modifier = (army.get_attack() + army.get_defense()) / 10
            army_size_modifier = 1 / (1 - (army.get_army_quant() / 100)) / 10
            calc_val = (
                0 - army_health_modifier + army_stats_modifier + army_size_modifier
            )
            return calc_val

        max_val = float("-inf")
        best_army = None

        for army in army_list:
            current_value = sum_val(army)
            if current_value > max_val:
                max_val = current_value
                best_army = army

        return best_army

    def get_province_value(self, army):
        def army_health(army, comparer):
            total_health = 0
            actual_health = 0
            for armies in army:
                if armies.get_owner() == comparer:
                    total_health += armies.get_max_health()
                    actual_health += armies.get_health()
            return actual_health, total_health

        def defence_val(army, comparer):
            defence_value = 0
            for armies in army:
                if armies.get_owner() == comparer:
                    defence_value += armies.get_defense()
            return defence_value

        def province_verifier(province, owner):
            army_quant = []
            for province in province.get_neighbors():
                if province.get_owner() != owner:
                    if province.get_armys():
                        army_quant.append(
                            army.get_army_quant() for army in province.get_armys()
                        )
            return army_quant

        def army_province_verifier(army_quanti, province, owner):
            army_quant = province_verifier(province, owner)
            for i in army_quant:
                if army_quanti > army_quanti:
                    return True
            return False

        def calc_base_weight(**kwargs) -> float:
            # Obtém a quantidade de exércitos na província
            province_army_count = kwargs.get("province").get_armys()
            army_province_ratio = 1 / (1 + province_army_count)
            
            # Calcula a saúde do exército na província
            province_army_health = kwargs.get("province_army_health")
            province_army_max_health = kwargs.get("province_army_max_health")
            army_health_ratio = province_army_health / province_army_max_health
            
            # Obtém a quantidade de exércitos aliados na província
            allied_army_count = kwargs.get("province_allied_armys_quant")
            allied_army_ratio = 1 / (1 + allied_army_count)
            
            # Verifica se a província está em batalha
            in_battle = kwargs.get("province").get_in_battle()
            battle_modifier = 0.5 if in_battle else 0.0
            
            # Verifica se não há exércitos na província
            province_army_quantity = kwargs.get("province_armys_quant")
            no_army_modifier = 1.0 if province_army_quantity == 0 else 0.0
            
            # Calcula o peso base
            base_weight = (
                (army_province_ratio / 10) +
                army_health_ratio +
                (allied_army_ratio / 10) +
                battle_modifier +
                no_army_modifier
            )
            
            return base_weight

        def calc_enemy_modifier(**kwargs) -> float:
            # Obtém os modificadores e valores necessários dos argumentos
            province = kwargs.get("province")
            province_army_defence = kwargs.get("province_army_defence")
            province_army_health = kwargs.get("province_army_health")
            province_army_quant = kwargs.get("province_army_quant")
            allied_army = kwargs.get("allied_army")

            # Calcula os modificadores individuais
            defense_modifier = 1 - province.get_defence_modifier()
            army_defence_value = province_army_defence / 100
            attack_defence_modifier = (allied_army.get_attack() / province_army_defence) / 10
            attack_health_modifier = (allied_army.get_health() / province_army_health) / 10
            army_quant_modifier = (allied_army.get_army_quant() / province_army_quant) / 10
            terrain_modifier = 1 - province.get_terrain().get_defence_modifier()

            # Soma todos os modificadores para obter o valor final
            total_modifier = (
                defense_modifier
                + army_defence_value
                + attack_defence_modifier
                + attack_health_modifier
                + army_quant_modifier
                + terrain_modifier
            )

            return total_modifier

        def sum_val(province, allied_army):
            owner = province.get_owner()
            province_army = province.get_armys()
            army_size_comparer_modifier = 0.3

            province_army_health, province_army_max_health = army_health(
                province_army, owner
            )
            province_allied_army_health, province_allied_max_health = army_health(
                province_army, self.player
            )
            province_armys_quant = sum(
                army.get_army_quant()
                for army in province.get_armys()
                if army.get_owner() != self.player
            )
            province_allied_armys_quant = sum(
                army.get_army_quant()
                for army in province.get_armys()
                if army.get_owner() == self.player
            )
            province_army_defence = defence_val(province_army, owner)
            province_allied_army_defence = defence_val(province_army, self.player)

            base_weight = calc_base_weight(
                province=province,
                province_army_health=province_army_health,
                province_army_max_health=province_army_max_health,
                province_armys_quant=province_armys_quant,
            )
            if owner != self.player:
                enemy_province_weight = calc_enemy_modifier(
                    province=province,
                    province_army_defence=province_army_defence,
                    allied_army=allied_army,
                    province_armys_quant=province_armys_quant,
                )

                value = 1 + base_weight + enemy_province_weight
            else:
                allied_province_weight = (
                    ((1 - province.get_defence_modifier()) / 3)
                    + (1 / (1 + province_allied_army_defence) / 10)
                    + (1 / (1 + province_allied_armys_quant) / 10)
                    + (1 - (province_allied_army_health / province_allied_max_health))
                    + ((1 - province.get_terrain()) / 3)
                    + army_size_comparer_modifier
                    if army_province_verifier(province_armys_quant, province, owner)
                    else 0.00
                )

                value = 1 + base_weight + allied_province_weight

            return value

        neighbors = army.get_province().get_neighbors()
        max_val = float("-inf")
        best_province = None

        for province in neighbors:
            current_value = sum_val(province, army)
            if current_value > max_val:
                max_val = current_value
                best_province = province

        return best_province, max_val

    def act_choose(self):
        act_points = self.player.get_player_actions()
        acts_ = list(self.acoes_custo.keys())

        for act in acts_:
            if act_points < self.acoes_custo[act]:
                acts_.remove(act)

        for act in acts_:
            match act:
                case "mover":
                    armys = self.player.get_available_army()
                    if not armys:
                        self.acoes_weight[act] = 0
                    else:
                        province, mov_val = self.get_province_value(
                            (self.get_army_value(armys))
                        )
                        print(province.get_name(), mov_val)

    def act_do(self):
        self.act_choose()
        return "Pular", None
        """
        if act == "mover":
            return "Mover", self.act_move()
        elif act == "Up_Prov":
            return "Upgrade", self.act_upgrade(prov)
        elif act == "curar":
            return "Curar", self.act_heal()
        elif act == "pular":
            return "Pular", None
        """

    def act_move(self):
        army = self.player.get_no_move_armys()
        army_choose = random.choice(army)
        province = army_choose.get_province()
        neighbors = province.get_neighbors()
        province_move = random.choice(neighbors)

        return army_choose, province_move

    def act_upgrade(self, prov):
        return prov

    def act_heal(self):
        army = self.player.wound_army()
        heal_army = random.choice(army)
        if heal_army.get_in_healing():
            self.act_heal()
        return heal_army


"""
- Pontuação de ação para realizar a escolha
- Verificar se a ação é possível
- Atribuir ou retirar peso de acordo com a situação
- Escolher a ação

    - Mover
    - Para mover primeiro precisa de um exército disponível
    - Se não tiver exército disponível, a ação de mover não é possível
    - Para selecionar o exército disponível é necessário:
        - Verificar se o exército está em movimento
        - Verificar se o exército está em batalha
        - Verificar se o exército está em cura
        - Verificar se o exército está disponível para mover
        
    - Para encontrar o melhor exército disponível para mover é necessário:
        - Verificar o tamanho do exército
        - Verificar a vida do exército
        - Verificar a força do exército

    -Assumindo que um exército foi escolhido, para encontrar a melhor província para mover é necessário:
        - Verificar a defesa da província
        - Verificar a quantidade de exércitos inimigos na província
        - Verificar a vida dos exércitos inimigos na província
        - Verificar a defesa dos exércitos inimigos na província
        - Verificar o terreno da província
        - Comparar a força do exército com a defesa e o exército da província
        - Verificar qual dos possíveis movimentos é o mais vantajoso
        - Verificar a quantidade de exército aliado na província
        - Verificara existencia de batalhas na provincia envolvendo a IA
    
    - Assumindo que a província e o exército forma escolhidos, a ação de mover deve ganhar uma pontuação com base no quão vantajoso é o movimento
    - A ação de mover deve perder pontos se o movimento não for vantajoso
    - A pontuação da ação de mover deve ser comparada com a pontuação das outras ações
    - A pontuação da ação de mover será igual a maior pontuação das ações possíveis
    
    Sistema de Pontuação para escolher o exército:
        - Pontuação base: 0
        - Dedução pontuação com base na vida:
            - (1 - (vida atual / vida total))
        - Verificação dos valores de ataque e defesa:
            - (Ataque + defesa) / 10
        - Verificação do tamanho do exército:
            - Tamanho / 100
        
        Conclui-se:
            X = 0 + (-(1 - (vida atual/vida total)) + ((ataque + defesa)/10) + (tamanho/100))
            
    Sistema de Pontuação para escolher a província:
        Pontuação base: 1
        
        Variação da pontuação com base na quantidade de exércitos na província:
            - (1 / (1 + (quantidade / 10)))
        Variação da pontuação com base na vida dos exércitos na província:
            - (1 - (vida atual / vida total))
        Variação com base na quantidade de exércitos aliados na província:
            - (1 / (1 + (quantidade / 10))
        Pontuação com base na existência de batalhas na província:
            - 0.5
        Pontuação caso a província tenha exército = 0:
            - 1
            
        Concluí-se:
            Y = (1 / (1 + (quantidade / 10))) + (1 - (vida atual / vida total)) + (1 / (1 + (quantidade / 10)) + 0.5 + 1)
            
        Caso a provincia seja inimiga:
            Variação de pontuação com base no nível de defesa da provincia:
                - (1 - modificador de defesa)
            Variação com base na defesa dos exércitos inimigos na província:
                - (valor de defesa / 100)
            Variação com base na diferença de força entre o exército e a defesa da província:
                - (valor de ataque aliado / valor de defesa inimiga) / 10
            Variação com base na diferença de vida entre o exército e a defesa da província:
                - (vida do exército / vida da defesa) / 10
            Variação com base na diferença de quantidade de exércitos inimigos na província:
                - (quantidade de exércitos aliados / quantidade de exércitos inimigos) / 10
            Variação com base no terreno da província:
                - (1 - terreno)
            
            Conclui-se:
                Y = (1 - modificador de defesa) - (valor de defesa / 100) + ((valor de ataque aliado / valor de defesa inimiga) / 10) + ((vida do exército / vida da defesa) / 10) + ((quantidade de exércitos aliados / quantidade de exércitos inimicos) / 10) - (1 - terreno)
                
        Caso a província seja aliada:
            Variação de pontuação com base no nível de defesa da provincia:
                - ((1 - modificador de defesa) / 3)
            Variação de pontuação com base na defesa dos exercitos aliados na provincia:
                - (( 1 / (1 + defesa)) / 10)
            Variação com base na quantidade de exércitos na província:
                - (1 / (1 + (quantidade / 10)))
            Variação com base na vida dos exércitos na província:
                - (1 - (vida atual / vida total))
            Variacao com base no terreno da província:
                - ((1 - terreno) / 3)
            Pontuação caso exista provincia vizinha com exército maior:
                - 0.3

        
        
        Concluí-se:
            Y = ((1 - modificador de defesa) / 3) + (( 1 / (1 + defesa)) / 10) + (1 / (1 + (quantidade / 10))) + (1 - (vida atual / vida total)) + ((1 - terreno) / 3) + 0.3

"""
