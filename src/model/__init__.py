# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __init__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/07/21 16:44:23 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 15:25:13 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Package that contains every utility models."""

from .model import FunctionCallResult, FunctionDefinition, Prompt

__all__ = ["FunctionCallResult", "FunctionDefinition", "Prompt"]
