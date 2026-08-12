# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    llm.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 15:51:08 by nyramana         #+#    #+#              #
#    Updated: 2026/08/12 16:09:02 by nyramana        ###   ########.fr        #
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
        self._valid_type = {
            "number": self._tokenizer.get_token("number"),
            "boolean": self._tokenizer.get_token("boolean"),
            "string": self._tokenizer.get_token("string"),
        }

    def generate_func_name(
        self, prompt: Prompt, func_name_token: list[list[int]]
    ) -> dict[str, str]:
        tmp_prompt = f"""Choose the exact function name from the list that best answers the prompt.

### Example
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
        decoded_name = self._argument_generator.generate_from_tokens(
            tmp_prompt, func_name_token
        )
        return {"name": decoded_name}

    def generate_func_args(
        self, prompt: Prompt, func_name: str
    ) -> dict[str, Any]:
        signature = self.get_func_signature(func_name)
        if not signature:
            return {"parameters": {}}
        base_prompt = f"""Task: Extract argument values directly from the \
request.
Rules:
1. Do not calculate, solve or compute math.
2. Copy exact words or values.
3. When a parameters is finished, put a new line '\n'.

Request: "{prompt}"
Function: {func_name}

JSON Output:
"""
        buffer = "{\n"
        result = {}
        params_items = list(signature.items())
        print(params_items)
        for index, (param_name, param_info) in enumerate(params_items):
            parameter_type = self.get_param_type(param_info)

            if parameter_type == "string":
                prefix = f'    "{param_name}": "'
            else:
                prefix = f'    "{param_name}": '

            buffer += prefix
            current_prompt = base_prompt + buffer
            value = self._argument_generator.get_arg_value(
                current_prompt, param_name, parameter_type
            )
            result[param_name] = value
            if parameter_type == "string":
                buffer += f'{value}"'
            elif parameter_type == "boolean":
                buffer += "true" if value else "false"
            else:
                buffer += str(value)

            if index < len(params_items) - 1:
                buffer += ",\n"
            else:
                buffer += "\n}"

        print(result)
        return {"parameters": result}

    def generate_func_arg(self) -> None: ...

    def generate_func_call(
        self, prompt: Prompt, func_name_tokens
    ) -> FunctionCallResult:
        result = {"prompt": prompt.prompt}
        result.update(self.generate_func_name(prompt, func_name_tokens))
        result.update(self.generate_func_args(prompt, result["name"]))
        return FunctionCallResult.model_validate(result)

    def get_func_signature(self, func_name: str) -> dict[str, Any]:
        for func in self._func_defs:
            if func_name == func.name:
                value = {
                    k: "".join(str(x) for x in v.model_dump().values() if x)
                    for k, v in func.parameters.items()
                }
                return value
        return {}

    def get_param_type(self, p_type: str) -> str:
        tmp_prompt = f"""Choose the best name that match the string.

list of name: {self._valid_type}
String: {p_type}
Best match: """
        func_tokens = []
        for base_type in self._valid_type:
            func_tokens += self._tokenizer.get_token(base_type)
        decoded_name = self._argument_generator.generate_from_tokens(
            tmp_prompt, func_tokens
        )
        return decoded_name

    def run(self) -> list[FunctionCallResult]:
        result: list[FunctionCallResult] = []
        func_tokens = []
        for func in self._func_defs:
            func_tokens += self._tokenizer.get_token(func.name)
        for prompt in self._prompts:
            func_call = self.generate_func_call(prompt, func_tokens)
            result.append(func_call)
        return result
