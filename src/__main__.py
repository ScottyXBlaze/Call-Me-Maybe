# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/17 09:55:16 by nyramana         #+#    #+#              #
#    Updated: 2026/08/17 10:07:36 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Package that run the program."""

from .main import Main
from .venv import check_depedencies


def main() -> None:
    if not check_depedencies():
        return
    main = Main()
    main.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
