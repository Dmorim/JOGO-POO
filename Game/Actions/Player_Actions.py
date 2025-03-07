from Player import Player
from IA.IA import IA
from Game.Actions.Game_Actions import Game_Action
from multipledispatch import dispatch
from Game.Game_State import Game_State


class Player_Action():
    def __init__(self):
        self.game_state = Game_State
        self.game_actions = Game_Action()

    def __valid_acts_choices(self, valid_answers: list = ["1", "2", "0"]) -> str:
        while True:
            act = input("Escolha uma opção: ")
            if act in valid_answers:
                return act

    def __show_valid_acts(self, player, valid_answers_text: str = "1 - Ações com Exército\n2 - Melhorar Província\n0 - Passar"):
        print(
            f"Ações disponíveis:\n{valid_answers_text}\nPontos de Ação: {round(player.get_player_actions(), 2)}\n{'='*25}"
        )

    def __show_initial_screen(player: Player):
        print(
            f"{'='*25}\nJogador Atual: {player.get_player_name()}"
        )
        print(
            f"Pontos de Ação: {
                round(player.get_player_actions(), 2)}\n"
        )

    @dispatch(Player, bool)
    def action(self, player: Player, mapmode: bool):
        if mapmode:
            self.__show_initial_screen
        self.__show_valid_acts(player)
        action_choose = self.__valid_acts_choices()
        self.game_actions.action(player, action_choose)

    @dispatch(IA, bool)
    def action(self, IA: IA, mapmode: bool):
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
