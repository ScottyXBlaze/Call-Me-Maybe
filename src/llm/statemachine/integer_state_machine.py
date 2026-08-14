# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    integer_state_machine.py                          :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/14 20:25:23 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 00:02:05 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from enum import Enum, auto


class State(Enum):
    START = auto()
    SIGN = auto()
    INTEGER = auto()
    END = auto()


class IntegerStateMachine:
    def __init__(self):
        self.state = State.START
        self.value = ""

    def can_accept(self, char: str) -> bool:
        if self.state == State.START:
            return (
                char.strip() in ("-", "+")
                or char.strip().isdigit()
            )

        if self.state == State.SIGN:
            return char.isdigit()

        if self.state == State.INTEGER:
            return char.isdigit() or char == "."

        return False

    def transition(self, char) -> bool:
        if not self.can_accept(char):
            return False

        self.value += char

        if self.state == State.START:
            self.state = State.SIGN if char == "-" else State.INTEGER

        elif self.state == State.SIGN:
            self.state = State.INTEGER

        return True

    def is_finished(self):
        return self.state == (State.INTEGER)

    def reset(self) -> None:
        self.state = State.START
        self.value = ""
