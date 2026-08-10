# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    model.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/07/21 16:44:05 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 15:40:18 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains every utility models."""

from typing import Any

from pydantic import BaseModel, Field


class Prompt(BaseModel):
    """Class that contains the prompt."""

    prompt: str = Field()


class ParameterInfo(BaseModel):
    """Class that contains the parameter of the function."""

    type: str = Field()


class FunctionDefinition(BaseModel):
    """Class that contains the function."""

    name: str = Field()
    description: str = Field()
    parameters: dict[str, ParameterInfo] = Field()
    returns: dict[str, str] = Field()


class FunctionCallResult(BaseModel):
    """Class that should contains the result of the prompt."""

    prompt: str = Field()
    name: str = Field()
    parameters: dict[str, Any] = Field()
