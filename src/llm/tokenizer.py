# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    tokenizer.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 15:56:35 by nyramana         #+#    #+#              #
#    Updated: 2026/08/13 15:10:06 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from llm_sdk import Small_LLM_Model


class Tokenizer:
    def __init__(self) -> None:
        self._model = Small_LLM_Model()

    def get_tokens(self, strings: list[str]) -> list[list[int]]:
        result = []
        for string in strings:
            result += self.get_token(string)
        return result

    def get_token(self, string: str) -> list[list[int]]:
        """
        Get the token version of the name of the function.

        Args:
            func_names (list[str]): The name of the function.
        Returns:
            list: List of the token.
        """
        result = []
        tokens_raw = self._model.encode(string).tolist()[0]
        result.append(tokens_raw)

        tokens_spaced = self._model.encode(f" {string}").tolist()[0]
        if tokens_spaced != tokens_raw:
            result.append(tokens_spaced)

        return result

    def get_best_token(self, string: str, allowed_tokens: set[int]) -> int:
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
                best_token = self.get_best_token(prompt, allowed_token)
            else:
                best_token = allowed_token.pop()
            result.append(best_token)
            prompt += self.decode([best_token])
            i += 1
            if result in allowed_tokens:
                break
        return self.decode(result).strip()

    def decode(self, tokens: list[int]) -> str:
        return self._model.decode(tokens)

    def encode(self, string: str) -> list[int]:
        return self._model.encode(string).tolist()[0]

    def get_logits_from_input_ids(self, tokens: list[int]) -> list[float]:
        return self._model.get_logits_from_input_ids(tokens)

# fn_add_numbers -> 1000, 1881, 31847, 1987
# fn_greet -> 1000, 3174, 13498
# fn_mult -> 1000, 13483, 19348
# [1000, 3174, 13498]
