import random


class IA:
    def __init__(self, name, player) -> None:
        self.name = name
        self.player = player
        self.acoes_custo = {"mover": 0.75, "Up_Prov": 1.5, "curar": 0.75, "pular": 0.0}
        self.acoes_weight = {"mover": 1, "Up_Prov": 1, "curar": 1, "pular": 0.5}

    def act_choose(self):
        redo = False
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

    def act_do(self):
        act, prov = self.act_choose()
        print(act)
        if act == "mover":
            return "Mover", self.act_move()
        elif act == "Up_Prov":
            return "Upgrade", self.act_upgrade(prov)
        elif act == "curar":
            return "Curar", self.act_heal()
        elif act == "pular":
            return "Pular", None

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
            
        Caso a provincia seja inimiga:
            Variação de pontuação com base no nível de defesa da provincia:
                - (1 - modificador de defesa)
            Variação com base na defesa dos exércitos inimigos na província:
                - (valor de defesa / 100)
            Variação com base na diferença de força entre o exército e a defesa da província:
                - (valor de ataque aliado / valor de defesa inimiga) / 10
            Variação com base na diferença de vida entre o exército e a defesa da província:
                - (vida do exército / vida da defesa) / 10 
            Variação com base no terreno da província:
                - (1 - terreno)
            
            Conclui-se:
                Y = 1 + (1 / (1 + (quantidade / 10))) + (1 - (vida atual / vida total)) + (1 - (vida atual/vida total) - (valor de defesa/100) - (1 - terreno) + (valor de ataque - valor de defesa)/10) + (vida do exército / vida da defesa) / 10
                
        Caso a província seja aliada:
            Variação de pontuação com base no nível de defesa da provincia:
                - (1 - modificador de defesa)
            Variação com base na defesa dos exércitos aliados na província:
                - (valor de defesa / 100)
            Variação com base na diferença de força entre o exército e a defesa da província:
                - (valor de ataque - valor de defesa)/10
            Variacao com base no terreno da província:
        
        
        
        Concluí-se:
            Y = 1 - (1 - modificador de defesa) - ((0.02 * quantidade)) + (1 - (vida atual/vida total) - (valor de defesa/100) - (1 - terreno) + (valor de ataque - valor de defesa)/10)

"""
