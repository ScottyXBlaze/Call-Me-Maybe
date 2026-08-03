# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/03 13:42:18 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from llm_sdk import Small_LLM_Model


class Main:
    def __init__(self) -> None:
        self.model = Small_LLM_Model()

    def run(self) -> None:
        print("AHAHAH")


if __name__ == "__main__":
    main = Main()
    main.run()

