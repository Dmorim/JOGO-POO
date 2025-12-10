import random
from math import sqrt

from Army import Army, Army_Group
from Province import Province


class Battle:
    def __init__(self, off_owner, def_owner, province: Province):
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
        self.damage_multiplier = 1
        self.offensive_defensive_debuff = 1
        self.__off_damage_history = []
        self.__def_damage_history = []

    def create_off_army(self):
        for army in self.off_army_owner.get_armys():
            if army.get_province() == self.province:
                self.off_army.append(army)
                army.set_in_battle(True)

    def create_def_army(self):
        for army in self.def_army_owner.get_armys():
            if army.get_province() == self.province:
                self.def_army.append(army)
                army.set_in_battle(True)

    def add_off_army(self, army):
        self.off_army.append(army)
        army.set_in_battle(True)

    def add_def_army(self, army):
        self.def_army.append(army)
        army.set_in_battle(True)

    def remove_off_army(self, army):
        self.off_army.remove(army)

    def remove_def_army(self, army):
        self.def_army.remove(army)

    def start_battle(self):
        self.create_off_army()
        self.create_def_army()
        self.province.set_in_battle(True)

    def finish_battle(self):
        self.__remove_army_from_battle()
        self.__set_winner_loser()
        self.__update_provinces_after_battle()

    def __remove_army_from_battle(self):
        for army in self.off_army:
            army.set_in_battle(False)
            self.off_army.remove(army)
        for army in self.def_army:
            army.set_in_battle(False)
            self.def_army.remove(army)

    def __set_winner_loser(self):
        if self.get_off_actual_health() > self.get_def_actual_health():
            self.winner = self.off_army_owner
            self.loser = self.def_army_owner
        else:
            self.winner = self.def_army_owner
            self.loser = self.off_army_owner

    def __update_provinces_after_battle(self):
        if self.winner == self.off_army_owner:
            self.province.set_current_owner(self.winner)
            self.province.set_dom_turns(3)
            self.province.reset_turns_under_control()
            self.province.set_in_battle(False)
            self.loser.remove_province(self.province)
            self.winner.add_province(self.province)

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

    def get_off_total_defense(self) -> float:
        return round(sum([army.get_defense() for army in self.off_army]), 2)

    def get_def_total_attack(self):
        return round(sum([army.get_attack() for army in self.def_army]), 2)

    def get_def_total_defense(self) -> float:
        return round(sum([army.get_defense() for army in self.def_army]), 2)

    def off_diff_health(self):
        return round(sqrt(self.get_off_actual_health() / self.get_off_total_health()), 2)

    def def_diff_health(self):
        return round(sqrt(self.get_def_actual_health() / self.get_def_total_health()), 2)

    @property
    def off_damage_history(self):
        return self.__off_damage_history

    @property
    def def_damage_history(self):
        return self.__def_damage_history

    def battle_situation(self):
        battle_situation = f'Batalha em {self.province.get_name()} entre {self.off_army_owner.get_player_name()} e {self.def_army_owner.get_player_name()}'
        attack_situation = f'Exército atacante: Quantidade: {self.total_off_army()}, Ataque: {self.get_off_total_attack()}, Defesa: {self.get_off_total_defense()}, Vida: {round(self.get_off_actual_health(), 2)}'
        defense_situation = f'Exército defensor: Quantidade: {self.total_def_army()}, Ataque: {self.get_def_total_attack()}, Defesa: {self.get_def_total_defense()}, Vida: {round(self.get_def_actual_health(), 2)}'
        return f"{battle_situation}\n{attack_situation}\n{defense_situation}"

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

    def dice_roll(self, values: list = [1, 2, 3, 4, 5, 6]) -> float:
        multiplier = {
            1: 0.5,
            2: 0.8,
            3: 0.9,
            4: 1.0,
            5: 1.1,
            6: 1.5
        }
        roll = random.choice(values)
        return multiplier.get(roll, 1.0)

    def __return_adapted_off_army_stats(self) -> float:
        army_stats = sum(
            army.get_attack() * army.get_birth_modifier()
            for army in self.off_army
        )
        return round(army_stats, 2)

    def __return_adapted_def_army_stats(self) -> float:
        army_stats = sum(
            army.get_defense() * army.get_birth_modifier()
            for army in self.def_army
        )
        return round(army_stats, 2)

    def __calculate_offensive_off_damage(self, off_attack_stats: float) -> float:
        # Adicionar ao cálculo o bônus de ataque baseado no nível da província de origem
        return off_attack_stats * self.off_diff_health()

    def __calculate_offensive_def_damage(self, def_defense_stats):
        return (
            def_defense_stats
            * self.province.get_terrain().get_defence_modifier()
            * self.province.get_defence_modifier()
            * self.def_diff_health()
        )

    def __calculate_defensive_off_damage(self, def_attack_stats):
        return def_attack_stats * self.def_diff_health()

    def __calculate_defensive_def_damage(self, off_defense_stats):
        return off_defense_stats * self.off_diff_health()

    def off_damage(self, off_attack_stats: float, def_defense_stats: float):
        off_damage = round(
            (self.__calculate_offensive_off_damage(off_attack_stats) -
             self.__calculate_offensive_def_damage(def_defense_stats)) * self.dice_roll(),
            2,
        )
        return off_damage if off_damage > 0 else 0.1

    def def_damage(self, def_attack_stats, off_defense_stats):
        def_damage = round((
                           self.__calculate_defensive_off_damage(def_attack_stats) -
                           self.__calculate_defensive_def_damage(
                               off_defense_stats)) * self.dice_roll(),
                           2,
                           )
        return def_damage if def_damage > 0 else 0.1

    def health_check(self):
        for army in self.off_army:
            if army.check_health():
                self.remove_off_army(army)
        for army in self.def_army:
            if army.check_health():
                self.remove_def_army(army)

        return self.army_check()

    def army_check(self):
        if self.get_off_actual_health() <= 0:
            return True
        if self.get_def_actual_health() <= 0:
            return True
        return False

    def battle_going(self):
        check = self.health_check()
        if check:
            print("Batalha finalizada!")
            return True

        self.turn_update()

        off_damage = self.off_damage(
            self.__return_adapted_off_army_stats(), self.get_def_total_defense()
        )
        def_damage = self.def_damage(
            self.__return_adapted_def_army_stats(), self.get_off_total_defense()
        )

        if self.get_turns_count() == self.get_epic_turns():
            print("Batalha épica!")
            off_damage *= 3
            def_damage *= 3
            off_damage = round(off_damage, 2)
            def_damage = round(def_damage, 2)

        self.last_off_damage = off_damage
        self.last_def_damage = def_damage

        self.__off_damage_history.append(off_damage)
        self.__def_damage_history.append(def_damage)

        off_unit_damage = off_damage / self.total_off_army()
        def_unit_damage = def_damage / self.total_def_army()

        for army in self.off_army:
            army.health_damage(def_unit_damage)

        for army in self.def_army:
            army.health_damage(off_unit_damage)

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
    teste.add_off_army(army_off2)
    teste.add_off_army(army_off3)
    teste.add_off_army(army_off4)
    teste.add_off_army(army_off5)

    teste.add_def_army(army_def)
    teste.add_def_army(army_def2)
    teste.add_def_army(army_def3)
    teste.add_def_army(army_def4)

    for i in range(0, 2000):
        var = teste.battle_going()
        if var is True:
            break
        print(
            f"\nVida do exército atacante: {teste.get_off_actual_health(
            )}\nVida do exército defensor: {teste.get_def_actual_health()}"
        )
