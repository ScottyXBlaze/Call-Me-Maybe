# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    tokenizer.py                                      :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 15:56:35 by nyramana         #+#    #+#              #
#    Updated: 2026/08/11 10:42:01 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


class Tokenizer:
    def __init__(self) -> None: ...

    def get_token(self, string: str) -> list[int]: ...

    def get_best_token(self, string: str, allowed_tokens: set[int]) -> int: ...
