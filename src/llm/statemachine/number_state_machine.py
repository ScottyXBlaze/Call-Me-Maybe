# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    number_state_machine.py                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/14 20:25:23 by nyramana         #+#    #+#              #
#    Updated: 2026/08/14 20:45:41 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from enum import Enum, auto


class State(Enum):
    START = auto()
    SIGN = auto()
    INTEGER = auto()
    DOT = auto()
    DECIMAL = auto()
    END = auto()


class NumberStateMachine:
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

        if self.state == State.DOT:
            return char.isdigit()

        if self.state == State.DECIMAL:
            return char.isdigit()

        return False

    def transition(self, char) -> bool:
        if not self.can_accept(char):
            return False

        self.value += char

        if self.state == State.START:
            self.state = State.SIGN if char == "-" else State.INTEGER

        elif self.state == State.SIGN:
            self.state = State.INTEGER

        elif self.state == State.INTEGER and char == ".":
            self.state = State.DOT

        elif self.state == State.DOT:
            self.state = State.DECIMAL

        return True

    def is_finished(self):
        return self.state in (State.INTEGER, State.DECIMAL)

    def reset(self) -> None:
        self.state = State.START
        self.value = ""
