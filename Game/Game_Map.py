from Game.Battle_Control.Battle_Control import BattleControl


class GameMap:
    def __init__(self, game):
        self.game = game
        self.battle_control = BattleControl()
        pass

    def __print_player_province(self, player):
        for province in player.get_player_province():
            print(province.province_situation())
            self.__print_player_army(player, province)

    def __print_player_army(self, player, province):
        for army in player.army_in_province(province):
            print(army.army_situation())

    def __print_player_battle(self, player):
        print(f"{'='*25}\nBatalhas em andamento:\n{'='*25}")
        for i, battle in enumerate(self.battle_control.ongoing_battles):
            print(f"\nBatalha {i+1} - {battle.battle_situation()}")
            print(f"{'='*78}")
            print(battle.get_last_off_damage())
            print(f"{battle.get_last_def_damage()}\n")
            if self.battle_control.ongoing_battles.index(battle) != len(self.battle_control.ongoing_battles) - 1:
                print(f"{'='*78}\n")

    def print_map(self):
        # Print the map with province ownership and armies
        print(f"\nTurno: {self.game.get_turn_count()}")
        print("\nMapa:")
        for player in self.game.players:
            print(f"{'-'*110}\nJogador: {player.get_player_name()}\n{'-'*110}")
            self.__print_player_province(player)
            print()
        if self.battle_control.ongoing_battles:
            pass
