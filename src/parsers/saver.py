# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    saver.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 09:53:19 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 12:11:38 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from typing import List

from model.model import FunctionCallResult


class Saver:
    def __init__(self, output_file: str) -> None:
        self.output_file = output_file

    def save_function_calls(self, results: List[FunctionCallResult]) -> None:
        serialized_output = [result.model_dump() for result in results]
        print(serialized_output)
