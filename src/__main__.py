# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/03 14:18:08 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from .parser import Parser

from .my_llm import My_LLM

class Main:
    def __init__(self) -> None:
        self.parser = Parser()
        self.my_llm = My_LLM()

    def run(self) -> None:
        self.my_llm.run()


if __name__ == "__main__":
    main = Main()
    main.run()
