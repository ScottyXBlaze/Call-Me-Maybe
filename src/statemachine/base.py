# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    base.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/15 07:59:54 by nyramana         #+#    #+#              #
#    Updated: 2026/08/15 08:05:56 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

"""Module that contains the abstract class for the state machine."""

from abc import ABC, abstractmethod


class StateMachine(ABC):
    """Base state machine class model."""

    @abstractmethod
    def can_accept(self, char: str) -> bool:
        """
        Check if the state machine can accept the char.

        Args:
            char (str): The char to check.
        Returns:
            bool: True if so.
        """

    @abstractmethod
    def is_finished(self) -> bool:
        """
        Check if the value can be finished.

        Returns:
            bool: True if so.
        """

    @abstractmethod
    def transition(self, char: str) -> bool:
        """
        Change to one State to another.

        Args:
            char (Any): The char to check.
        Returns:
            bool: True if it was successfull.
        """
