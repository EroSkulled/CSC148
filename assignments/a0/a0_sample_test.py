"""CSC148 Assignment 0: Sample tests

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 0.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Diane Horton, Jacqueline Smith, and Bogdan Simion

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Diane Horton, Jacqueline Smith, and Bogdan Simion
"""
from datetime import date
from io import StringIO
from elections import Election, Jurisdiction

# Contents of a file with one result
# We will use it with StringIO to test file reading methods.
# StringIO allows us to pass an open file within a Python module.
# You can use it in your own testing, but you do not have to.
SHORT_FILE_CONTENTS = 'header\n' + \
                      ','.join(['35090', '"St. Paul\'s"', '"St. Paul\'s"',
                                '" 1"', '"Toronto"', 'N', 'N', '""', '1',
                                '367', '"Bennett"', '""', '"Carolyn"',
                                '"Liberal"', '"Liberal"', 'Y', 'Y', '113'])


def simple_election_setup() -> Election:
    """Set up a simple Election with two ridings and three parties"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 1234)
    e.update_results('r1', 'lib', 1345)
    e.update_results('r1', 'pc', 1456)
    e.update_results('r2', 'ndp', 300)
    e.update_results('r2', 'lib', 200)
    e.update_results('r2', 'pc', 100)

    return e


def simple_jurisdiction_setup() -> Jurisdiction:
    """Set up a simple Jurisdiction with a single Election and one result."""
    j = Jurisdiction('Canada')
    res1 = StringIO(SHORT_FILE_CONTENTS)
    j.read_results(2000, 1, 2, res1)
    return j


def test_simple_election_ridings_of() -> None:
    """Test Election.ridings_of with a simple Election."""
    e = simple_election_setup()
    assert e.ridings_of() == ['r1', 'r2']


def test_simple_election_results_for() -> None:
    """Test Election.results_for with a simple Election."""
    e = simple_election_setup()
    assert e.results_for('r1', 'ndp') == 1234


def test_simple_election_riding_winners() -> None:
    """Test Election.riding_winners with a simple Election."""
    e = simple_election_setup()
    assert e.riding_winners('r1') == ['pc']


def test_simple_election_riding_winners_tie() -> None:
    """Test Election.riding_winners with a tie Election."""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 1)
    e.update_results('r1', 'lib', 1)
    e.update_results('r1', 'pc', 1)
    assert e.riding_winners('r1') == ['ndp', 'lib', 'pc']


def test_simple_election_popular_vote() -> None:
    """Test Election.popular_vote with a simple Election."""
    e = simple_election_setup()
    assert e.popular_vote() == {'ndp': 1534, 'lib': 1545, 'pc': 1556}


def test_complex_election_popular_vote() -> None:
    """Test Election.popular_vote with a simple Election."""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 1)
    e.update_results('r1', 'lib', 1)
    e.update_results('r1', 'pc', 0)
    e.update_results('r2', 'ndp', 3)
    e.update_results('r2', 'lib', 2)
    e.update_results('r2', 'pc', 0)
    e.update_results('r2', 'green', 1)
    assert e.popular_vote() == {'ndp': 4, 'lib': 3, 'green': 1}


def test_read_short_data() -> None:
    """Test read_results method with short_data"""
    fo = open('data/short_data.csv', "r")
    e = Election(date(2000, 2, 8))
    e.read_results(fo)


def test_simple_election_party_seats() -> None:
    """Test Election.party_seats with a simple Election."""
    e = simple_election_setup()
    assert e.party_seats() == {'ndp': 1, 'lib': 0, 'pc': 1}


def test_one_party_one_riding_read_results() -> None:
    """Test Election.read_results with a file with a single line."""
    file = StringIO(SHORT_FILE_CONTENTS)
    e = Election(date(2012, 10, 30))
    e.read_results(file)
    assert e.popular_vote() == {'Liberal': 113}


def test_simple_election_win() -> None:
    e = simple_election_setup()
    assert e.election_winners() == ['ndp', 'pc']


def test_simple_election_win_single_party() -> None:
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 100)
    e.update_results('r2', 'ndp', 100)
    assert e.election_winners() == ['ndp']


def test_simple_election_win_tie() -> None:
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 1)
    e.update_results('r1', 'lib', 1)
    e.update_results('r1', 'pc', 1)
    e.update_results('r2', 'ndp', 1)
    e.update_results('r2', 'lib', 1)
    assert e.election_winners() == ['ndp', 'lib', 'pc']


def test_simple_jurisdiction_party_wins() -> None:
    """Test Jurisdiction.party_wins with a file with a single line. """
    j = simple_jurisdiction_setup()
    assert j.party_wins('Liberal') == [date(2000, 1, 2)]


# def test_simple_jurisdiction_party_history() -> None:
#     """Test Jurisdiction.party_history with a file with a single line."""
#     j = simple_jurisdiction_setup()
#     assert j.party_history('Liberal') == {date(2000, 1, 2): 1.0}
#
#
# def test_simple_jurisdiction_riding_changes() -> None:
#     """Test Jurisdiction.riding_changes with two Elections."""
#     j = simple_jurisdiction_setup()
#     res2 = open('sample_data/toronto-stpauls.csv')
#     j.read_results(2004, 5, 15, res2)
#     res2.close()
#     assert j.riding_changes() == [({"St. Paul's"}, {"Toronto--St. Paul's"})]


if __name__ == '__main__':
    import pytest
    pytest.main(['a0_sample_test.py'])
