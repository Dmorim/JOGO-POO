from Game.Battle_Control.Battle_Control import BattleControl
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.style import Style


class GameMap:
    def __init__(self, game):
        self.game = game
        self.battle_control = BattleControl()
        self.console = Console()

    def __print_player_province(self, player):
        for province in player.get_player_province():
            self.console.print(
                province.province_situation(), style="bold green")
            self.__print_player_army(player, province)

    def __print_player_army(self, player, province):
        for army in player.army_in_province(province):
            self.console.print(army.army_situation(), style="bold blue")

    def __print_player_battle(self, player):
        self.console.print(
            f"{'='*25}\nBatalhas em andamento:\n{'='*25}", style="bold red")
        for i, battle in enumerate(self.battle_control.ongoing_battles):
            self.console.print(
                f"\nBatalha {i+1} - {battle.battle_situation()}", style="bold yellow")
            self.console.print(f"{'='*78}")
            self.console.print(battle.get_last_off_damage(),
                               style="bold magenta")
            self.console.print(
                f"{battle.get_last_def_damage()}\n", style="bold magenta")
            if self.battle_control.ongoing_battles.index(battle) != len(self.battle_control.ongoing_battles) - 1:
                self.console.print(f"{'='*78}\n")

    def print_map(self):
        # Create a table for the turn and map information
        title_style = Style(color="bright_white",
                            bgcolor="dark_blue", bold=True, italic=True)

        provinces_style_player = Style(
            color="green")
        provinces_style_enemy = Style(
            color="red")

        self.console.print(Panel.fit(f"JOGADOR: {self.game.current_player.get_player_name().upper()}\nTurno: {self.game.get_turn_count()}",
                                     style=title_style))

        general_map = Table.grid(padding=(0, 1), expand=True)

        for player in self.game.players:
            color_of_player = "green" if player == self.game.current_player else "red"
            general_map.add_row(Panel.fit(
                f"Jogador: {player.get_player_name()} | Total de Exércitos: {player.get_total_armys()}", style=color_of_player, border_style=color_of_player))

            provinces_table = Table.grid()
            for provinces in player.get_player_province():
                provinces_table.add_row(
                    Panel.fit(provinces.province_situation(), border_style=color_of_player, style=color_of_player))

                if len(player.army_in_province(provinces)) > 0:
                    army_table = Table.grid()
                    for army in player.army_in_province(provinces):
                        army_table.add_row(
                            Panel.fit(army.army_situation(), style='bright_blue'))
                    provinces_table.add_row(army_table)
            panel_provinces = Panel.fit(
                provinces_table, style=provinces_style_player if player == self.game.current_player else provinces_style_enemy)
            general_map.add_row(panel_provinces)
        self.console.print(general_map)

        """
        # Print the map with province ownership and armies
        for player in self.game.players:
            self.console.print(
                f"{'-'*110}\nJogador: {player.get_player_name()}\n{'-'*110}", style="bold white")
            self.__print_player_province(player)
            self.console.print()
        if self.battle_control.ongoing_battles:
            self.__print_player_battle(player)
        """
