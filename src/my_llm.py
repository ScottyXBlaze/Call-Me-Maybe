# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    my_llm.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 14:08:13 by nyramana         #+#    #+#              #
#    Updated: 2026/08/03 15:55:51 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

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

        self.func_desc: list[tuple[str, str]] = [
            (a.name, a.description) for a in self.func_defs
        ]
        print(self.func_desc)

    def get_func_name(self, prompt: str, func_name_token: list[Any]) -> None:
        new_prompt = f"""
        Here is a list of function and it's definition:

        {str(self.func_desc)}

        Which function name of the above is valid for the following prompts:
        Example:
        the prompt is: What is the sum of 9 and 1?
        The function name: fn_add_numbers

        The prompt is: {prompt}
        The function name: """
        func_name = []
        i = 0
        func_name_token = [func[0] for func in func_name_token]
        while True:
            next_token = self.get_next_tokens(new_prompt)
            probability = [a[i] for a in func_name_token if len(a) > i]
            for token in next_token:
                try:
                    if token in probability:
                        func_name.append(token)
                        new_prompt += self.model.decode([token])
                        i += 1
                        break
                except IndexError:
                    pass
            if func_name in func_name_token:
                break
        print(f"{new_prompt}")

    def get_func_args(self) -> None: ...

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

    def run(self) -> None:
        self.parser.check_args()
        func_token = self.get_tokens([a.name for a in self.func_defs])
        for prompt in self.prompts:
            self.get_func_name(prompt, func_token)
