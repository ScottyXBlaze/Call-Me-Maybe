# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    home.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/13 16:35:44 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 00:10:22 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import sys

from readchar import readkey
from rich.console import Console


class Home:
    def __init__(self, models: list[str]) -> None:
        self.title = """
  ░██████             ░██ ░██    ░███     ░███               ░███     ░███                       ░██                   
 ░██   ░██            ░██ ░██    ░████   ░████               ░████   ░████                       ░██                   
░██         ░██████   ░██ ░██    ░██░██ ░██░██  ░███████     ░██░██ ░██░██  ░██████   ░██    ░██ ░████████   ░███████  
░██              ░██  ░██ ░██    ░██ ░████ ░██ ░██    ░██    ░██ ░████ ░██       ░██  ░██    ░██ ░██    ░██ ░██    ░██ 
░██         ░███████  ░██ ░██    ░██  ░██  ░██ ░█████████    ░██  ░██  ░██  ░███████  ░██    ░██ ░██    ░██ ░█████████ 
 ░██   ░██ ░██   ░██  ░██ ░██    ░██       ░██ ░██           ░██       ░██ ░██   ░██  ░██   ░███ ░███   ░██ ░██        
  ░██████   ░█████░██ ░██ ░██    ░██       ░██  ░███████     ░██       ░██  ░█████░██  ░█████░██ ░██░█████   ░███████  
                                                                                             ░██                       
                                                                                       ░███████                        
        """
        self.models = models

    def get_model_name(self, arguments: dict[str, str]) -> str:
        console = Console()
        console.clear()
        console.print(f"{self.title}", style="blue")
        console.print("\nParameters:", style="red bold underline")
        console.print(
            *[
                f"    - [bold blue]{p[2:].center(25)}[/bold blue]: {v}"
                for p, v in arguments.items()
            ],
            sep="\n",
        )
        console.print("\nChoose your llm:\n", style="bold")
        for index, model in enumerate(self.models, start=1):
            console.print(f"    {index}: [yellow]{model}[/yellow]")
        console.print()
        console.print("[magenta bold]Type 'q' to abord[/magenta bold]")
        while True:
            value = readkey()
            if value.lower() == "q":
                console.print("Exiting...", style="bold blue")
                sys.exit()
            if not value.isnumeric():
                continue
            value = int(value)
            if len(self.models) >= value:
                console.print(
                    f"[green]Choosing {self.models[value - 1]}...[/green]"
                )
                break
            else:
                console.print("[red bold]Error: Invalid input[/red bold]")
        return self.models[value - 1]


if __name__ == "__main__":
    try:
        home = Home(["Qwen/Qwen3-0.6B", "HuggingFaceTB/SmolLM2-360M-Instruct"])
    except KeyboardInterrupt:
        ...
