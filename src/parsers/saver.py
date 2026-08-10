# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    saver.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 09:53:19 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 15:44:12 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contain the basic saver for the program."""

from ..model import FunctionCallResult


class Saver:
    """Class that contains method to save the function call result json."""

    # TODO: Add the saving class
    def save_function_calls(
        self, results: list[FunctionCallResult], path: str
    ) -> None:
        """
        Save the function calls data into a file.

        Args:
            results (list[FunctionCallResult]): The list of function calls.
            path (str): The path of the file.
        """
