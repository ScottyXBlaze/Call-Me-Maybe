# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    loader.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 13:15:18 by nyramana         #+#    #+#              #
#    Updated: 2026/08/13 15:39:12 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the loader file for the program."""

import json
import sys

from ..model import FunctionDefinition, Prompt


class Loader:
    """Class that loads function definitions and prompts."""

    def load_func_defs(self, path: str) -> list[FunctionDefinition]:
        """
        Load the function definition file.

        Args:
            path (str): The path of the file.
        Returns:
            list: The list of function definitions.
        """
        try:
            with open(path, "r") as r:
                result = json.load(r)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
        return [
            FunctionDefinition.model_validate(func_defs)
            for func_defs in result
        ]

    def load_prompts(self, path: str) -> list[Prompt]:
        """
        Load the prompt file.

        Args:
            path (str): The path of the file.
        Returns:
            list: The list of prompts.
        """
        try:
            with open(path, "r") as file:
                result = json.load(file)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
        return [Prompt.model_validate(prompt) for prompt in result]
