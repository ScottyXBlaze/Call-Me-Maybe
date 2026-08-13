# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/13 16:29:11 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main entry point of the program."""

import json
import sys

from pydantic import ValidationError

from .llm import MyLLM
from .model import FunctionCallResult, FunctionDefinition, Prompt
from .parsers import ArgumentError, Checker, Loader, Saver


def main() -> None:
    """Serve as a main entry point."""
    checker = Checker()
    loader = Loader()
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

    my_llm = MyLLM(func_defs, prompts)
    saver = Saver()
    result: list[FunctionCallResult] = my_llm.run()
    saver.save_function_calls(result, arguments["--output"])


if __name__ == "__main__":
    main()
