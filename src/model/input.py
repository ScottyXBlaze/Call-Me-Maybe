# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    input.py                                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/07/21 16:44:05 by nyramana         #+#    #+#              #
#    Updated: 2026/08/31 10:43:27 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains basic class for the inpu part of the program."""

from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Prompt(BaseModel):
    """Class that contains the prompt."""

    model_config = ConfigDict(extra="forbid")
    prompt: str = Field()

    @model_validator(mode="after")
    def check_prompt(self) -> Self:
        """Check if the prompt is valid or not."""
        if not self.prompt.strip():
            raise ValueError("Prompt cannot be empty")
        return self


class ParameterInfo(BaseModel):
    """Class that contains the parameter of the function."""

    model_config = ConfigDict(extra="forbid")
    type: str = Field()

    @model_validator(mode="after")
    def check_param_info(self) -> Self:
        """Check if the parameter type is valid or not."""
        if not self.type.strip():
            raise ValueError("Parameter type cannot be empty")
        return self


class FunctionDefinition(BaseModel):
    """Class that contains the function."""

    model_config = ConfigDict(extra="forbid")
    name: str = Field()
    description: str = Field()
    parameters: dict[str, ParameterInfo] = Field()
    returns: dict[str, str] = Field()

    @model_validator(mode="after")
    def check_func_name(self) -> Self:
        """Check if the function name is valid or not."""
        if not self.name.strip():
            raise ValueError("Function name cannot be empty")
        return self

    @model_validator(mode="after")
    def check_func_desc(self) -> Self:
        """Check if the function description is valid or not."""
        if not self.description.strip():
            raise ValueError("Function description cannot be empty")
        return self
