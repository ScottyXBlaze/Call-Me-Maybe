# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    my_llm.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 14:08:13 by nyramana         #+#    #+#              #
#    Updated: 2026/08/04 16:30:04 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import json
from typing import Any, Generator

from llm_sdk import Small_LLM_Model

from .model import FunctionDefinition
from .parser import Parser


class My_LLM:
    def __init__(self) -> None:
        self.model = Small_LLM_Model()
        self.parser = Parser()

        self.prompts = self.parser.load_prompts()
        self.func_defs: list[FunctionDefinition] = (
            self.parser.load_function_definitions()
        )

        self.func_desc = "\n".join(
            [f"{a.name}: {a.description}" for a in self.func_defs]
        )

    def get_func_name(
        self, prompt: str, func_name_token: list[Any]
    ) -> dict[str, str]:
        new_prompt = f"""Choose the exact function name from the list that best answers the prompt.

### Example 1
Functions:
calculate_sum: Adds two numbers
convert_to_upper: Converts text to uppercase

User prompt: What is 15 plus 10?
Function: calculate_sum

### Real Task
Functions:
{self.func_desc}

User prompt: {prompt}
Function:"""
        func_name = []
        i = 0
        func_name_token = [func[0] for func in func_name_token]
        while True:
            prob = [a[i] for a in func_name_token if len(a) > i]
            for token in self.get_next_tokens(new_prompt):
                if token in prob:
                    func_name.append(token)
                    new_prompt += self.model.decode([token])
                    i += 1
                    break
            if func_name in func_name_token:
                break
        return {"name": self.model.decode(func_name)}

    def get_func_args(self, prompt: str, func_name: str) -> dict[str, Any]:
        func_signature = self.get_func_signature(func_name)
        return func_signature

    def get_func_arg(self, prompt: str) -> None: ...

    def get_tokens(self, func_names: list[str]) -> list[Any]:
        result = []
        for name in func_names:
            result.append(self.model.encode(name).tolist())
        return result

    def get_next_tokens(self, prompt: str) -> Generator[int, None, None]:
        """
        Generate the next token and transform it into string.

        This is a generator so that you can Check the next string
        given by the token.
        Args:
            prompt (str): The prompt that the LLM should continue.
        Returns:
            Generator: The next token transformed into string.
        """
        token = self.model.encode(prompt).tolist()
        logits = self.model.get_logits_from_input_ids(token[0])
        while True:
            max_index = logits.index(max(logits))
            yield max_index
            logits[max_index] = float("-inf")

    def get_func_signature(self, func_name: str) -> dict[str, Any]:
        for func in self.func_defs:
            if func.name == func_name:
                return func.parameters
        return {}

    def run(self) -> None:
        self.parser.check_args()
        func_token = self.get_tokens([a.name for a in self.func_defs])
        for prompt in self.prompts:
            result = {"prompt": prompt}
            func_name = self.get_func_name(prompt, func_token)
            result.update(func_name)
            obj = json.dumps(result, indent=4)
            print(obj)
