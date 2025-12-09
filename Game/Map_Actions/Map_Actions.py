from Configs.Console import ConsoleClass

from rich.table import Table
from rich.text import Text


class MapActions:
    def __init__(self):
        self.console = ConsoleClass.get_console()

    def __print_map_actions(self):
        text_show = ['1. Ver Batalhas em Andamento',
                     '2. Informações das Províncias',
                     '3. Exibir Mapa Detalhado',
                     '4. Histórico do Turno passado',
                     '5. Sair']
        map_text = Text("Ações:", style="bold blue")
        map_table = Table.grid(padding=(0, 0))
        map_table.add_row(map_text, style="bold blue")
        for text in text_show:
            map_table.add_row(
                Text(text, style="bold white"))
        return map_table

    def __map_validate_option(self, option):
        valid_options = ['1', '2', '3', '4', '5']
        if option not in valid_options:
            self.console.print(
                "Opção inválida. Tente novamente.", style="bold red")
            return False
        return option in valid_options

    def map_actions(self):
        self.console.print(self.__print_map_actions())
        option = self.console.input(
            "\nEscolha uma opção: ")
        while not self.__map_validate_option(option):
            option = self.console.input(
                "\nEscolha uma opção: ")
        return option
