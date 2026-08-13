# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    saver.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 09:53:19 by nyramana         #+#    #+#              #
#    Updated: 2026/08/13 15:24:41 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contain the basic saver for the program."""

import json
import sys

from ..model import FunctionCallResult


class Saver:
    """Class that contains method to save the function call result json."""

    def save_function_calls(
        self, results: list[FunctionCallResult], path: str
    ) -> None:
        """
        Save the function calls data into a file.

        Args:
            results (list[FunctionCallResult]): The list of function calls.
            path (str): The path of the file.
        """
        function_dict = [result.model_dump() for result in results]
        obj = json.dumps(function_dict, indent=4)
        try:
            with open(path, "w") as file:
                file.write(obj)
        except OSError as e:
            print(f"[ERROR] {e}")
            print("This should never crash!")
            sys.exit()
