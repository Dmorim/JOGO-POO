from Configs.Console import ConsoleClass

from rich.table import Table
from rich.text import Text


class MapActions:
    def __init__(self):
        self.console = ConsoleClass.get_console()

    def __print_map_actions(self):
        map_text = Text("Ações do Mapa", style="bold blue")
        map_table = Table.grid(padding=(0, 0))
        map_table.add_row(map_text, style="bold blue")
        map_table.add_row(
            Text("1. Ver Batalhas em Andamento", style="bold green"),
            Text("2. Informações das Províncias", style="bold green"),
            Text("3. Exibir Mapa Detalhado", style="bold green"),
            Text("4. Histórico do Turno passado", style="bold green"),
            Text("5. Sair", style="bold green")
        )
        return map_table

    def map_actions(self):
        self.console.print(self.__print_map_actions())
        self.console.print("\nEscolha uma opção: ", style="bold yellow")
        self.console.input()
