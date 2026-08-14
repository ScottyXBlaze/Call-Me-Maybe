# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    string_state_machine.py                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/15 00:33:18 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 00:57:06 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

from enum import Enum, auto


class State(Enum):
    START = auto()
    STRING = auto()
    ESCAPE = auto()
    END = auto()


class StringStateMachine:
    def __init__(self):
        self.state = State.START
        self.value = ""

    def _next_state(self, state, char):
        if state == State.START:
            if char == '"':
                return State.STRING
            return None

        if state == State.STRING:
            if char == '"':
                return State.END

            if char == "\\":
                return State.ESCAPE

            return State.STRING

        if state == State.ESCAPE:
            if char in '"\\/bfnrt':
                return State.STRING

            return None

        if state == State.END:
            return None

    def can_accept(self, token: str) -> bool:
        state = self.state

        for char in token:
            state = self._next_state(state, char)

            if state == State.END:
                return True
            if state is None:
                return False

        return True

    def transition(self, token: str):
        for char in token:
            if self.state == State.START:
                self.state = State.STRING

            elif self.state == State.STRING:
                if char == '"':
                    self.state = State.END
                    return
                elif char == "\\":
                    self.state = State.ESCAPE
                else:
                    self.value += char

            elif self.state == State.ESCAPE:
                self.value += char
                self.state = State.STRING

    def is_finished(self):
        return self.state == State.END
