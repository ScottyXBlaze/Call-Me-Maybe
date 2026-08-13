# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    output.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/13 15:15:59 by nyramana         #+#    #+#              #
#    Updated: 2026/08/13 15:19:18 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains basic of the output class for the project."""

from typing import Any

from pydantic import BaseModel, Field


class FunctionCallResult(BaseModel):
    """Class that should contains the result of the prompt."""

    prompt: str = Field()
    name: str = Field()
    parameters: dict[str, Any] = Field()
