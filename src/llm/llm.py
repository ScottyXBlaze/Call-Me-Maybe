# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    llm.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 15:51:08 by nyramana         #+#    #+#              #
#    Updated: 2026/08/12 07:03:31 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


from typing import Any

from ..model import FunctionCallResult, FunctionDefinition, Prompt
from .generator import ArgumentGenerator
from .tokenizer import Tokenizer


class MyLLM:
    def __init__(
        self, func_defs: list[FunctionDefinition], prompts: list[Prompt]
    ) -> None:
        self._tokenizer = Tokenizer()
        self._func_defs = func_defs
        self._prompts = prompts
        self._func_desc = [
            f"- {a.name}: {a.description}\n" for a in self._func_defs
        ]
        self._argument_generator = ArgumentGenerator(self._tokenizer)

    def generate_func_name(
        self, prompt: Prompt, func_name_token: list[list[int]]
    ) -> dict[str, str]:
        tmp_prompt = f"""
Choose the exact function name from the list that best answers the prompt.

### Example 1
Functions:
- calculate_sum: Adds two numbers
- convert_to_upper: Converts text to uppercase

prompt:'What is 15 plus 10?'
Function: calculate_sum

### Real Task
Functions:
{''.join(self._func_desc)}

{prompt}
Function: """
        decoded_name = self._argument_generator.generate_from_list(tmp_prompt, func_name_token)
        return {"name": decoded_name}

    def generate_func_args(
        self, prompt: Prompt, func_name: str
    ) -> dict[str, Any]:
        return {}

    def generate_func_arg(self) -> None: ...

    def generate_func_call(
        self, prompt: Prompt, func_name_tokens
    ) -> FunctionCallResult:
        result = {"prompt": prompt.prompt}
        result.update(self.generate_func_name(prompt, func_name_tokens))
        result.update(self.generate_func_args(prompt, result["name"]))
        print(result)
        return FunctionCallResult.model_validate(result)

    def get_func_signature(self, func_name) -> dict[str, Any]:
        for func in self._func_defs:
            if func_name == func.name:
                value = {
                    k: "".join(str(x) for x in v.model_dump().values() if x)
                    for k, v in func.parameters.items()
                }
                return value
        return {}

    def run(self) -> list[FunctionCallResult]:
        result: list[FunctionCallResult] = []
        func_tokens = []
        for func in self._func_defs:
            func_tokens += self._tokenizer.get_token(func.name)
        for prompt in self._prompts:
            func_call = self.generate_func_call(prompt, func_tokens)
            result.append(func_call)
        return result
