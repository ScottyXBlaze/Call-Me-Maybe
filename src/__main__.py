# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 09:51:28 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main entry point of the program."""

import json
import sys

from pydantic import ValidationError
from rich.console import Console
from rich.progress import track

from .llm import MyLLM
from .model import FunctionCallResult, FunctionDefinition, Prompt
from .parsers import ArgumentError, Checker, Loader, Saver
from .ui import Home


class Main:
    """Class that contains the main entry point."""

    def __init__(self) -> None:
        """Everything starts here."""
        self.checker = Checker()
        self.loader = Loader()
        self.saver = Saver()
        self.model_list = [
            "Qwen/Qwen3-0.6B",
            "HuggingFaceTB/SmolLM2-360M-Instruct",
        ]

        self.ui = Home(self.model_list)
        self.console = Console()

        self.arguments = self.get_args()

    def get_args(self) -> dict[str, str]:
        """
        Get the argument of the program stored in sys.argv and validate them.

        Returns:
            dict: The name of the flag and it's value.
        """
        try:
            arguments = self.checker.check_args(sys.argv[1:])
        except ArgumentError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
        return arguments

    def load_args(
        self, arguments: dict[str, str]
    ) -> tuple[list[FunctionDefinition], list[Prompt]]:
        """
        Load every argument and put them in the pydantic validator.

        Args:
            arguments (dict[str, str]): the list of arguments.
        Returns:
            tuple: the list of func_defs and prompts.
        """
        try:
            func_defs: list[FunctionDefinition] = self.loader.load_func_defs(
                arguments["--functions_definition"]
            )
            prompts: list[Prompt] = self.loader.load_prompts(
                arguments["--input"]
            )
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid json file: {e}")
            sys.exit(1)
        except ValidationError as e:
            for error in e.errors():
                print(f"[ERROR] Invalid format for file: {error}")
            sys.exit(1)
        return func_defs, prompts

    def run(self) -> None:
        """Run the program."""
        if self.arguments.get("--bonus"):
            self.run_bonus()
        else:
            self.run_nornal()

    def run_bonus(self) -> None:
        """Run the bonus program."""
        func_defs, prompts = self.load_args(self.arguments)
        model = self.ui.get_model_name(self.arguments)
        llm = MyLLM(func_defs, prompts, model)
        llm_func_calls = llm.run()
        try:
            while True:
                self.console.print_json(
                    next(llm_func_calls).model_dump_json(), indent=4
                )
        except StopIteration as e:
            result = e.value
        self.saver.save_function_calls(result, self.arguments["--output"])

    def run_nornal(self) -> None:
        """Run the normal program."""
        func_defs, prompts = self.load_args(self.arguments)
        llm = MyLLM(func_defs, prompts)
        llm_func_calls = llm.run()
        result: list[FunctionCallResult] = []
        try:
            for i in track(
                range(len(prompts)),
                "Generating the function call...",
                console=self.console,
            ):
                self.console.print(
                    next(llm_func_calls).prompt.center(79),
                    "[bold green]DONE![/bold green]",
                )
        except StopIteration as e:
            result = e.value
        self.saver.save_function_calls(result, self.arguments["--output"])


if __name__ == "__main__":
    try:
        main = Main()
        main.run()
    except KeyboardInterrupt:
        ...
