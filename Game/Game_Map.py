from Game.Battle_Control.Battle_Control import BattleControl
from Configs.Console import ConsoleClass

from rich.table import Table
from rich.panel import Panel
from rich.style import Style
from rich.text import Text


class GameMap:
    def __init__(self):
        self.game = None
        self.battle_control = BattleControl()
        self.console = ConsoleClass.get_console()

    def get_game(self, game):
        if self.game is None:
            self.game = game
        return self.game

    def __province_color_status(self, province, player_style):
        if province.get_in_battle():
            return Style(color="red", bold=True)
        elif province.get_dom_turns() > 0:
            return Style(color="yellow", bold=True)
        else:
            return player_style

    def __army_color_status(self, army):
        if army.get_in_battle():
            return Style(color="red", bold=True)
        elif army.get_in_healing():
            return Style(color="green", bold=True)
        else:
            return Style(color="bright_blue")

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

    def __print_current_player(self, title_style, player):
        self.console.print(
            Panel.fit(
                f"JOGADOR: {player.get_player_name().upper()} | Turno: {self.game.get_turn_count()} | Pontos: {player.get_player_actions()}",
                style=title_style
            )
        )

    def __player_province_group(self, province, player_style, player_color):
        province_situation = province.province_situation() or "Sem informações"

        province_border = player_color
        province_style = self.__province_color_status(province, player_style)
        province_text = Text(province_situation, style=province_style)

        province_group = Table.grid(padding=(0, 0))
        province_group.add_row(
            Panel(
                province_text,
                border_style=province_border,
                style=province_style,
                padding=(0, 1),
                width=120
            )
        )
        return province_group

    def __player_province_army(self, army, province_group):
        army_situation = army.army_situation() or "Sem informações"
        army_style = self.__army_color_status(army)

        army_text = Text(f"    {army_situation}", style=army_style)
        province_group.add_row(army_text)

    def print_map(self):
        # Estilo do título
        title_style = Style(color="bright_white", bold=True, italic=True)

        self.__print_current_player(title_style, self.game.current_player)

        # Tabela principal
        main_table = Table.grid(padding=(1, 2), expand=True)

        for player in self.game.players:
            # Determinar estilo do jogador
            is_current = player == self.game.current_player
            player_color = "green" if is_current else "dark_orange"
            player_style = Style(color=player_color)
            player_name = player.get_player_name()
            total_armys = player.get_total_armys()
            player_title_text = Text(f"Jogador: {player_name} | Exércitos: {total_armys}", style=Style(
                bold=True, color=player_color))

            # Container de províncias do jogador
            player_container = Table.grid(padding=(0, 0))
            for province in player.get_player_province():
                province_group = self.__player_province_group(
                    province, player_style, player_color)
                # Exércitos indentados como linhas simples e coloridos
                armies = player.army_in_province(province)
                for army in armies:
                    self.__player_province_army(army, province_group)
                player_container.add_row(province_group)

            # Adiciona container de jogador na tabela principal com título estilizado e largura dinâmica
            main_table.add_row(
                Panel(player_container, border_style=player_color,
                      title=player_title_text, title_align="left")
            )

        self.console.print(main_table)
        self.__print_player_battle(self.game.current_player)
