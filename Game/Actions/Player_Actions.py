from Player import Player
from IA.IA import IA
from Game.Actions.Game_Actions import Game_Action
from multipledispatch import dispatch


class Player_Action():
    def __init__(self, game):
        self.game = game
        self.game_actions = Game_Action()

    def __valid_acts_choices(self, valid_answers: list = ["1", "2", "0"]) -> str:
        act = input("Escolha uma opção: ")
        while act not in valid_answers:
            print("Valor inválido. Tente novamente.")
            act = input("Escolha uma opção: ")
        return act

    def __show_valid_acts(self, valid_answers_text: str = "1 - Mover Exército\n2 - Melhorar Província\n0 - Passar"):
        print(
            f"Ações disponíveis:\n{valid_answers_text}"
        )

    @dispatch(Player)
    def action(self, player: Player):
        print(
            f"{'='*25}\nJogador Atual: {player.get_player_name()}"
        )
        print(
            f"Pontos de Ação: {
                round(player.get_player_actions(), 2)}\n"
        )
        self.__show_valid_acts()
        action_choose = self.__valid_acts_choices()
        return self.game_actions.action(player, action_choose)

    @dispatch(IA)
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
