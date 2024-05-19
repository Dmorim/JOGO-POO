import random


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

    def turn_update(self):
        self.turns_count += 1

    def off_damage(self, off_attack_stats, def_defense_stats):
        off_damage = round(
            (
                (
                    (off_attack_stats * self.get_off_diff_health())
                    * random.uniform(0.5, 1.7)
                )
                - (
                    (
                        (
                            def_defense_stats
                            * self.province.get_terrain().get_defence_modifier()
                        )
                        * self.def_diff_health()
                    )
                    * random.uniform(0.4, 1.5)
                )
            ),
            2,
        )
        return off_damage if off_damage > 0 else 0.1

    def def_damage(self, def_attack_stats, off_defense_stats):
        def_damage = round(
            (
                (
                    (def_attack_stats * self.get_def_diff_health())
                    * random.uniform(0.7, 1.1)
                )
                - (
                    (off_defense_stats * self.off_diff_health())
                    * random.uniform(0.5, 1.2)
                )
            ),
            2,
        )
        return def_damage if def_damage > 0 else 0.1

    def health_check(self):
        if self.get_off_actual_health() <= 0:
            self.winner = self.def_army_owner
            return True
        elif self.get_def_actual_health() <= 0:
            self.winner = self.off_army_owner
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

        print(f"Dano do exército atacante: {off_damage}")
        print(f"Dano do exército defensor: {def_damage}")

        off_unit_damage = off_damage / len(self.off_army)
        def_unit_damage = def_damage / len(self.def_army)

        for army in self.off_army:
            army.health_damage(def_unit_damage)

        for army in self.def_army:
            army.health_damage(off_unit_damage)
            
        check = self.health_check()
        if check:
            return True
        return False
