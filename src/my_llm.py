# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    my_llm.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/03 14:08:13 by nyramana         #+#    #+#              #
#    Updated: 2026/08/04 19:57:35 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import json
from typing import Any, Generator

from llm_sdk import Small_LLM_Model

from .model import FunctionDefinition
from .parser import Parser


class My_LLM:
    """
    Simple class that generates the function call by using the Small_LLM_Model.

    It use the concept of constrained decoding.
    """

    def __init__(self) -> None:
        """Everything starts here."""
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
        self, prompt: str, func_name_token: list[list[int]]
    ) -> dict[str, str]:
        """
        Get the name of the function that matches the prompt.

        Args:
            prompt (str): The initial prompt/question.
            func_name_token (list[list[int]]): The token version
            of every function name.
        Returns:
            dict: The key, value of the function name.
        """
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
Function: """
        func_name: list[int] = []
        i = 0

        while True:
            candidates = [
                seq
                for seq in func_name_token
                if len(seq) > i and seq[:i] == func_name
            ]

            if not candidates:
                break

            allowed_tokens = {seq[i] for seq in candidates}

            token = self.get_best_allowed_token(new_prompt, allowed_tokens)

            func_name.append(token)
            new_prompt += self.model.decode([token])
            i += 1

            if func_name in func_name_token:
                break

        decoded_name = self.model.decode(func_name).strip()
        return {"name": decoded_name}

    def get_func_args(self, prompt: str, func_name: str) -> dict[str, Any]:
        """
        Get the function arguments.

        Args:
            prompt (str): The initial prompt/question.
            func_name (str): The name of the function.
        Returns:
            dict: The key, value of the parameters.
        """
        func_signature = self.get_func_signature(func_name)
        return func_signature

    def get_func_arg(self, prompt: str) -> None: ...

    def get_tokens(self, func_names: list[str]) -> list[list[int]]:
        """
        Get the token version of the name of the function.

        Args:
            func_names (list[str]): The name of the function.
        Returns:
            list: List of the token.
        """
        result = []
        for name in func_names:
            tokens_raw = self.model.encode(name).tolist()[0]
            result.append(tokens_raw)

            tokens_spaced = self.model.encode(f" {name}").tolist()[0]
            if tokens_spaced != tokens_raw:
                result.append(tokens_spaced)

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
        token = self.model.encode(prompt).tolist()[0]
        logits = self.model.get_logits_from_input_ids(token)
        while True:
            max_index = logits.index(max(logits))
            yield max_index
            logits[max_index] = float("-inf")

    def get_best_allowed_token( self, prompt: str, allowed_tokens: set[int]) -> int:
        """
        Get the best allowed tokens.

        Args:
            prompt (str): The prompt/question.
            allowed_tokens (set[int]): The allowed tokens.
        Returns:
            int: The best token.
        """
        input_ids = self.model.encode(prompt).tolist()[0]
        logits = self.model.get_logits_from_input_ids(input_ids)

        best_token = -1
        best_score = float("-inf")

        for token_id in allowed_tokens:
            if logits[token_id] > best_score:
                best_score = logits[token_id]
                best_token = token_id

        return best_token

    def get_func_signature(self, func_name: str) -> dict[str, Any]:
        """
        Get the function signature.

        Args:
            func_name (str): The name of the function.
        Returns:
            dict: The parameters of the function.
        """
        for func in self.func_defs:
            if func.name == func_name:
                return func.parameters
        return {}

    def run(self) -> None:
        """Run the generation of the function call."""
        self.parser.check_args()
        total = []
        func_token = self.get_tokens([a.name for a in self.func_defs])
        for prompt in self.prompts:
            result = {"prompt": prompt}
            func_name = self.get_func_name(prompt, func_token)
            result.update(func_name)
            total.append(result)
            print(result)
        obj = json.dumps(total, indent=4)
        print(obj)
