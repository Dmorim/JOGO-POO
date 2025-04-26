from Game.Battle_Control.Battle_Control import BattleControl
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text


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
        # Estilo do título
        title_style = Style(color="bright_white",
                            bgcolor="dark_blue", bold=True, italic=True)

        self.console.print(
            Panel.fit(
                f"JOGADOR: {self.game.current_player.get_player_name().upper() if self.game.current_player.get_player_name() else 'Desconhecido'}\nTurno: {self.game.get_turn_count()}",
                style=title_style
            )
        )

        # Tabela principal
        main_table = Table.grid(padding=(1, 2), expand=True)

        for player in self.game.players:
            # Determinar estilo do jogador
            is_current = player == self.game.current_player
            player_color = "green" if is_current else "dark_orange"
            player_style = Style(color=player_color)

            # Nome e total de exércitos do jogador como título estilizado
            player_name = player.get_player_name() or "Desconhecido"
            total_armys = player.get_total_armys() or 0
            player_title_text = Text(f"Jogador: {player_name} | Exércitos: {total_armys}", style=Style(
                bold=True, color=player_color))

            # Container de províncias do jogador
            player_container = Table.grid(padding=(0, 0))

            for province in player.get_player_province():
                province_situation = province.province_situation() or "Sem informações"
                is_battling = province.get_in_battle() if hasattr(
                    province, "get_in_battle") else False
                dom_turns = province.get_dom_turns() if hasattr(province, "get_dom_turns") else 0

                province_style = player_style
                province_border = player_color
                if is_battling:
                    province_style = Style(
                        color="red", bold=True)
                    province_border = "red"
                elif dom_turns > 0:
                    province_style = Style(color="yellow", bold=True)
                    province_border = "yellow"

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

                # Exércitos indentados como linhas simples e coloridos
                armies = player.army_in_province(province) or []
                for army in armies:
                    army_situation = army.army_situation() or "Sem informações"
                    is_army_battling = army.get_in_battle()
                    is_army_healing = army.get_in_healing()

                    if is_army_battling:
                        army_style = Style(
                            color="red", bold=True)
                    elif is_army_healing:
                        army_style = Style(
                            color="bright_green")
                    else:
                        army_style = Style(color="bright_blue")

                    army_text = Text(f"    {army_situation}", style=army_style)
                    province_group.add_row(army_text)

                player_container.add_row(province_group)

            # Adiciona container de jogador na tabela principal com título estilizado e largura dinâmica
            main_table.add_row(
                Panel(player_container, border_style=player_color,
                      title=player_title_text, title_align="left")
            )

        self.console.print(main_table)
