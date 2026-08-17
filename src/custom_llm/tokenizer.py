# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    tokenizer.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 15:56:35 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 14:14:04 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the tokenizer class."""

from typing import Any

from llm_sdk import Small_LLM_Model


class Tokenizer:
    """Contain the basics of tokenization and detokenization."""

    def __init__(self, model: str) -> None:
        """Everything starts here."""
        self._model = Small_LLM_Model(model)

    def get_tokens(self, strings: list[str]) -> list[list[int]]:
        """
        Get the list of allowed tokens based on a list of strings.

        Args:
            strings (list[str]): The list of string to be allowed.
        Returns:
            list: List of the allowed tokens.
        """
        result = []
        for string in strings:
            result += self.get_token(string)
        return result

    def get_token(self, string: str) -> list[list[int]]:
        """
        Get the token version of a string.

        It also check the string with a space before to be more accurate.
        Args:
            string (str): The string to transfom.
        Returns:
            list: The list of possible token.
        """
        result = []
        tokens_raw = self._model.encode(string).tolist()[0]
        result.append(tokens_raw)

        tokens_spaced = self._model.encode(f" {string}").tolist()[0]
        if tokens_spaced != tokens_raw:
            result.append(tokens_spaced)

        return result

    def _get_best_token(self, string: str, allowed_tokens: set[int]) -> int:
        """
        Get the best token based on the allowed tokens.

        Args:
            string (str): The initial string / prompt.
            allowed_tokens (set[int]): The set of allowed token.
        Returns:
            int: The most probable token.
        """
        input_ids = self._model.encode(string).tolist()[0]
        logits = self._model.get_logits_from_input_ids(input_ids)

        best_token = -1
        best_score = float("-inf")

        for token_id in allowed_tokens:
            if logits[token_id] > best_score:
                best_score = logits[token_id]
                best_token = token_id

        return best_token

    def generate_from_tokens(
        self, prompt: str, allowed_tokens: list[list[int]]
    ) -> str:
        """
        Generate tokens amoung the list of allowed token.

        It use a tricky way of constrained decoding where instead of
        setting every forbiden token, we only check the probabily with
        the allowed token.
        Args:
            prompt (str): The initial prompt.
            allowed_tokens (list[list[int]]): The list of allowed_token.
        Returns:
            str: The decoded value from one of the allowed token.
        """
        result: list[int] = []
        i = 0
        while True:
            candidates = [
                seq
                for seq in allowed_tokens
                if len(seq) > i and seq[:i] == result
            ]
            if not candidates:
                break
            allowed_token = {seq[i] for seq in candidates}
            if len(allowed_token) > 1:
                best_token = self._get_best_token(prompt, allowed_token)
            else:
                best_token = allowed_token.pop()
            result.append(best_token)
            prompt += self.decode([best_token])
            i += 1
            if result in allowed_tokens:
                break
        return self.decode(result).strip()

    def decode(self, tokens: list[int]) -> str:
        """
        Decode a token and return the string.

        Args:
            tokens (list[int]): The token.
        Returns:
            str: The string gaved by the model.
        """
        return self._model.decode(tokens)

    def encode(self, string: str) -> Any:
        """
        Encode a string and return the token.

        Args:
            string (str): The string.
        Returns:
            str: The list of token.
        """
        return self._model.encode(string).tolist()[0]

    def get_logits_from_input_ids(self, tokens: list[int]) -> list[float]:
        """
        Get the logits based on the tokens.

        Args:
            tokens (list[int]): The list of token.
        Returns:
            list: The list of probability.
        """
        return self._model.get_logits_from_input_ids(tokens)
