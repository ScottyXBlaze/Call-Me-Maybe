# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    checker.py                                        :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 10:03:23 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 14:40:40 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module That contains the basic argument checker for the program."""

import os
import sys


class Checker:
    """Class That checks if the parameter is Valid or not."""

    def __init__(self) -> None:
        """Everything starts here."""
        self.args = {}

    def check_args(self, args: list[str]) -> None:
        """Check the arguments and validate them."""
        i = 0
        while i < len(args):
            flag = args[i]
            if flag not in self.args:
                print(f"Error: Unknown parameter '{flag}'", file=sys.stderr)
                sys.exit(1)

            if i + 1 >= len(args):
                print(
                    f"Error: Missing value for parameter '{flag}'",
                    file=sys.stderr,
                )
                sys.exit(1)

            self.validate_params(flag, sys.argv[i + 1])
            self.args[flag] = sys.argv[i + 1]
            i += 2

    def check_args2(self, args: list[str]) -> dict[str, str]:
        result: dict[str, str] = {}
        return result

    def validate_params(self, params: str, path: str) -> None:
        """
        Validate the parameter.

        Args:
            params (str): The flag.
            path (str): The path of the file.
        """
        if params == "--output":
            self.verify_output(path)
        self.verify_input(path)

    def verify_output(self, path: str) -> None:
        """
        Verify if we can make the directory.

        Args:
            path (str): the path of the file.
        """
        dirname = os.path.dirname(path)
        if dirname:
            try:
                os.makedirs(dirname, exist_ok=True)
                with open(path, "w") as _:
                    pass
            except Exception as e:
                print(
                    f"Error: Cannot create output directory '{dirname}': {e}",
                    file=sys.stderr,
                )
                sys.exit(1)

    def verify_input(self, path: str) -> None:
        """
        Try to read a file.

        Args:
            path (str): The path of the file.
        """
        try:
            with open(path, "r"):
                pass
        except Exception as e:
            print(f"Error: Cannot read file '{path}': {e}", file=sys.stderr)
            sys.exit(1)
