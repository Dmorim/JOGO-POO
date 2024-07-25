import random


class IA:
    def __init__(self, name, player) -> None:
        self.name = name
        self.player = player
        self.acoes_custo = {"mover": 0.75, "Up_Prov": 1.5, "curar": 0.75, "pular": 0.0}

    def act_choose(self):
        redo = False
        act_points = self.player.get_player_actions()
        acts_ = list(self.acoes_custo.keys())
        act = random.choice(acts_)
        if act == "Up_Prov":
            if len(self.player.no_battle_province()) == 0:
                redo = True
            else:
                prov = random.choice(self.player.no_battle_province())
                self.acoes_custo[act] = self.player.get_upgrade_cost(prov)

        elif act == "mover":
            if len(self.player.get_armys()) == 0:
                redo = True
            elif len(self.player.get_available_army()) == 0:
                redo = True
            elif len(self.player.get_no_healing_armys()) == 0:
                redo = True

        elif act == "curar":
            if len(self.player.wound_army()) == 0:
                redo = True

        if redo:
            return self.act_choose()
        if act_points < self.acoes_custo[act]:
            return self.act_choose()

        if act_points >= self.acoes_custo[act] and act != "Up_Prov" and redo == False:
            return act, None
        elif act_points >= self.acoes_custo[act] and act == "Up_Prov" and redo == False:
            return act, prov

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
