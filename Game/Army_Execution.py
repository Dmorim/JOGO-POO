from Army import Army_Group

class Army_Execution:
    def __init__(self):
        pass

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

    def army_split(self, player_m, selected_army):
        if selected_army.get_in_move():
            print("Exército em movimento. Não é possível dividir.")
            return
        if selected_army.get_in_healing():
            print("Exército em cura. Não é possível dividir.")
            return
        if isinstance(selected_army, Army_Group):
            army = selected_army.split_group()
            if army is not None:
                player_m.armys.append(army)
                self.mapmode = False
        else:
            print("Exército não é um grupo.")
            return
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