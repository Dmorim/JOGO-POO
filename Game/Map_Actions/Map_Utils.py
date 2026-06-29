from rich import print


def map_mensage(mensage: str, color: str = "red"):
    print(f"[bold {color}]{mensage}[/bold {color}]")
