# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    parser.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/07/21 16:43:42 by nyramana         #+#    #+#              #
#    Updated: 2026/08/05 10:02:37 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the parser part of the program."""

import json
import os
import sys
from typing import List

from pydantic import ValidationError

from .model import FunctionCallResult, FunctionDefinition


class ArgumentError(Exception):
    """Special Error for argument."""

    def __init__(self, *args: object) -> None:
        """
        Everything starts here.

        Args:
            args (object): Every arguments you need.
        """
        if not self.args:
            self.args = ("Unknown argument error",)
        super().__init__(*args)


class Parser:
    """
    Special Parser class for the program.

    It has utility method like trying to read a file or write a file
    """

    def __init__(self) -> None:
        """Special Parser class for the program."""
        self.args = {
            "--functions_definition": "data/input/functions_definition.json",
            "--input": "data/input/function_calling_tests.json",
            "--output": "data/output/function_calls.json",
        }

    def check_args(self) -> None:
        """Check the arguments and validate them."""
        i = 1
        while i < len(sys.argv):
            flag = sys.argv[i]
            if flag not in self.args:
                print(f"Error: Unknown parameter '{flag}'", file=sys.stderr)
                sys.exit(1)

            if i + 1 >= len(sys.argv):
                print(
                    f"Error: Missing value for parameter '{flag}'",
                    file=sys.stderr,
                )
                sys.exit(1)

            self.validate_params(flag, sys.argv[i + 1])

            self.args[flag] = sys.argv[i + 1]
            i += 2

    def validate_params(self, params: str, path: str) -> None:
        """
        Validate the parameter.

        Args:
            params (str): The flag.
            path (str): The path of the file.
        """
        if params == "--output":
            self.verify_output_directory(path)
        self.try_read(path)

    def verify_output_directory(self, path: str) -> None:
        """
        Verify if we can make the directory.

        Args:
            path (str): the path of the file.
        """
        dirname = os.path.dirname(path)
        if dirname:
            try:
                os.makedirs(dirname, exist_ok=True)
            except Exception as e:
                print(
                    f"Error: Cannot create output directory '{dirname}': {e}",
                    file=sys.stderr,
                )
                sys.exit(1)

    def try_read(self, path: str) -> None:
        """
        Try to read a file.

        Args:
            path (str): The path of the file.
        """
        try:
            with open(path, "r", encoding="utf-8"):
                pass
        except Exception as e:
            print(f"Error: Cannot read file '{path}': {e}", file=sys.stderr)
            sys.exit(1)

    def load_function_definitions(self) -> List[FunctionDefinition]:
        """
        Load and validate the function definitions file.

        Returns:
            List: The list of the function definition class.
        """
        filepath = self.args["--functions_definition"]
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("The file must contain a JSON list.")
            return [FunctionDefinition(**item) for item in data]
        except (
            FileNotFoundError,
            json.JSONDecodeError,
            ValueError,
            ValidationError,
        ) as e:
            print(
                f"Error during loading definitions ({filepath}): {e}",
                file=sys.stderr,
            )
            sys.exit(1)

    def load_prompts(self) -> List[str]:
        """
        Load the prompt file.

        Returns:
            List: The list of string that contains de prompt.
        """
        filepath = self.args["--input"]
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("The file must contain a JSON list.")

            prompts: List[str] = []
            for item in data:
                if isinstance(item, dict) and "prompt" in item:
                    prompts.append(str(item["prompt"]))
            return prompts
        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(
                f"Error while loading file ({filepath}): {e}", file=sys.stderr
            )
            sys.exit(1)

    def save_function_calls(self, results: List[FunctionCallResult]) -> None:
        """
        Save the function call to the output file.

        Args:
            results (List[FunctionCallResult]): The list of class
            that contains the file.
        """
        filepath = self.args["--output"]
        try:
            serialized_results = [result.model_dump() for result in results]
            os.makedirs(os.path.join(*filepath.split("/")[:-1]))
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(serialized_results, f, indent=2, ensure_ascii=False)
            print(f"Success: {len(results)} saved in {filepath}")
        except Exception as e:
            print(
                f"Error while saving function call ({filepath}): {e}",
                file=sys.stderr,
            )
            print(
                f"Error while saving function call ({filepath}): {e}",
                file=sys.stderr,
            )
            sys.exit(1)
