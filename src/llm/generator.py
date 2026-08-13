# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    generator.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/11 15:48:28 by nyramana         #+#    #+#              #
#    Updated: 2026/08/13 16:17:01 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contain a generator class for the constrained decoding."""

from typing import Any

from .tokenizer import Tokenizer


class Generator:
    """Generator class that helps with constrained decoding."""

    def __init__(self, tokenizer: Tokenizer) -> None:
        """
        Contain helper method to generate valid data from the llm.

        Args:
            tokenizer (Tokenizer): The tokenizer class.
        """
        self._tokenizer = tokenizer
        self._valid_type = self._tokenizer.get_tokens(
            ["boolean", "string", "number", "integer"]
        )

    def _get_integer_value(self, input_ids: list[int]) -> int:
        """
        Get an integer value from the llm based on input_ids.

        Args:
            input_ids (list[int]): The list of tokens / input_ids.
        Returns:
            int: The value gaved by the llm.
        """
        val_str = ""
        for _ in range(12):
            logits = self._tokenizer.get_logits_from_input_ids(input_ids)
            sorted_tokens = sorted(
                range(len(logits)), key=lambda k: logits[k], reverse=True
            )

            best_token = None
            for token_id in sorted_tokens[:150]:
                decoded = self._tokenizer.decode([token_id])
                if decoded and (
                    all(c in "0123456789-" for c in decoded)
                    or decoded in [",", "\n", " ", "}", '"']
                ):
                    best_token = token_id
                    break

            if best_token is None:
                break

            decoded_str = self._tokenizer.decode([best_token])
            if decoded_str in [",", "\n", " ", "}", '"']:
                break

            val_str += decoded_str
            input_ids.append(best_token)

        clean_val = val_str.strip()
        if not clean_val:
            return 0

        try:
            return int(clean_val)
        except ValueError:
            return 0

    def _get_number_value(self, input_ids: list[int]) -> float:
        """
        Get a float or double value from the llm based on input_ids.

        Args:
            input_ids (list[int]): The list of tokens / input_ids.
        Returns:
            float: The value gaved by the llm.
        """
        val_str = ""
        for _ in range(12):
            logits = self._tokenizer.get_logits_from_input_ids(input_ids)
            sorted_tokens = sorted(
                range(len(logits)), key=lambda k: logits[k], reverse=True
            )

            best_token = None
            for token_id in sorted_tokens[:150]:
                decoded = self._tokenizer.decode([token_id])
                if decoded and (
                    all(c in "0123456789.-" for c in decoded)
                    or decoded in [",", "\n", " ", "}", '"']
                ):
                    best_token = token_id
                    break

            if best_token is None:
                break

            decoded_str = self._tokenizer.decode([best_token])
            if decoded_str in [",", "\n", " ", "}", '"']:
                break

            val_str += decoded_str
            input_ids.append(best_token)

        clean_val = val_str.strip()
        if not clean_val:
            return 0

        try:
            return float(clean_val)
        except ValueError:
            return 0

    def _get_bool_value(self, input_ids: list[int]) -> bool:
        """
        Get a boolean value from the llm based on input_ids.

        Args:
            input_ids (list[int]): The list of tokens / input_ids.
        Returns:
            bool: The value gaved by the llm.
        """
        candidates = ["true", "false"]

        return (
            self._tokenizer.generate_from_tokens(
                self._tokenizer.decode(input_ids),
                self._tokenizer.get_tokens(candidates),
            )
            == "true"
        )

    def _get_string_value(self, input_ids: list[int]) -> str:
        """
        Get a string value from the llm based on input_ids.

        Args:
            input_ids (list[int]): The list of tokens / input_ids.
        Returns:
            str: The value gaved by the llm.
        """
        val_str = ""
        for _ in range(40):
            logits = self._tokenizer.get_logits_from_input_ids(input_ids)
            sorted_tokens = sorted(
                range(len(logits)), key=lambda k: logits[k], reverse=True
            )

            best_token = None
            decoded = ""
            for token_id in sorted_tokens[:150]:
                decoded = self._tokenizer.decode([token_id])
                if decoded:
                    best_token = token_id
                    break

            if best_token is None:
                break

            if any(stop in decoded for stop in ['"', "\n"]):
                clean_part = decoded
                for stop in ['"', "\n"]:
                    clean_part = clean_part.split(stop)[0]
                val_str += clean_part
                break

            val_str += decoded
            input_ids.append(best_token)

        return val_str.strip()

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
            return self._get_number_value(input_ids)
        elif p_type == "integer":
            return self._get_integer_value(input_ids)
        elif p_type == "boolean":
            return self._get_bool_value(input_ids)
        return self._get_string_value(input_ids)
