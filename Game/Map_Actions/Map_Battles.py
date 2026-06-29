from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table

from Configs.Console import ConsoleClass
from Game.Battle_Control.Battle_Control import BattleControl
from Province import Province


class Map_Battles:
    def __init__(self, battle_control: BattleControl):
        self.console = ConsoleClass.get_console()
        self.battle_control = battle_control
        self.no_fog_battles_info = battle_control.ongoing_battles

    def __create_army_token(self, army, index: int, border_color: str) -> Panel:
        is_group = hasattr(army, "armys") and army.get_army_quant() > 1
        label = "Grupo" if is_group else "Exército"
        size_info = f"Qtd: {army.get_army_quant()}" if is_group else None
        token_lines = [
            *([size_info] if size_info else []),
            f"Ataque: {army.get_attack():.2f}",
            f"Defesa: {army.get_defense():.2f}",
            f"Vida: {army.get_health():.2f}",
        ]
        return Panel(
            "\n".join(token_lines),
            title=f"{label} #{index}",
            border_style=border_color,
            padding=(0, 1),
            expand=False,
        )

    def __build_army_tokens(self, armies, color: str):
        if not armies:
            return [
                Panel(
                    "Sem exércitos ativos",
                    border_style=color,
                    padding=(0, 1),
                    expand=False,
                )
            ]
        return [
            self.__create_army_token(army, index, color)
            for index, army in enumerate(armies, start=1)
        ]

    def __build_army_map(self, battle):
        army_map = Table(title="Mapa da Batalha", show_lines=True, width=100)
        army_map.add_column("Atacantes", justify="center")
        army_map.add_column("Defensores", justify="center")

        attacker_tokens = Columns(
            self.__build_army_tokens(battle.get_off_army(), "green"),
            expand=True,
            equal=True,
        )
        defender_tokens = Columns(
            self.__build_army_tokens(battle.get_def_army(), "red"),
            expand=True,
            equal=True,
        )

        army_map.add_row(attacker_tokens, defender_tokens)
        return army_map

    def __build_battle_info(self, fog_of_war: bool, province: Province, battle):
        if fog_of_war or battle is None:
            return

        battle_neighbors = ", ".join(
            neighbor.get_name() for neighbor in province.get_neighbors()
        ) or "Sem vizinhos"
        battle_province_stats = province.obtain_province_battle_stats()
        battle_off_player = battle.get_off_army_owner().get_player_name()
        battle_def_player = battle.get_def_army_owner().get_player_name()
        battle_off_army_size = battle.total_off_army()
        battle_def_army_size = battle.total_def_army()
        battle_off_health = battle.get_off_actual_health()
        battle_def_health = battle.get_def_actual_health()
        battle_off_last_damage = battle.get_last_off_damage()
        battle_def_last_damage = battle.get_last_def_damage()
        battle_turns = battle.get_turns_count()
        battle_epic_turns = battle.get_epic_turns()
        epic_turns_left = battle_epic_turns - battle_turns
        epic_status = str(epic_turns_left) if epic_turns_left > 0 else "ÉPICA!"
        battle_predicted_winner = self.battle_control.predict_battle_winner(
            province
        )
        battle_map = self.__build_army_map(battle)
        battle_province_name = province.get_name()

        main_table = Table(title="Visão Geral", show_lines=True)
        local_table = Table(
            title="Informações da Província", show_lines=True, width=100
        )
        stats_table = Table(
            title="Informações da Batalha", show_lines=True, width=100
        )

        local_table.add_column("Campo", style="bold magenta", justify="center")
        local_table.add_column(
            "Detalhes", style="bold white", justify="center")

        province_rows = (
            ("Província em Batalha", battle_province_name),
            (
                "Modificadores",
                f"Terreno: {battle_province_stats[0] * 100}%, "
                f"Defesa: {battle_province_stats[1] * 100}%, "
                f"Level: {battle_province_stats[2]}",
            ),
            ("Vizinhos", battle_neighbors),
        )
        for row in province_rows:
            local_table.add_row(*row)

        stats_table.add_column("Campo", style="bold cyan", justify="center")
        stats_table.add_column("Atacante", style="green", justify="center")
        stats_table.add_column("Defensor", style="red", justify="center")

        stats_rows = (
            ("Jogador", battle_off_player, battle_def_player),
            ("Qtd. Exércitos", str(battle_off_army_size), str(battle_def_army_size)),
            ("Vida Atual", str(battle_off_health), str(battle_def_health)),
            (
                "Último Dano",
                str(battle_off_last_damage),
                str(battle_def_last_damage),
            ),
            ("Turnos Decorridos", str(battle_turns), str(battle_turns)),
            ("Épica em", epic_status, epic_status),
            (
                "Vencedor Previsto",
                battle_predicted_winner[0],
                battle_predicted_winner[1],
            ),
        )
        for row in stats_rows:
            stats_table.add_row(*row)

        main_table.add_column(
            f"A Batalha de {battle_province_name}",
            style="bold yellow",
            justify="center",
            no_wrap=True,
        )
        main_table.add_row(local_table)
        main_table.add_row(stats_table)
        main_table.add_row(battle_map)
        return main_table

    def __refresh_no_fog_battles(self):
        self.no_fog_battles_info = self.battle_control.ongoing_battles

    def display_battle_map(self, province_filter=None):
        """
        Se province_filter for None: exibe todas as batalhas (comportamento atual).
        Se for uma string: busca por nome da província (case-insensitive).
        Se for um objeto Province: compara pelo nome/identidade.
        """
        self.__refresh_no_fog_battles()

        if not self.no_fog_battles_info:
            self.console.print("Nenhuma batalha em andamento no mapa.")
            return

        # Quando for solicitado filtrar por uma província específica
        if province_filter is not None:
            target_province = None
            target_battle = None
            for province, battle in self.no_fog_battles_info.items():
                if isinstance(province_filter, Province):
                    match = province is province_filter or province.get_name() == province_filter.get_name()
                else:
                    # tratar como nome (string)
                    try:
                        match = province.get_name().strip().lower() == str(
                            province_filter).strip().lower()
                    except Exception:
                        match = False
                if match:
                    target_province = province
                    target_battle = battle
                    break

            if target_battle is None:
                self.console.print(
                    f"Nenhuma batalha encontrada para a província '{province_filter}'.")
                return

            main_table = self.__build_battle_info(
                fog_of_war=False, province=target_province, battle=target_battle)
            if main_table:
                self.console.print(main_table)
            return

        # Sem filtro: comportamento original — exibir todas as batalhas
        for province, battle in self.no_fog_battles_info.items():
            main_table = self.__build_battle_info(
                fog_of_war=False, province=province, battle=battle)
            if main_table:
                self.console.print(main_table)
