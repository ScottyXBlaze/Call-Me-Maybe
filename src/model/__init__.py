# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __init__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/07/21 16:44:23 by nyramana         #+#    #+#              #
#    Updated: 2026/08/13 15:18:31 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""
Package that contains every utility models for the program.

These class are a pydantic class and serves as validator for the json format
and output format.
"""

from .input import FunctionDefinition, Prompt
from .output import FunctionCallResult

__all__ = ["FunctionCallResult", "FunctionDefinition", "Prompt"]
