class Spinner:
    slots: int
    position: int

    def __init__(self, size: int) -> None:
        slots = size
        position = 0


# s = Spinner(8)
# print(s.position)

'''
AttributeError: 'Spinner' object has no attribute 'position'

Must use self to go to the instance attribute
'''
print(__name__)
import doctest

doctest.testmod()

import python_ta

python_ta.check_all()