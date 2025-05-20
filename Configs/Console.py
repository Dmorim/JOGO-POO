from rich.console import Console


class ConsoleClass:
    __ininstance = None

    def __new__(cls):
        if cls.__ininstance is None:
            cls.__ininstance = super(ConsoleClass, cls).__new__(cls)
        return cls.__ininstance

    def __init__(self):
        self.console = None

    @classmethod
    def get_console(cls):
        if cls.__ininstance is None:
            cls.__new__(cls)
            cls.__ininstance.console = Console()
        return cls.__ininstance.console
