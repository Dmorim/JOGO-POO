from rich.table import Table

from Configs.Console import ConsoleClass
from Game.Battle_Control.Battle_Control import BattleControl


class Map_Battles:
    def __init__(self, battle_control: BattleControl):
        self.console = ConsoleClass.get_console()
        self.battle_control = battle_control

    def __get_no_fog_battles(self):
        battles_info = {}
        for idx, (province, battle) in enumerate(self.battle_control.ongoing_battles.items(), start=1):
            battles_info[idx] = (
                province.get_name(),
                (", ".join(neighbor.get_name()
                 for neighbor in province.get_neighbors())),
                province.obtain_province_battle_stats(),
                battle.get_off_army_owner().get_player_name(),
                battle.get_def_army_owner().get_player_name(),
                battle.total_off_army(),
                battle.total_def_army(),
                battle.get_off_actual_health(),
                battle.get_def_actual_health(),
                battle.get_last_off_damage(),
                battle.get_last_def_damage(),
                battle.get_turns_count(),
                battle.get_epic_turns(),
            )
        return (battles_info)

    def __build_battle_info(self, fog_of_war: bool, battle_id: str):
        if fog_of_war:
            return

        battle_data = self.no_fog_battles_info[battle_id]
        battle_province = battle_data[0]
        battle_neighbors = battle_data[1]
        battle_province_stats = battle_data[2]
        battle_off_player = battle_data[3]
        battle_def_player = battle_data[4]
        battle_off_army_size = battle_data[5]
        battle_def_army_size = battle_data[6]
        battle_off_health = battle_data[7]
        battle_def_health = battle_data[8]
        battle_off_last_damage = battle_data[9]
        battle_def_last_damage = battle_data[10]
        battle_turns = battle_data[11]
        battle_epic_turns = battle_data[12]
        battle_predicted_winner = self.battle_control.predict_battle_winner(
            battle_province)

        main_table = Table(title="Visão Geral", show_lines=True)
        local_table = Table(title="Informações da Província",
                            show_lines=True, width=100)
        stats_table = Table(title="Informações da Batalha",
                            show_lines=True, width=100)

        local_table.add_column("Campo", style="bold magenta",
                               justify="center")
        local_table.add_column(
            "Detalhes", style="bold white", justify="center")

        local_table.add_row("Província em Batalha", battle_province)
        local_table.add_row("Modificadores",
                            f'Terreno: {(battle_province_stats[0]) * 100}%, Defesa: {(battle_province_stats[1]) * 100}%, Level: {battle_province_stats[2]}')
        local_table.add_row("Vizinhos", battle_neighbors)

        stats_table.add_column("Campo", style="bold cyan", justify="center")
        stats_table.add_column("Atacante", style="green", justify="center")
        stats_table.add_column("Defensor", style="red", justify="center")

        stats_table.add_row("Jogador", battle_off_player, battle_def_player)
        stats_table.add_row("Qtd. Exércitos", str(
            battle_off_army_size), str(battle_def_army_size))
        stats_table.add_row("Vida Atual", str(
            battle_off_health), str(battle_def_health))
        stats_table.add_row("Último Dano", str(
            battle_off_last_damage), str(battle_def_last_damage))
        stats_table.add_row("Turnos Decorridos", str(
            battle_turns), str(battle_turns))
        stats_table.add_row("Turnos Épicos", str(battle_epic_turns -
                                                 battle_turns if battle_epic_turns > battle_turns else 'ÉPICA!'), str(battle_epic_turns - battle_turns if battle_epic_turns > battle_turns else 'ÉPICA!'))
        stats_table.add_row("Vencedor Previsto",
                            battle_predicted_winner[0], battle_predicted_winner[1])

        main_table.add_column(
            f"A Batalha de {battle_province}", style="bold yellow", justify="center", no_wrap=True)
        main_table.add_row(local_table)
        main_table.add_row(stats_table)
        return main_table

    def display_battle_map(self):
        self.no_fog_battles_info = self.__get_no_fog_battles()

        if not self.no_fog_battles_info:
            self.console.print("Nenhuma batalha em andamento no mapa.")
            return

        for battle_id in self.no_fog_battles_info:
            main_table = self.__build_battle_info(
                fog_of_war=False, battle_id=battle_id)
            self.console.print(main_table)
