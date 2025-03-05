from multipledispatch import dispatch

from Army import Army, Army_Group
from Player import Player


class Army_Execution:
    def __init__(self, game):
        self.game = game

    def group_army(self, player_m):
        for province in player_m.provinces:
            armies = [
                army
                for army in player_m.armys
                if army.get_province() == province and army.get_in_move() == False
            ]

            if len(armies) > 1:
                group = None
                for army in armies:
                    if isinstance(army, Army_Group):
                        group = army
                        break

                if group is None:
                    self.create_group_army(player_m, armies)

                else:
                    self.add_army_to_group(player_m, armies)

    def create_group_army(self, player_m, armies):
        army_group = armies[0].group_army()
        player_m.armys.append(army_group)
        for army in armies:
            army_group.add_army(army)
            player_m.armys.remove(army)

    def add_army_to_group(self, player_m, armies):
        # Check if there is an existing Army_Group
        for army in armies:
            if isinstance(army, Army_Group):
                group = army
                break
        for army in armies:
            if army != group:
                if army not in group.get_armys():
                    if not isinstance(army, Army_Group):
                        group.add_army(army)
                        player_m.armys.remove(army)
                    else:
                        army.transfer_army(group)
                        player_m.armys.remove(army)
        return

    def __army_division_quantity(self, selected_army):
        try:
            quantity = int(
                input("Quantidade do novo exército: "))
        except ValueError:
            print("Valor inválido.")
            return self.__army_division_quantity(selected_army)
        if quantity <= 0 or quantity >= selected_army.get_army_quant():
            print("Valor inválido.")
            return self.__army_division_quantity(selected_army)
        return quantity

    @dispatch(Player, Army)
    def army_division(self, player_m: Player, selected_army: Army):
        self.game.mapmode = False
        return print("Não é possível divisão para esse exército")

    @dispatch(Player, Army_Group)
    def army_division(self, player_m: Player, selected_army: Army_Group):
        quantity = self.__army_division_quantity(selected_army)
        new_army = selected_army.split_group(quantity)
        player_m.armys.append(new_army)
        self.game.mapmode = False
        return

    def heal_army(self, selected_army):
        if selected_army.get_in_move():
            print("Exército em movimento. Não é possível curar.")
            self.mapmode = False
            return
        if selected_army.get_in_healing():
            print("Exército já está em cura. Deseja cancelar? (S/N)")
            if input().lower() == "s":
                selected_army.set_in_healing(False)
                print("Cura cancelada.")
            elif input().lower() == "n":
                pass
            else:
                print("Comando inválido.")
            self.mapmode = False
            return
        if selected_army.get_health() == selected_army.get_max_health():
            print("Exército já está com vida máxima.")
            self.mapmode = False
            return
        if selected_army.get_province().get_in_battle():
            print("Exército em batalha, não é possível curar ele")
            self.mapmode = False
            return
        selected_army.set_in_healing(True)
        selected_army.get_owner().action_heal_army()
        print("Exército em cura.")
        self.mapmode = False
        return
