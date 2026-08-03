# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    my_llm.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 14:08:13 by nyramana         #+#    #+#              #
#    Updated: 2026/08/03 14:54:15 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from typing import Any, Generator

from llm_sdk import Small_LLM_Model

from .parser import Parser
from .model import FunctionDefinition


class My_LLM:
    def __init__(self) -> None:
        self.model = Small_LLM_Model()
        self.parser = Parser()

        self.prompts = self.parser.load_prompts()
        self.func_defs: list[FunctionDefinition] = self.parser.load_function_definitions()

        self.func_desc: list[tuple[str, str]] = [(a.name, a.description) for a in self.func_defs]
        print(self.func_desc)

    def get_func_name(self, prompt: str, func_name_token: list[Any]) -> None:
        new_prompt = f"""
        Here is a list of function and it's definition:

        {str(self.func_desc)}

        Which function name to use for the following prompt:

        Example:
        P: What is the sum of 2 and 3
        A: add_numbers

        P: {prompt}
        A: 
        """
        func_name = []
        next_token = self.get_next_tokens(new_prompt)
        i = 0
        print(f"THE PROMPT IS: {prompt}")
        for token in next_token:
            if token in [a[0][i] for a in func_name_token]:
                print(f"Token {token} added")
                func_name.append(token)
                print(self.model.decode(func_name))
                break

    def get_func_args(self) -> None:
        ...

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
