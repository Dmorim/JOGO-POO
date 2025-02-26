from Game.Game import Game
from Player import Player
from Army import Army_Group


class Game_Action():
    def __init__(self, game: Game):
        self.game = game

    def action(self, player: Player):
        try:
            print("Exércitos disponíveis: ")
            for army in player.get_available_army():
                if isinstance(army, Army_Group):
                    if army.get_in_healing():
                        print(
                            f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {
                                army.get_health()}, Província: {army.get_province().get_name()} {'(Em Cura)' if army.get_in_healing() else ''}"
                        )
                    else:
                        print(
                            f"Grupo com: {len(army.get_armys())} exércitos. Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Saúde: {army.get_health()}, Província: {
                                army.get_province().get_name()}, ({player.get_available_army().index(army) + 1}) {'(Em movimento)' if army.get_in_move() else ''}"
                        )
                else:
                    if army.get_in_healing():
                        print(
                            f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Vida: {army.get_health(
                            )}. Província: {army.get_province().get_name()} {'(Em Cura)' if army.get_in_healing() else ''}"
                        )
                    else:
                        print(
                            f"Exército: Ataque: {army.get_attack()}, Defesa: {army.get_defense()}, Vida: {army.get_health()}. Província: {army.get_province(
                            ).get_name()}, ({player.get_available_army().index(army) + 1}) {'(Em movimento)' if army.get_in_move() else ''}"
                        )

            selected_army = input()
            if int(selected_army) <= len(player.get_available_army()) + 1:
                selected_army = player.armys[int(selected_army) - 1]
                print(
                    f"Província atual: {selected_army.get_province().get_name()}, Vizinhos: {
                        [neighbor.get_name() for neighbor in selected_army.get_province().get_neighbors()]}"
                )

                print(
                    "Ações disponíveis:\n1 - Mover Exército\n2 - Dividir Exército\n3 - Curar Exército\n0 - Voltar"
                )
                army_actions = input()
                if army_actions == "1":
                    self.moviment.army_movement(player, selected_army)
                elif army_actions == "2":
                    self.army_split(player, selected_army)
                elif army_actions == "3":
                    self.heal_army(selected_army)
                elif army_actions == "0":
                    pass
        except:
            print("Não há exércitos disponíveis.")
            self.mapmode = False
            return
