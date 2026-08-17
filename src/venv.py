# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    venv.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/17 09:48:35 by nyramana         #+#    #+#              #
#    Updated: 2026/08/17 09:51:43 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from importlib import import_module


def check_depedencies() -> bool:
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
