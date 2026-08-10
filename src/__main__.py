# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 13:16:51 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 15:40:06 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main entry point of the program."""

from .my_llm import My_LLM


class Main:
    """Main entry point of the program."""

    def __init__(self) -> None:
        """Everything starts here."""
        self.my_llm = My_LLM()

    def run(self) -> None:
        """Run the program."""
        self.my_llm.run()


if __name__ == "__main__":
    main = Main()
    main.run()
