# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    checker.py                                        :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 10:03:23 by nyramana         #+#    #+#              #
#    Updated: 2026/08/13 15:40:50 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module That contains the basic argument checker for the program."""

import os


class ArgumentError(Exception):
    """Basic argument error class."""


class Checker:
    """Class That checks if the parameter is Valid or not."""

    def __init__(self) -> None:
        """Everything starts here."""
        self._arguments = {
            "--functions_definition": "data/input/functions_definition.json",
            "--input": "data/input/function_calling_tests.json",
            "--output": "data/output/function_calls.json",
        }

    def check_args(self, args: list[str]) -> dict[str, str]:
        """
        Check and validate arguments for the input, output, and funcdef.

        Args:
            args (list[str]): Every argument to test and validate.
        Returns:
            dict: dictionnary that contains every arguments.
        """
        i = 0
        while i < len(args):
            flag = args[i]
            if flag not in self._arguments:
                raise ArgumentError(f"Parameter {flag} is invalid.")
            elif i + 1 >= len(args):
                raise ArgumentError(f"Missing value for parameter {flag}")
            self._validate_params(flag, args[i + 1])
            self._arguments[flag] = args[i + 1]
            i += 2
        return self._arguments

    def _validate_params(self, params: str, path: str) -> None:
        """
        Validate the parameter.

        Args:
            params (str): The flag.
            path (str): The path of the file.
        """
        if params == "--output":
            self._verify_output(path)
        self._verify_input(path)

    def _verify_output(self, path: str) -> None:
        """
        Verify if we can make the directory.

        Args:
            path (str): the path of the file.
        """
        dirname = os.path.dirname(path)
        if dirname:
            try:
                os.makedirs(dirname, exist_ok=True)
            except OSError as e:
                raise ArgumentError(f"Cannot create path directory: {e}.")
        try:
            with open(path, "w") as _:
                pass
        except OSError as e:
            raise ArgumentError(f"Cannot create file {path}: {e}")

    def _verify_input(self, path: str) -> None:
        """
        Try to read a file.

        Args:
            path (str): The path of the file.
        """
        try:
            with open(path, "r"):
                pass
        except OSError as e:
            raise ArgumentError(f"Invalid input argument {e}")
