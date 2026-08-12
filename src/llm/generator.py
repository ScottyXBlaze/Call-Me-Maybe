# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    generator.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/11 15:48:28 by nyramana         #+#    #+#              #
#    Updated: 2026/08/12 08:16:44 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


from .tokenizer import Tokenizer


class ArgumentGenerator:
    def __init__(self, tokenizer: Tokenizer) -> None:
        self._tokenizer = tokenizer
        self._valid_type = self._tokenizer.get_tokens(["boolean", "string", "number"])

    def _get_number_value(self, input_ids: list[int]) -> float:
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
            return float(clean_val) if "." in clean_val else int(clean_val)
        except ValueError:
            return 0

    def _get_bool_value(self, input_ids: list[int]) -> bool:
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

            logits = self._tokenizer.get_logits_from_input_ids(input_ids)
            sorted_tokens = sorted(
                range(len(logits)), key=lambda k: logits[k], reverse=True
            )

            best_token = None
            for token_id in sorted_tokens[:150]:
                decoded = self._tokenizer.decode([token_id]).lower()
                if decoded and any(
                    c.startswith(chosen + decoded) for c in remaining
                ):
                    best_token = token_id
                    break

            if best_token is None:
                break

            decoded_str = self._tokenizer.decode([best_token]).lower()
            chosen += decoded_str
            input_ids.append(best_token)

        if chosen not in candidates:
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

    def generate_from_tokens(self, prompt: str, allowed_tokens: list[list[int]]) -> str:
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
            best_token = self._tokenizer.get_best_token(prompt, allowed_token)
            result.append(best_token)
            prompt += self._tokenizer.decode([best_token])
            i += 1
            if result in allowed_tokens:
                break

        return self._tokenizer.decode(result).strip()
