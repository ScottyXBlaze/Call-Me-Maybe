# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    main.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/17 11:21:01 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main entry point of the program."""

import json
import sys
import time
from typing import Any

from pydantic import ValidationError
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
)

from .llm import CustomLLM
from .model import FunctionDefinition, Prompt
from .parsers import ArgumentError, Checker, Loader, Saver
from .ui import Home


class Main:
    """Class that contains the main entry point."""

    def __init__(self) -> None:
        """Everything starts here."""
        self._checker = Checker()
        self._loader = Loader()
        self._saver = Saver()
        self._model_list = [
            "Qwen/Qwen3-0.6B",
            "HuggingFaceTB/SmolLM2-360M-Instruct",
        ]

        self._ui = Home(self._model_list)
        self._console = Console()

        self._arguments = self._get_args()

    def _get_args(self) -> dict[str, str]:
        """
        Get the argument of the program stored in sys.argv and validate them.

        Returns:
            dict: The name of the flag and it's value.
        """
        try:
            arguments: dict[str, str] = self._checker.check_args(sys.argv[1:])
        except ArgumentError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
        return arguments

    def _load_args(
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
            func_defs: list[FunctionDefinition] = self._loader.load_func_defs(
                arguments["--functions_definition"]
            )
            prompts: list[Prompt] = self._loader.load_prompts(
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
        self._console.clear()
        self._ui.print_header()
        func_defs, prompts = self._load_args(self._arguments)
        if self._arguments.get("--bonus"):
            model = self._ui.get_model_name(self._arguments)
            llm = CustomLLM(func_defs, prompts, model)
        else:
            llm = CustomLLM(func_defs, prompts)
        llm_func_calls = llm.run()
        len_prompts = len(prompts)
        if self._arguments.get("--bonus"):
            self._run_bonus(llm_func_calls, len_prompts)
        else:
            self._run_nornal(llm_func_calls, len_prompts)

    def _run_bonus(self, func_calls: Any, len_prompts: int) -> None:
        """Run the bonus program."""
        total = 0.0
        try:
            while True:
                try:
                    start = time.perf_counter()
                    item = next(func_calls)
                    self._console.print_json(item.model_dump_json())
                    done = time.perf_counter() - start
                    total += done
                except StopIteration as e:
                    result = e.value
                    break
        except StopIteration as e:
            result = e.value
        self._console.print(
            f"\nGeneration done in {total:.2f} second\n", style="bold green"
        )
        self._console.print(
            f"Saving the function call in {self._arguments['--output']}"
        )
        self._saver.save_function_calls(result, self._arguments["--output"])

    def _run_nornal(self, func_calls: Any, len_prompts: int) -> None:
        """Run the normal program."""
        total = 0.0
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[magenta]Generating..."),
                BarColumn(),
                TaskProgressColumn(),
            ) as progress:
                task = progress.add_task(
                    "Generating...",
                    total=len_prompts,
                )

                while True:
                    try:
                        start = time.perf_counter()
                        item = next(func_calls)
                        done = time.perf_counter() - start
                        total += done
                    except StopIteration as e:
                        result = e.value
                        break

                    progress.console.print(
                        f"[bold green]DONE! ({done:05.2f}s)\
[/bold green] {item.prompt}"
                    )

                    progress.update(task, advance=1)

        except StopIteration as e:
            result = e.value
        self._console.print(
            f"\nGeneration done in {total:.2f} second\n", style="bold green"
        )
        self._console.print(
            f"Saving the function call in {self._arguments['--output']}"
        )
        self._saver.save_function_calls(result, self._arguments["--output"])
