# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __init__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 16:44:32 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 11:31:43 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""
Package that contains all the LLM implementation.

There are a lot of llm implementation here like Finite State Machine,
constrained decoding, Custom LLM method, ...
"""
from .custom_llm import CustomLLM

__all__ = ["CustomLLM"]
