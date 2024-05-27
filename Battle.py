import random
from Army import Army, Army_Group


class Battle:
    def __init__(self, off_owner, def_owner, province):
        self.off_army_owner = off_owner
        self.def_army_owner = def_owner
        self.province = province
        self.off_army = []
        self.def_army = []
        self.turns_count = 0
        self.turns_to_epic = 10
        self.winner = None
        self.loser = None
        self.last_off_damage = 0
        self.last_def_damage = 0

    def create_off_army(self):
        for army in self.off_army_owner.get_armys():
            if army.get_province() == self.province:
                print(army.get_owner().get_player_name())
                self.off_army.append(army)

    def create_def_army(self):
        for army in self.def_army_owner.get_armys():
            if army.get_province() == self.province:
                print(army.get_owner().get_player_name())
                self.def_army.append(army)

    def add_off_army(self, army):
        self.off_army.append(army)

    def add_def_army(self, army):
        self.def_army.append(army)

    def get_off_total_health(self):
        return sum([army.get_max_health() for army in self.off_army])

    def get_off_actual_health(self):
        return sum([army.get_health() for army in self.off_army])

    def get_def_total_health(self):
        return sum([army.get_max_health() for army in self.def_army])

    def get_def_actual_health(self):
        return sum([army.get_health() for army in self.def_army])

    def get_off_total_attack(self):
        return round(sum([army.get_attack() for army in self.off_army]), 2)

    def get_off_total_defense(self):
        return round(sum([army.get_defense() for army in self.off_army]), 2)

    def get_def_total_attack(self):
        return round(sum([army.get_attack() for army in self.def_army]), 2)

    def get_def_total_defense(self):
        return round(sum([army.get_defense() for army in self.def_army]), 2)

    def off_diff_health(self):
        return round(self.get_off_actual_health() / self.get_off_total_health(), 2)

    def def_diff_health(self):
        return round(self.get_def_actual_health() / self.get_def_total_health(), 2)

    def get_province(self):
        return self.province

    def get_turns_count(self):
        return self.turns_count

    def get_epic_turns(self):
        return self.turns_to_epic

    def get_off_army_owner(self):
        return self.off_army_owner

    def get_def_army_owner(self):
        return self.def_army_owner

    def get_winner(self):
        return self.winner

    def get_loser(self):
        return self.loser

    def get_off_army(self):
        return self.off_army

    def get_def_army(self):
        return self.def_army

    def get_last_off_damage(self):
        return self.last_off_damage

    def get_last_def_damage(self):
        return self.last_def_damage

    def total_off_army(self):
        tam = 0
        for army in self.off_army:
            if isinstance(army, Army_Group):
                tam += len(army.armys)
            else:
                tam += 1
        return tam

    def total_def_army(self):
        tam = 0
        for army in self.def_army:
            if isinstance(army, Army_Group):
                tam += len(army.armys)
            else:
                tam += 1
        return tam

    def turn_update(self):
        self.turns_count += 1

    def off_damage(self, off_attack_stats, def_defense_stats):
        off_damage = round(
            (
                (
                    ((off_attack_stats * self.off_diff_health()))
                    * random.uniform(0.6, 1.6)
                )
                - (
                    (
                        (
                            (
                                (
                                    def_defense_stats
                                    * self.province.get_terrain().get_defence_modifier()
                                )
                                * self.province.get_defence_modifier()
                            )
                            * self.def_diff_health()
                        )
                        * random.uniform(0.7, 1.4)
                    )
                )
            ),
            2,
        )
        """
        print(
            f"Dano base do exército atacante: {off_attack_stats * self.off_diff_health()} + diferença de saúde {self.off_diff_health()}"
        )
        print(
            f"Valor base do exército defensor: {(def_defense_stats * self.province.get_terrain().get_defence_modifier()) * self.province.get_defence_modifier()}"
        )
        print(
            f"Valor total do exército defensor: {((def_defense_stats * self.province.get_terrain().get_defence_modifier()) * self.province.get_defence_modifier()) * self.def_diff_health()} + diferença de saúde {self.def_diff_health()}"
        )
        """
        return off_damage if off_damage > 0 else 0.1

    def def_damage(self, def_attack_stats, off_defense_stats):
        def_damage = round(
            (
                (
                    ((def_attack_stats * self.def_diff_health()))
                    * random.uniform(0.6, 1.3)
                )
                - (
                    (
                        off_defense_stats
                        * (self.off_diff_health())
                        * random.uniform(0.5, 1.1)
                    )
                )
            ),
            2,
        )
        return def_damage if def_damage > 0 else 0.1

    def health_check(self):
        if self.get_off_actual_health() <= 0:
            self.winner = self.def_army_owner
            self.loser = self.off_army_owner
            print("Exército atacante derrotado!")
            return True
        elif self.get_def_actual_health() <= 0:
            self.winner = self.off_army_owner
            self.loser = self.def_army_owner
            print("Exército defensor derrotado!")
            return True
        return False

    def battle_going(self):
        self.turn_update()
        off_attack_stats = self.get_off_total_attack()
        def_attack_stats = self.get_def_total_attack()
        off_defense_stats = self.get_off_total_defense()
        def_defense_stats = self.get_def_total_defense()

        off_damage = self.off_damage(off_attack_stats, def_defense_stats)
        def_damage = self.def_damage(def_attack_stats, off_defense_stats)

        if self.get_turns_count() == self.get_epic_turns():
            print("Batalha épica!")
            off_damage *= random.uniform(1.3, 2.8)
            def_damage *= random.uniform(1.3, 2.8)
            off_damage = round(off_damage, 2)
            def_damage = round(def_damage, 2)

        self.last_off_damage = f"Dano do exército atacante: {off_damage}"
        self.last_def_damage = f"Dano do exército defensor: {def_damage}"

        off_unit_damage = off_damage / self.total_off_army()
        def_unit_damage = def_damage / self.total_def_army()

        for army in self.off_army:
            army.health_damage(def_unit_damage)

        for army in self.def_army:
            army.health_damage(off_unit_damage)

        check = self.health_check()
        if check:
            return True
        return False


if __name__ == "__main__":
    print("Teste de Batalhas para obtenção de resultados:")
    from Player import Player
    from Army import Army
    from Province import Province
    from Terrain import Terrain

    atacante = Player("Atacante")
    defensor = Player("Defensor")
    terrain = Terrain("Plains", 1.0, 1.0, 1.0)
    prov = Province("Província", defensor, terrain)
    prov.level = 1

    army_off = Army(prov, atacante)
    army_off2 = Army(prov, atacante)
    army_off3 = Army(prov, atacante)
    army_off4 = Army(prov, atacante)
    army_off5 = Army(prov, atacante)

    army_def = Army(prov, defensor)
    army_def2 = Army(prov, defensor)
    army_def3 = Army(prov, defensor)
    army_def4 = Army(prov, defensor)

    teste = Battle(atacante, defensor, prov)
    teste.add_off_army(army_off)
    # teste.add_off_army(army_off2)
    # teste.add_off_army(army_off3)
    # teste.add_off_army(army_off4)
    # teste.add_off_army(army_off5)

    teste.add_def_army(army_def)
    # teste.add_def_army(army_def2)
    # teste.add_def_army(army_def3)
    # teste.add_def_army(army_def4)

    for i in range(0, 100):
        var = teste.battle_going()
        print(
            f"\nVida do exército atacante: {teste.get_off_actual_health()}\nVida do exército defensor: {teste.get_def_actual_health()}\n"
        )
        if i == 20:
            teste.add_off_army(army_off2)
            teste.add_off_army(army_off3)
            teste.add_off_army(army_off4)
            teste.add_def_army(army_def2)
            teste.add_def_army(army_def3)
            print("Reforços chegaram!")

        if i == 40:
            teste.add_off_army(army_off5)
            teste.add_def_army(army_def4)
            print("Reforços chegaram!")
        if var is True:
            break
