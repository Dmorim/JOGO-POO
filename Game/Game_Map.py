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
        # Estilo do título
        title_style = Style(color="bright_white",
                            bgcolor="dark_blue", bold=True, italic=True)

        self.console.print(
            Panel.fit(
                f"JOGADOR: {self.game.current_player.get_player_name().upper() or 'Desconhecido'}\nTurno: {self.game.get_turn_count()}",
                style=title_style
            )
        )

        # Tabela principal
        main_table = Table.grid(padding=(0, 1), expand=True)

        for player in self.game.players:
            # Determinar estilo do jogador
            player_color = "green" if player == self.game.current_player else "red"
            player_style = Style(color=player_color)

            # Cabeçalho do jogador
            player_name = player.get_player_name() or "Desconhecido"
            total_armys = player.get_total_armys() or 0
            player_header = Panel.fit(
                f"Jogador: {player_name} | Exércitos: {total_armys}",
                style=player_style,
                border_style=player_color
            )
            main_table.add_row(player_header)

            # Container de províncias
            provinces_container = Table.grid(padding=0, pad_edge=False)

            for province in player.get_player_province():
                province_situation = province.province_situation() or "Sem informações"
                print(province_situation)
                province_panel = Panel(
                    province_situation,
                    border_style=player_color,
                    style=player_style,
                    padding=(0, 1),
                    expand=False
                )
                provinces_container.add_row(province_panel)
                self.console.print(province_panel)

                # Exércitos na província
                armies = player.army_in_province(province) or []
                for army in armies:
                    army_situation = army.army_situation() or "Sem informações"
                    print(army_situation)
                    army_panel = Panel(
                        army_situation,
                        style="bright_blue",
                        padding=(0, 2),
                        border_style=None,
                        expand=False
                    )
                    provinces_container.add_row(army_panel)

            main_table.add_row(provinces_container)
            main_table.add_row("")  # Espaçamento entre jogadores

        self.console.print(main_table)
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
