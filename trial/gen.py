# l = list(range(1000000000000000000000000000000000000000000000000))

# for i in l:
#     print(i)

# for i in range(1000000000000000000000000000000000000000000000000):
#     print(i)

# Generator function
"""
    it should have a loop (for or while)
    it should have yield statement
    it can have a if condition
"""


def generate_my_name():
    name = 'swadhikar c'
    for char in name:
        if char != ' ':  # yield only non-space char
            yield char


# for c in generate_my_name():
#     print(c)

from builtins import *

for type in dir():
    print(type)
