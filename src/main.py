# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    main.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#   By: nyramana <nyramana@student.42antananariv   +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#   Created: 2026/08/03 13:16:51 by nyramana          #+#    #+#              #
#    Updated: 2026/08/17 16:58:32 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main entry point of the program."""

import json
import sys
import time
from collections.abc import Generator
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

from .custom_llm import CustomLLM
from .model import FunctionDefinition, Prompt
from .parsers import ArgumentError, Checker, Loader, Saver
from .ui import Home


class Main:
    """Class that contains the main entry point."""

    def __init__(self) -> None:
        """Initialize components and parse command line arguments."""
        self._checker = Checker()
        self._loader = Loader()
        self._saver = Saver()
        self._console = Console()
        self._model_list = [
            "Qwen/Qwen3-0.6B",
            "HuggingFaceTB/SmolLM2-360M-Instruct",
        ]
        self._ui = Home(self._model_list)
        self._arguments = self._get_args()

    def _get_args(self) -> dict[str, str]:
        """
        Get the program arguments stored in sys.argv and validate them.

        Returns:
            dict[str, str]: Mapping of flag names to their values.
        """
        try:
            return self._checker.check_args(sys.argv[1:])
        except ArgumentError as e:
            self._console.print(f"[bold red][ERROR][/bold red] {e}")
            sys.exit(1)

    def _load_args(
        self, arguments: dict[str, str]
    ) -> tuple[list[FunctionDefinition], list[Prompt]]:
        """
        Load argument files and parse them using Pydantic models.

        Args:
            arguments (dict[str, str]): Parsed command-line arguments.

        Returns:
            tuple[list[FunctionDefinition], list[Prompt]]: Function
            definitions and prompts.
        """
        try:
            func_defs = self._loader.load_func_defs(
                arguments["--functions_definition"]
            )
            prompts = self._loader.load_prompts(arguments["--input"])
            return func_defs, prompts
        except json.JSONDecodeError as e:
            self._console.print(
                f"[bold red][ERROR][/bold red] Invalid JSON file: {e}"
            )
            sys.exit(1)
        except ValidationError as e:
            for error in e.errors():
                loc = " -> ".join(str(x) for x in error.get("loc", []))
                msg = error.get("msg", str(error))
                self._console.print(
                    f"[bold red][ERROR][/bold red]\
Invalid format at {loc}: {msg}"
                )
            sys.exit(1)

    def _process_stream(
        self,
        func_calls: Generator[Any, None, Any],
        is_bonus: bool,
        total_prompts: int,
    ) -> tuple[Any, float]:
        """
        Print and process the program.

        It consume the generation stream, manage UI updates,
        and measure total elapsed time.
        Args:
            func_calls (Generator): LLM generation stream.
            is_bonus (bool): Whether bonus mode is enabled.
            total_prompts (int): Total number of input prompts.

        Returns:
            tuple[Any, float]: Final execution result and total time spent.
        """
        total_time = 0.0

        if is_bonus:
            while True:
                try:
                    start = time.perf_counter()
                    item = next(func_calls)
                    total_time += time.perf_counter() - start
                    self._console.print_json(item.model_dump_json())
                except StopIteration as e:
                    return e.value, total_time

        with Progress(
            SpinnerColumn(),
            TextColumn("[magenta]Generating..."),
            BarColumn(),
            TaskProgressColumn(),
            console=self._console,
        ) as progress:
            task = progress.add_task("Generating...", total=total_prompts)
            while True:
                try:
                    start = time.perf_counter()
                    item = next(func_calls)
                    done = time.perf_counter() - start
                    total_time += done

                    progress.console.print(
                        f"[bold green]DONE! ({done:05.2f}s)\
[/bold green] {item.prompt}"
                    )
                    progress.update(task, advance=1)
                except StopIteration as e:
                    return e.value, total_time

    def run(self) -> None:
        """Run the main execution flow."""
        self._console.clear()
        self._ui.print_header()

        func_defs, prompts = self._load_args(self._arguments)
        is_bonus = bool(self._arguments.get("--bonus"))

        if is_bonus:
            model = self._ui.get_model_name(self._arguments)
            llm = CustomLLM(func_defs, prompts, model)
        else:
            llm = CustomLLM(func_defs, prompts)

        llm_func_calls = llm.run()
        result, total_time = self._process_stream(
            llm_func_calls, is_bonus, len(prompts)
        )

        output_path = self._arguments["--output"]
        self._console.print(
            f"\nGeneration done in {total_time:.2f} seconds\n",
            style="bold green",
        )
        self._console.print(f"Saving the function call in {output_path}")
        self._saver.save_function_calls(result, output_path)
