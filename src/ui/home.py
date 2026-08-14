# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    home.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/13 16:35:44 by nyramana         #+#    #+#              #
#    Updated: 2026/08/14 15:14:04 by nyramana        ###   ########.fr        #
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

    def get_model_name(self) -> str:
        console = Console()
        console.clear()
        console.print(f"{self.title}", style="blue")
        console.print("Choose your llm:\n", style="bold")
        for index, model in enumerate(self.models, start=1):
            console.print(f"    {index}: [yellow]{model}[/yellow]")
        while True:
            console.print()
            value = readkey()
            if value.lower() == "q":
                console.print("Exiting...", style="blue")
                sys.exit()
            if not value.isnumeric():
                console.print("[red]Error: Invalid input[/red]")
                continue
            value = int(value)
            if len(self.models) >= value:
                console.print(f"[green]Choosing {self.models[value - 1]}...[/green]")
                break
            else:
                console.print("[red bold]Error: Invalid input[/red bold]")
        return self.models[value - 1]


if __name__ == "__main__":
    try:
        home = Home(["Qwen/Qwen3-0.6B", "HuggingFaceTB/SmolLM2-360M-Instruct"])
        home.get_model_name()
    except KeyboardInterrupt:
        ...
