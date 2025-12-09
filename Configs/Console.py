from rich.console import Console


class ConsoleClass:
    __ininstance = None

    def __new__(cls):
        if cls.__ininstance is None:
            cls.__ininstance = super(ConsoleClass, cls).__new__(cls)
        return cls.__ininstance

    def __init__(self):
        self.console = None

    def set_new_console(self, console: Console):
        if self.console is None:
            self.console = console

    @classmethod
    def get_console(cls):
        if cls.__ininstance is None:
            cls.__new__(cls)
            cls.__ininstance.console = Console()
        return cls.__ininstance.console
