# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    llm.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 15:51:08 by nyramana         #+#    #+#              #
#    Updated: 2026/08/11 14:06:46 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


from ..model import FunctionCallResult, FunctionDefinition, Prompt
from .tokenizer import Tokenizer


class MyLLM:
    def __init__(
        self, func_defs: list[FunctionDefinition], prompts: list[Prompt]
    ) -> None:
        self.tokenizer = Tokenizer()
        self.func_defs = func_defs
        self.prompts = prompts

    def generate_func_name(self) -> None: ...

    def generate_func_args(self) -> None: ...

    def generate_func_arg(self) -> None: ...

    def generate_func_call(self, prompt: Prompt) -> None: ...

    def run(self) -> list[FunctionCallResult]: ...
