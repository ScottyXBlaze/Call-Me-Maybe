# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    saver.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/05 09:53:19 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 14:46:01 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from model.model import FunctionCallResult


class Saver:
    def __init__(self, output_file: str) -> None:
        self.output_file = output_file

    def save_function_calls(self, results: list[FunctionCallResult]) -> None:
        serialized_output = [result.model_dump() for result in results]
        print(serialized_output)
