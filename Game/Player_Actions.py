from Game.Game import Game
from Player import Player
from IA.IA import IA


class Player_Action():
    def __init__(self, game: Game):
        self.game = game

    def action(self, player: Player):
        if self.game.mapmode:
            self.game.print_map()
        print(
            f"{'='*25}\nJogador Atual: {player.get_player_name()}"
        )
        print(
            f"Pontos de Ação: {
                round(player.get_player_actions(), 2)}\n"
        )
        action = input("Escolha uma opção: ")
        if action == "1":
            self.game.army_actions(player)
        elif action == "2":
            self.game.upgrade_province(player)
        elif action == "3":
            self.game.attack_province()
        elif action == "0":
            return
        else:
            print("Invalid action. Try again.")

    def action(self, IA: IA):
        act, var = IA.act_do()
        if act == "Move":
            province = var[0][0]
            army = var[0][1]
            self.moviment.army_make_movement(
                army, None, province)
            print(f"Exército movido para {
                province.get_name()}")
        elif act == "Up_Prov":
            prov = var[0]
            self.current_player.action_upgrade_province(prov)
            self.upgrade_province(self.current_player, prov)
            print(f"Província {prov.get_name()} melhorada")
        elif act == "Heal":
            heal_army = var[0]
            self.heal_army(heal_army)
        elif act == "Skip":
            pass
