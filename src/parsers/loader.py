# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    loader.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 13:15:18 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 15:43:07 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the loader file for the program."""

import json

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
        with open(path, "r") as r:
            result = json.load(r)
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
        with open(path, "r") as file:
            result = json.load(file)
        return [Prompt.model_validate(prompt) for prompt in result]
