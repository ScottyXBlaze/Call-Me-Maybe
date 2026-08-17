# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    venv.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/17 09:48:35 by nyramana         #+#    #+#              #
#    Updated: 2026/08/17 10:51:39 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the checker for the dependencies."""

from importlib import import_module


def check_depedencies() -> bool:
    """
    Check the depedencies of the program.

    Returns:
        bool: True if everything is OK.
    """
    dependencies = {"pydantic", "readchar", "rich"}
    missing = set()
    for dependency in dependencies:
        try:
            import_module(dependency)
        except ImportError:
            missing.add(dependency)
    if missing:
        print(f"[ERROR] Missing dependency {', '.join(missing)}")
        return False
    return True
