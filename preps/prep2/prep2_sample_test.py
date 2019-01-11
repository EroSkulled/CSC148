"""Prep 2 Synthesize Sample Tests

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains sample tests for Prep 2.

WARNING: THIS IS AN EXTREMELY INCOMPLETE SET OF TESTS!
We will test your code on a much more thorough set of tests.  You should
write your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<https://www.teach.cs.toronto.edu/~csc148h/winter/notes/testing/hypothesis.html>

Note: this file is for support purposes only, and is not part of your
submission.
"""
from hypothesis import given
from hypothesis.strategies import integers
from prep2 import Spinner


# This is a hypothesis test; it generates a random integer to use as input,
# so that we don't need to hard-code a specific number of slots in the test.
@given(slots=integers(min_value=1))
def test_new_spinner_position(slots: int) -> None:
    """Test that the position of a new spinner is always 0."""
    spinner = Spinner(slots)
    assert spinner.position == 0


def test_doctest() -> None:
    """Test the given doctest in the Spinner class docstring."""
    spinner = Spinner(8)

    spinner.spin(4)
    assert spinner.position == 4

    spinner.spin(2)
    assert spinner.position == 6

    spinner.spin(2)
    assert spinner.position == 0


def test_random() -> None:
    spinner = Spinner(8)

    spinner.spin_randomly()
    assert 0 <= spinner.position <= spinner.slots

    spinner.spin_randomly()
    assert 0 <= spinner.position <= spinner.slots

    spinner.spin_randomly()
    assert 0 <= spinner.position <= spinner.slots


if __name__ == '__main__':
    import pytest
    pytest.main(['prep2_sample_test.py'])
