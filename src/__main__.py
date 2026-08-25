# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __main__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/17 09:55:16 by nyramana         #+#    #+#              #
#    Updated: 2026/08/25 23:03:34 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Package that run the program."""


def main() -> None:
    """Program main entry point."""
    from .venv import check_depedencies

    if not check_depedencies():
        return

    from .main import Main

    main = Main()
    main.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"[ERROR] {e}")
        print("This should never happen.")
