# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    model.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/07/21 16:44:05 by nyramana         #+#    #+#              #
#    Updated: 2026/08/03 13:45:52 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains every utility models."""

from typing import Any, Dict

from pydantic import BaseModel, Field


class ParameterInfo(BaseModel):
    """Class that contains the parameter of the function."""

    type: str = Field()


class FunctionDefinition(BaseModel):
    """Class that contains the function."""

    name: str = Field()
    description: str = Field()
    parameters: Dict[str, ParameterInfo] = Field()
    returns: Dict[str, str] = Field()


class FunctionCallResult(BaseModel):
    """Class that should contains the result of the prompt."""

    prompt: str = Field()
    name: str = Field()
    parameters: Dict[str, Any] = Field()
