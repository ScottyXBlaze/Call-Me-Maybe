# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    test.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/10 14:34:19 by nyramana         #+#    #+#              #
#    Updated: 2026/08/10 14:34:19 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import pytest

def test_answer1():
  a = 5
  b = 10
  assert a==b
  
def test_answer2():
  c = 15
  d = 3*5
  assert c==d
