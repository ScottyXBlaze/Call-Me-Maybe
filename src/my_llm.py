# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    my_llm.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 14:08:13 by nyramana         #+#    #+#              #
#    Updated: 2026/08/03 14:11:18 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from llm_sdk import Small_LLM_Model

from .parser import Parser


class My_LLM:
    def __init__(self) -> None:
        self.model = Small_LLM_Model()
        self.parser = Parser()

        self.prompts = self.parser.load_prompts()
        self.function_defs = self.parser.load_function_definitions()

    def get_func_name(self) -> None:
        ...

    def get_func_args(self) -> None:
        ...

    def run(self) -> None:
        ...
