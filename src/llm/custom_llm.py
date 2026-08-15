# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    llm.py                                            :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 15:51:08 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 11:13:28 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the main file for the llm."""

from collections.abc import Generator as Gen
from typing import Any

from ..model import FunctionCallResult, FunctionDefinition, Prompt
from .generator import Generator
from .tokenizer import Tokenizer


class CustomLLM:
    """
    The Base class for the LLM.

    Here belongs the main part of the program where we use the constrained
    decoding, the finite state machine, and much more to return the json file.
    """

    def __init__(
        self,
        func_defs: list[FunctionDefinition],
        prompts: list[Prompt],
        model: str = "Qwen/Qwen3-0.6B",
    ) -> None:
        """
        Everything starts here.

        Args:
            func_defs (list[FunctionDefinition]): The list of function
            definitions.
            prompts (list[Prompt]): The list of prompts.
            models (str): Model to use.
        """
        self._tokenizer = Tokenizer(model)
        self._func_defs = func_defs
        self._prompts = prompts
        self._func_desc = [
            f"- {a.name}: {a.description}\n" for a in self._func_defs
        ]
        self._argument_generator = Generator(self._tokenizer)

        self._valid_type = {
            "number": self._tokenizer.get_token("number"),
            "boolean": self._tokenizer.get_token("boolean"),
            "string": self._tokenizer.get_token("string"),
            "integer": self._tokenizer.get_token("integer"),
        }

    def generate_func_name(
        self, prompt: Prompt, func_name_token: list[list[int]]
    ) -> dict[str, str]:
        """
        Generate the name of the function.

        Args:
            prompt (Prompt): The initial prompt or question.
            func_name_token (list[list[int]]): The list of valid token.
        Returns:
            dict: A dictionnary that contains the function name with it's key.
        """
        tmp_prompt = f"""
Choose the exact function name from the list that best answers the prompt.

### Example
Functions:
- calculate_sum: Adds two numbers
- convert_to_upper: Converts text to uppercase

prompt:'What is 15 plus 10?'
Function: calculate_sum

### Real Task
Functions:
{''.join(self._func_desc)}

prompt:'{prompt.prompt}'
Function: """
        decoded_name = self._tokenizer.generate_from_tokens(
            tmp_prompt, func_name_token
        )
        return {"name": decoded_name}

    def generate_func_args(
        self, prompt: Prompt, func_name: str
    ) -> dict[str, Any]:
        """
        Generate the function arguments based on the function name and prompt.

        Args:
            prompt (Prompt): The initial prompt / question.
            func_name (str): The name of the function.
        Returns:
            dict: A dictionnary that contains the function
            arguments with it's key.
        """
        signature = self.get_func_signature(func_name)
        if not signature:
            return {"parameters": {}}
        signature_txt = "\n".join(
            f"{i}. {name}: {type_}"
            for i, (name, type_) in enumerate(signature.items(), start=1)
        )

        base_prompt = f"""Extract function arguments from the request.

Function: {func_name}

Arguments:
{signature_txt}

Rules:
- Copy values directly from the request.
- Do not calculate or infer values.
- Do not invent values.
- If a value is not provided, use null.
- Return only valid JSON.
- Use the argument names as JSON keys.
- finish with '"' for string parameters.

Request:
"{prompt.prompt}"

JSON:
"""
        buffer = "{\n"
        result = {}
        params_items = list(signature.items())
        for index, (param_name, param_info) in enumerate(params_items):
            parameter_type = self.get_param_type(param_info)

            if parameter_type == "string":
                prefix = f'    "{param_name}": "'
            else:
                prefix = f'    "{param_name}": '

            buffer += prefix
            current_prompt = base_prompt + buffer
            value = self.get_arg_value(
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

        return {"parameters": result}

    def generate_func_call(
        self, prompt: Prompt, func_name_tokens: list[list[int]]
    ) -> FunctionCallResult:
        """
        Generate the function call class.

        Args:
            prompt (Prompt): The initial prompt.
            func_name_tokens (Any): The list of valid token for the func_name.
        Returns:
            FunctionCallResult: The function call class.
        """
        result = {"prompt": prompt.prompt}
        result.update(self.generate_func_name(prompt, func_name_tokens))
        result.update(self.generate_func_args(prompt, result["name"]))
        return FunctionCallResult.model_validate(result)

    def get_arg_value(self, prompt: str, param_name: str, p_type: str) -> Any:
        """
        Generate a value of a parameters based on the prompt and type.

        Args:
            prompt (str): The initial prompt to give to the llm.
            param_name (str): The name of the parameter to generate.
            p_type (str): The type of the parameter.
        Returns:
            Any: The value gaved by the llm.
        """
        input_ids = self._tokenizer.encode(prompt)
        if p_type == "number":
            return self._argument_generator._get_number_value(input_ids)
        elif p_type == "integer":
            return self._argument_generator._get_integer_value(input_ids)
        elif p_type == "boolean":
            return self._argument_generator._get_bool_value(input_ids)
        return self._argument_generator._get_string_value(input_ids)

    def get_func_signature(self, func_name: str) -> dict[str, Any]:
        """
        Generate the function signature based on function name.

        Args:
            func_name (str): The name of the function.
        Returns:
            dict: The dictionnary that contains the parameters with it's type.
        """
        for func in self._func_defs:
            if func_name == func.name:
                value = {
                    k: "".join(str(x) for x in v.model_dump().values() if x)
                    for k, v in func.parameters.items()
                }
                return value
        return {}

    def get_param_type(self, p_type: str) -> str:
        """
        Generate the type of parameters to match only the allowed one.

        Args:
            p_type (str): A type of parameters, preferably 'number', 'integer'
            'boolean', or 'string'.
        Returns:
            str: The allowed type.
        """
        tmp_prompt = f"""Choose the best name that match the string.

list of name: {self._valid_type}
String: {p_type}
Best match: """
        func_tokens = []
        for base_type in self._valid_type:
            func_tokens += self._tokenizer.get_token(base_type)
        decoded_name = self._tokenizer.generate_from_tokens(
            tmp_prompt, func_tokens
        )
        return decoded_name

    def run(self) -> Gen[FunctionCallResult, None, list[FunctionCallResult]]:
        """
        Run the generation of the function call.

        Returns:
            list: The list of function call class.
        """
        result: list[FunctionCallResult] = []
        func_tokens = []
        for func in self._func_defs:
            func_tokens += self._tokenizer.get_token(func.name)
        for prompt in self._prompts:
            func_call = self.generate_func_call(prompt, func_tokens)
            yield func_call
            result.append(func_call)
        return result
