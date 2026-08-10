# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    my_llm.py                                         :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/04 22:58:41 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 16:45:21 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains de base LLm of the program."""

import json
import logging
from collections.abc import Generator
from typing import Any

from llm_sdk import Small_LLM_Model

from .model import FunctionCallResult, FunctionDefinition
from .parser import Parser

logger = logging.getLogger(__name__)

# Ensemble des tokens qui doivent stopper la génération d'une valeur string.
_STRING_STOP_CHARS = ('"', "\n")


class My_LLM:
    """
    Simple class that generates the function call by using the Small_LLM_Model.

    It uses the concept of constrained decoding.
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
        new_prompt = f"""
Choose the exact function name from the list that best answers the prompt.

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

    def get_best_allowed_token(
        self, prompt: str, allowed_tokens: set[int]
    ) -> int:
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
        Get the function signature as a JSON-serializable dictionary.

        Args:
            func_name (str): The name of the function.
        Returns:
            dict: The parameters of the function.
        """
        for func in self.func_defs:
            if func.name == func_name:
                value = {
                    k: "".join(str(x) for x in v.model_dump().values() if x)
                    for k, v in func.parameters.items()
                }
                return value
        return {}

    @staticmethod
    def _classify_type(p_type: str) -> str:
        """
        Classify a raw type string into 'number', 'boolean' or 'string'.

        Args:
            p_type (str): The raw type description from the function signature.
        Returns:
            str: One of 'number', 'boolean', 'string'.
        """
        p_type_lower = p_type.lower()
        if "bool" in p_type_lower:
            return "boolean"
        if (
            "num" in p_type_lower
            or "int" in p_type_lower
            or "float" in p_type_lower
        ):
            return "number"
        return "string"

    def _get_number_value(self, input_ids: list[int]) -> float | int:
        """Constrained decoding for a numeric argument."""
        val_str = ""
        for _ in range(12):
            logits = self.model.get_logits_from_input_ids(input_ids)
            sorted_tokens = sorted(
                range(len(logits)), key=lambda k: logits[k], reverse=True
            )

            best_token = None
            for token_id in sorted_tokens[:150]:
                decoded = self.model.decode([token_id])
                if decoded and (
                    all(c in "0123456789.-" for c in decoded)
                    or decoded in [",", "\n", " ", "}", '"']
                ):
                    best_token = token_id
                    break

            if best_token is None:
                break

            decoded_str = self.model.decode([best_token])
            if decoded_str in [",", "\n", " ", "}", '"']:
                break

            val_str += decoded_str
            input_ids.append(best_token)

        clean_val = val_str.strip()
        if not clean_val:
            logger.warning(
                "Numeric extraction returned an empty value; "
                "defaulting to 0 and flagging for review."
            )
            return 0

        try:
            return float(clean_val) if "." in clean_val else int(clean_val)
        except ValueError:
            logger.warning(
                "Could not parse %r as a number; defaulting to 0.", clean_val
            )
            return 0

    def _get_boolean_value(self, input_ids: list[int]) -> bool:
        """
        Constrained decoding for a boolean argument.

        Only allows tokens that are a strict prefix of 'true' or 'false',
        exactly like the function-name selection does.
        """
        candidates = ["true", "false"]
        chosen = ""

        while True:
            remaining = [c for c in candidates if c.startswith(chosen)]
            if len(remaining) <= 1 or chosen in candidates:
                break

            logits = self.model.get_logits_from_input_ids(input_ids)
            sorted_tokens = sorted(
                range(len(logits)), key=lambda k: logits[k], reverse=True
            )

            best_token = None
            for token_id in sorted_tokens[:150]:
                decoded = self.model.decode([token_id]).lower()
                if decoded and any(
                    c.startswith(chosen + decoded) for c in remaining
                ):
                    best_token = token_id
                    break

            if best_token is None:
                break

            decoded_str = self.model.decode([best_token]).lower()
            chosen += decoded_str
            input_ids.append(best_token)

        if chosen not in candidates:
            logger.warning(
                "Boolean extraction produced %r, defaulting to False.", chosen
            )
            return False

        return chosen == "true"

    def _get_string_value(self, input_ids: list[int]) -> str:
        """
        Constrained decoding for a string argument.

        Stops as soon as a token contains a closing quote or newline,
        instead of running unconstrained until an arbitrary token limit.
        """
        val_str = ""
        for _ in range(40):
            logits = self.model.get_logits_from_input_ids(input_ids)
            sorted_tokens = sorted(
                range(len(logits)), key=lambda k: logits[k], reverse=True
            )

            best_token = None
            decoded = ""
            for token_id in sorted_tokens[:150]:
                decoded = self.model.decode([token_id])
                if decoded:
                    best_token = token_id
                    break

            if best_token is None:
                break

            if any(stop in decoded for stop in _STRING_STOP_CHARS):
                clean_part = decoded
                for stop in _STRING_STOP_CHARS:
                    clean_part = clean_part.split(stop)[0]
                val_str += clean_part
                break

            val_str += decoded
            input_ids.append(best_token)

        return val_str.strip()

    def get_single_arg_value(
        self, prompt_with_prefix: str, param_name: str, p_type: str
    ) -> Any:
        """
        Génère la valeur d'un paramètre via Constrained Decoding strict.

        Args:
            prompt_with_prefix (str): Le prompt déjà préfixé avec le début
                du buffer JSON (clé + éventuel guillemet ouvrant).
            param_name (str): Le nom du paramètre (pour le logging).
            p_type (str): Le type déclaré du paramètre.
        Returns:
            Any: La valeur extraite, typée selon p_type.
        """
        input_ids = self.model.encode(prompt_with_prefix).tolist()[0]
        kind = self._classify_type(p_type)

        if kind == "number":
            return self._get_number_value(input_ids)
        if kind == "boolean":
            return self._get_boolean_value(input_ids)
        return self._get_string_value(input_ids)

    def get_func_args(self, prompt: str, func_name: str) -> dict[str, Any]:
        """
        Get function.

        Args:
            self (Any): Description of self.
            prompt (str): Description of prompt.
            func_name (str): Description of func_name.
        Returns:
            dict: Description of return value.
        """
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
        json_buffer = "{\n"
        extracted_args = {}

        params_items = list(signature.items())
        for idx, (param_name, param_info) in enumerate(params_items):
            p_type = str(param_info)
            kind = self._classify_type(p_type)

            # Insérer la clé automatiquement dans la structure JSON.
            # Les strings ont un guillemet ouvrant, pas les nombres/booléens.
            if kind == "string":
                prefix = f'  "{param_name}": "'
            else:
                prefix = f'  "{param_name}": '

            json_buffer += prefix
            current_prompt = base_prompt + json_buffer

            val = self.get_single_arg_value(current_prompt, param_name, p_type)
            extracted_args[param_name] = val

            if kind == "string":
                json_buffer += f'{val}"'
            elif kind == "boolean":
                json_buffer += "true" if val else "false"
            else:
                json_buffer += str(val)

            if idx < len(params_items) - 1:
                json_buffer += ",\n"
            else:
                json_buffer += "\n"

        return {"parameters": extracted_args}

    def run(self) -> None:
        """Run the generation of the function call."""
        self.parser.check_args()
        total = []
        func_token = self.get_tokens([a.name for a in self.func_defs])
        for prompt in self.prompts:
            result = {"prompt": prompt}
            func_name = self.get_func_name(prompt, func_token)
            result.update(func_name)
            result.update(self.get_func_args(prompt, func_name["name"]))
            total.append(result)
            print(result)

        obj = json.dumps(total, indent=4)
        print(obj)
        self.parser.save_function_calls(
            [FunctionCallResult.model_validate(single) for single in total]
        )
