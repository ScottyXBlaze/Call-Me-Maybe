# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    home.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/13 16:35:44 by nyramana         #+#    #+#              #
#    Updated: 2026/08/17 10:06:50 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the Home UI class for the program."""

import sys

from readchar import readkey
from rich.console import Console


class Home:
    """Base UI class for the Home and generation process."""

    def __init__(self, models: list[str]) -> None:
        """
        Everything starts here.

        Args:
            models (list[str]): The list of model to choose.
        """
        self.title = """
  ░██████             ░██ ░██    ░███     ░███               \
░███     ░███                       ░██                   .
 ░██   ░██            ░██ ░██    ░████   ░████               \
░████   ░████                       ░██                   .
░██         ░██████   ░██ ░██    ░██░██ ░██░██  ░███████     \
░██░██ ░██░██  ░██████   ░██    ░██ ░████████   ░███████  .
░██              ░██  ░██ ░██    ░██ ░████ ░██ ░██    ░██    \
░██ ░████ ░██       ░██  ░██    ░██ ░██    ░██ ░██    ░██ .
░██         ░███████  ░██ ░██    ░██  ░██  ░██ ░█████████    \
░██  ░██  ░██  ░███████  ░██    ░██ ░██    ░██ ░█████████ .
 ░██   ░██ ░██   ░██  ░██ ░██    ░██       ░██ ░██           \
░██       ░██ ░██   ░██  ░██   ░███ ░███   ░██ ░██        .
  ░██████   ░█████░██ ░██ ░██    ░██       ░██  ░███████     \
░██       ░██  ░█████░██  ░█████░██ ░██░█████   ░███████  .
                                                             \
                                ░██                       .
                                                             \
                          ░███████                        .
        """
        self.models = models
        self.console = Console()

    def get_model_name(self, arguments: dict[str, str]) -> str:
        """
        Get the model name.

        Args:
            arguments (dict[str, str]): The list of arguments.
        Returns:
            str: The name of the model.
        """
        self.console.print("\nChoose your llm:\n", style="bold")
        for index, model in enumerate(self.models, start=1):
            self.console.print(f"    {index}: [yellow]{model}[/yellow]")
        self.console.print()
        self.console.print("[magenta bold]Type 'q' to abord[/magenta bold]")
        while True:
            value = readkey()
            if value.lower() == "q":
                self.console.print("Exiting...", style="bold blue")
                sys.exit()
            if not value.isnumeric():
                continue
            casted_value = int(value)
            if len(self.models) >= casted_value:
                self.console.print(
                    f"""[green]Choosing {self.models[casted_value - 1]}\
...[/green]""",
                )
                break
            else:
                self.console.print("[red bold]Error: Invalid input[/red bold]")
        return self.models[casted_value - 1]

    def print_header(self) -> None:
        """Print the header of the program."""
        self.console.print(f"{self.title}", style="blue")

    def print_parameters(self, arguments: dict[str, str]) -> None:
        self.console.print("\nParameters:", style="red bold underline")
        self.console.print(
            *[
                f"    - [bold blue]{p[2:].center(25)}[/bold blue]: {v}"
                for p, v in arguments.items()
            ],
            sep="\n",
        )
