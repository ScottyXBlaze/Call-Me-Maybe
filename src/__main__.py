# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 09:14:55 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main entry point of the program."""

import json
import sys

from pydantic import ValidationError
from rich.console import Console

from .llm import MyLLM
from .model import FunctionDefinition, Prompt
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
        arguments = self.get_args()
        func_defs, prompts = self.load_args(arguments)
        model = self.ui.get_model_name(arguments)
        llm = MyLLM(func_defs, prompts, model)
        llm_func_calls = llm.run()
        try:
            while True:
                self.console.print_json(
                    next(llm_func_calls).model_dump_json(), indent=4
                )
        except StopIteration as e:
            result = e.value
        self.saver.save_function_calls(result, arguments["--output"])


if __name__ == "__main__":
    try:
        main = Main()
        main.run()
    except KeyboardInterrupt:
        ...
