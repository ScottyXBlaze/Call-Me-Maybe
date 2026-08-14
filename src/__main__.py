# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/14 19:15:21 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main entry point of the program."""

import json
import sys

from pydantic import ValidationError
from rich.console import Console

from src.ui.home import Home

from .llm import MyLLM
from .model import FunctionCallResult, FunctionDefinition, Prompt
from .parsers import ArgumentError, Checker, Loader, Saver


def main() -> None:
    """Serve as a main entry point."""
    checker = Checker()
    loader = Loader()
    model_list = ["Qwen/Qwen3-0.6B", "HuggingFaceTB/SmolLM2-360M-Instruct"]
    try:
        arguments = checker.check_args(sys.argv[1:])
    except ArgumentError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    try:
        func_defs: list[FunctionDefinition] = loader.load_func_defs(
            arguments["--functions_definition"]
        )
        prompts: list[Prompt] = loader.load_prompts(arguments["--input"])
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid json file: {e}")
        sys.exit(1)
    except ValidationError as e:
        for error in e.errors():
            print(f"[ERROR] Invalid format for file: {error}")
        sys.exit(1)

    home_ui = Home(model_list)
    model = home_ui.get_model_name()
    my_llm = MyLLM(func_defs, prompts, model)
    saver = Saver()
    result: list[FunctionCallResult] = []
    console = Console()
    llm_func_calls = my_llm.run()
    try:
        while True:
            console.print_json(next(llm_func_calls).model_dump_json())
    except StopIteration as e:
        result = e.value
    saver.save_function_calls(result, arguments["--output"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        ...
