# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/11 13:58:03 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main entry point of the program."""

import json
import sys

from pydantic import ValidationError

from src.parsers.checker import ArgumentError

from .parsers import Checker, Loader


def main():
    checker = Checker()
    loader = Loader()

    try:
        arguments = checker.check_args(sys.argv[1:])
    except ArgumentError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
    try:
        func_defs = loader.load_func_defs(
            arguments.get(
                "--functions_definition",
                "data/input/function_calling_tests.json",
            )
        )
        prompts = loader.load_prompts(
            arguments.get("--input", "data/input/functions_definition.json")
        )
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid json file: {e}")
        sys.exit(1)
    except ValidationError as e:
        for error in e.errors():
            print(f"[ERROR] Invalid format for file: {error}")
        sys.exit(1)
    print(*[model.model_dump() for model in func_defs], sep="\n")
    print(*[model.model_dump() for model in prompts], sep="\n")


if __name__ == "__main__":
    main()
