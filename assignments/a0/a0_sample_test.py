"""CSC148 Assignment 0: Sample tests
=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto
=== Module description ===
This module contains s`ample tests for Assignment 0.
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
    assert e.popular_vote() == {'ndp': 4, 'lib': 3, 'green': 1, 'pc': 0}


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


def test_simple_jurisdiction_party_history() -> None:
    """Test Jurisdiction.party_history with a file with a single line."""
    j = simple_jurisdiction_setup()
    assert j.party_history('Liberal') == {date(2000, 1, 2): 1.0}


def test_simple_jurisdiction_riding_changes() -> None:
    """Test Jurisdiction.riding_changes with two Elections."""
    j = simple_jurisdiction_setup()
    res2 = open('data/toronto-stpauls.csv')
    j.read_results(2004, 5, 15, res2)
    res2.close()
    res3 = open('data/labrador.csv')
    j.read_results(2004, 5, 15, res3)
    res3.close()
    res4 = open('data/nunavut.csv')
    j.read_results(2005, 5, 15, res4)
    res4.close()
    assert j.riding_changes() == \
        [({"St. Paul's"}, {"Toronto--St. Paul's", 'Labrador'}),
            ({"Toronto--St. Paul's", 'Labrador'}, {'Nunavut'})]


def test_complex_jurisdiction_riding_changes() -> None:
    """Test Jurisdiction.riding_changes with two Elections."""
    j = simple_jurisdiction_setup()
    res2 = open('data/toronto-stpauls.csv')
    j.read_results(2004, 5, 15, res2)
    res2.close()
    res3 = open('data/labrador.csv')
    j.read_results(2005, 5, 15, res3)
    res3.close()
    assert j.riding_changes() == [({"St. Paul's"}, {"Toronto--St. Paul's"}),
                                  ({"Toronto--St. Paul's"}, {'Labrador'})]


def test_riding_of_0_vote() -> None:
    """Test Election.riding_of with riding of 0 votes"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    res1 = e.ridings_of()
    assert res1 == ['r1']
    e.update_results('r2', 'ndp', 0)
    e.update_results('r1', 'ncp', 0)
    e.update_results('r2', 'nap', 0)
    res2 = e.ridings_of()
    assert res2 == ['r1', 'r2']


def test_riding_of_1_vote() -> None:
    """Test Election.riding_of with riding of 1 votes"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 1)
    res1 = e.ridings_of()
    assert res1 == ['r1']
    e.update_results('r2', 'ndp', 1)
    e.update_results('r1', 'ncp', 1)
    e.update_results('r2', 'nap', 1)
    res2 = e.ridings_of()
    assert res2 == ['r1', 'r2']


def test_riding_of_multiple_ridings() -> None:
    """Test Election.riding_of with multiple ridings"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 1)
    res1 = e.ridings_of()
    assert res1 == ['r1']
    e.update_results('r2', 'ndp', 10)
    e.update_results('r3', 'ncp', 51)
    e.update_results('r4', 'nap', 14)
    res2 = e.ridings_of()
    assert res2 == ['r1', 'r2', 'r3', 'r4']


def test_update_results_1_votes() -> None:
    """Test update_result for not existed and existed riding"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 1)
    res1 = e.results_for('r1', 'ndp')
    assert res1 == 1
    assert 'r1' in e._ridings and 'r1' in e._results
    assert 'ndp' in e._parties and 'ndp' in e._results['r1']
    e.update_results('r1', 'nap', 13)
    res2 = e.results_for('r1', 'nap')
    assert res2 == 13
    assert 'r1' in e._ridings and 'r1' in e._results
    assert 'nap' in e._parties and 'nap' in e._results['r1']


def test_update_results_0_votes() -> None:
    """Test update_result for not existed and existed riding"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    res1 = e.results_for('r1', 'ndp')
    assert res1 == 0
    assert 'r1' in e._ridings and 'r1' in e._results
    assert 'ndp' in e._parties and 'ndp' in e._results['r1']
    e.update_results('r1', 'nap', 0)
    res2 = e.results_for('r1', 'nap')
    assert res2 == 0
    assert 'r1' in e._ridings and 'r1' in e._results
    assert 'nap' in e._parties and 'nap' in e._results['r1']


def test_update_results_multiple_value() -> None:
    """Test update_result for not existed and existed riding"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    res1 = e.results_for('r1', 'ndp')
    assert res1 == 0
    assert 'r1' in e._ridings and 'r1' in e._results
    assert 'ndp' in e._parties and 'ndp' in e._results['r1']
    e.update_results('r2', 'nap', 12)
    res2 = e.results_for('r2', 'nap')
    assert res2 == 12
    assert 'r2' in e._ridings and 'r2' in e._results
    assert 'nap' in e._parties and 'nap' in e._results['r2']
    e.update_results('r2', 'nap', 32)
    res2 = e.results_for('r2', 'nap')
    assert res2 == 44
    assert 'r2' in e._ridings and 'r2' in e._results
    assert 'nap' in e._parties and 'nap' in e._results['r2']
    e.update_results('r1', 'nap', 2)
    res2 = e.results_for('r1', 'nap')
    assert res2 == 2
    assert 'r1' in e._ridings and 'r1' in e._results
    assert 'nap' in e._parties and 'nap' in e._results['r1']
    e.update_results('r1', 'ndp', 2)
    res2 = e.results_for('r1', 'ndp')
    assert res2 == 2
    assert 'r1' in e._ridings and 'r1' in e._results
    assert 'ndp' in e._parties and 'ndp' in e._results['r1']


def test_results_for_non_exist_riding_and_party() -> None:
    """Test results_for for riding and party that has no vote"""
    e = Election(date(2000, 2, 8))
    res1 = e.results_for('r1', 'pc')
    assert res1 is None


def test_results_for_non_exist_riding() -> None:
    """Test results_for for riding that has no vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 2)
    res1 = e.results_for('r2', 'ndp')
    assert res1 is None


def test_results_for_non_exist_party() -> None:
    """Test results_for for party that has no vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 2)
    res1 = e.results_for('r1', 'np')
    assert res1 is None


def test_results_for_party_in_two_ridings() -> None:
    """Test results_for for a party in two ridings"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 2)
    e.update_results('r2', 'ndp', 4)
    res1 = e.results_for('r1', 'ndp')
    res2 = e.results_for('r2', 'ndp')
    assert res1 == 2
    assert res2 == 4


def test_results_for_party_0_votes() -> None:
    """Test results_for for party that has 0 votes"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    res1 = e.results_for('r1', 'ndp')
    assert res1 == 0


def test_riding_winners_1_party_nonzero_vote() -> None:
    """Test riding_winner for one party that has more than one vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 45)
    res1 = e.riding_winners('r1')
    assert res1 == ['ndp']


def test_riding_winners_1_party_zero_vote() -> None:
    """Test riding_winner for one party that has 0 votes"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    res1 = e.riding_winners('r1')
    assert res1 == ['ndp']


def test_riding_winners_2_party_different_vote() -> None:
    """Test riding_winner for two party that has different vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 45)
    e.update_results('r1', 'np', 74)
    res1 = e.riding_winners('r1')
    assert res1 == ['np']


def test_riding_winners_2_party_same_vote() -> None:
    """Test riding_winner for two party that has same vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 45)
    e.update_results('r1', 'np', 45)
    res1 = e.riding_winners('r1')
    assert res1.sort() == ['np', 'ndp'].sort()


def test_riding_winners_multiple_party_same_vote() -> None:
    """Test riding_winner for multiple party that same vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 45)
    e.update_results('r1', 'np', 45)
    e.update_results('r1', 'ncp', 45)
    e.update_results('r1', 'nap', 45)
    res1 = e.riding_winners('r1')
    assert res1.sort() == ['np', 'ndp', 'ncp', 'nap'].sort()


def test_riding_winners_multiple_party_different_vote() -> None:
    """Test riding_winner for multiple party that has different vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 4)
    e.update_results('r1', 'np', 5)
    e.update_results('r1', 'ncp', 45)
    e.update_results('r1', 'nap', 59)
    res1 = e.riding_winners('r1')
    assert res1 == ['nap']


def test_riding_winners_multiple_party_same_vote_except_largest() -> None:
    """Test riding_winner for multiple party that same vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 45)
    e.update_results('r1', 'np', 45)
    e.update_results('r1', 'ncp', 45)
    e.update_results('r1', 'nap', 55)
    res1 = e.riding_winners('r1')
    assert res1 == ['nap']


def test_riding_winners_multiple_party_same_0_vote() -> None:
    """Test riding_winner for multiple party that same vote"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    e.update_results('r1', 'np', 0)
    e.update_results('r1', 'ncp', 0)
    e.update_results('r1', 'nap', 0)
    res1 = e.riding_winners('r1')
    assert res1.sort() == ['np', 'ndp', 'ncp', 'nap'].sort()


def test_popular_vote_1_riding_1_party() -> None:
    """Test popular_vote for 1 riding and 1 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    res1 = e.popular_vote()
    assert res1 == {'ndp': 19}


def test_popular_vote_1_riding_2_party() -> None:
    """Test popular_vote for 1 riding and 2 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r1', 'np', 69)
    res1 = e.popular_vote()
    assert res1 == {'ndp': 19, 'np': 69}


def test_popular_vote_2_riding_1_party() -> None:
    """Test popular_vote for 2 riding and 1 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r2', 'ndp', 69)
    res1 = e.popular_vote()
    assert res1 == {'ndp': 88}


def test_popular_vote_2_riding_2_party() -> None:
    """Test popular_vote for 2 riding and 2 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r2', 'np', 69)
    res1 = e.popular_vote()
    assert res1 == {'ndp': 19, 'np': 69}


def test_popular_vote_0_votes() -> None:
    """Test popular_vote for each party has 0 votes"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    e.update_results('r2', 'np', 0)
    res1 = e.popular_vote()
    assert res1 == {'ndp': 0, 'np': 0}


def test_party_seats_1_riding_1_party() -> None:
    """Test party_seats for 1 riding and 1 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    res1 = e.party_seats()
    assert res1 == {'ndp': 1}


def test_party_seats_1_riding_2_party() -> None:
    """Test party_seats for 1 riding and 2 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r1', 'np', 69)
    res1 = e.party_seats()
    assert res1 == {'ndp': 0, 'np': 1}


def test_party_seats_2_riding_1_party() -> None:
    """Test party_seats for 2 riding and 1 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r2', 'ndp', 69)
    res1 = e.party_seats()
    assert res1 == {'ndp': 2}


def test_party_seats_2_riding_2_party() -> None:
    """Test party_seats for 2 riding and 2 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r2', 'np', 69)
    res1 = e.party_seats()
    assert res1 == {'ndp': 1, 'np': 1}


def test_party_seats_0_votes() -> None:
    """Test party_seats for each party has 0 votes"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    e.update_results('r2', 'np', 1)
    res1 = e.party_seats()
    assert res1 == {'ndp': 0, 'np': 1}


def test_party_seats_1_riding_2_party_tie() -> None:
    """Test party_seats for two tied party in 1 riding"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 20)
    e.update_results('r1', 'np', 20)
    res1 = e.party_seats()
    assert res1 == {'ndp': 0, 'np': 0}


def test_election_winners_1_riding_1_party() -> None:
    """Test election_winners for 1 riding and 1 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 20)
    res1 = e.election_winners()
    assert res1 == ['ndp']


def test_election_winners_1_riding_2_party() -> None:
    """Test election_winners for 1 riding and 2 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r1', 'np', 69)
    res1 = e.election_winners()
    assert res1 == ['np']


def test_election_winners_2_riding_1_party() -> None:
    """Test election_winners for 2 riding and 1 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r2', 'ndp', 69)
    res1 = e.election_winners()
    assert res1 == ['ndp']


def test_election_winners_2_riding_2_party() -> None:
    """Test election_winners for 2 riding and 2 party"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 19)
    e.update_results('r2', 'np', 69)
    res1 = e.election_winners()
    assert res1.sort() == ['ndp', 'np'].sort()


def test_election_winners_0_votes() -> None:
    """Test election_winners for each party has 0 votes"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 0)
    e.update_results('r2', 'np', 0)
    res1 = e.election_winners()
    assert res1.sort() == ['ndp', 'np'].sort()


def test_election_winners_1_riding_2_party_tie() -> None:
    """Test election_winners for two tied party in 1 riding"""
    e = Election(date(2000, 2, 8))
    e.update_results('r1', 'ndp', 20)
    e.update_results('r1', 'np', 20)
    res1 = e.election_winners()
    assert res1.sort() == ['ndp', 'np'].sort()


def test_election_winners_empty() -> None:
    """Test election_winners for a election with no vote"""
    e = Election(date(2000, 2, 8))
    res1 = e.election_winners()
    assert res1.sort() == ['ndp', 'np'].sort()


def test_party_wins_1_election_won() -> None:
    """Test party_wins for 1 election and the party winning."""
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r1', 'lib', 2)
    e1.update_results('r1', 'pc', 3)
    e1.update_results('r2', 'lib', 10)
    e1.update_results('r2', 'pc', 20)
    e1.update_results('r3', 'ndp', 200)
    e1.update_results('r3', 'pc', 100)
    j = Jurisdiction('Canada')
    j._history[date(2000, 2, 8)] = e1
    res1 = j.party_wins('pc')
    assert res1 == [date(2000, 2, 8)]


def test_party_wins_1_election_lose() -> None:
    """Test party_wins for 1 election and the party losing."""
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r1', 'lib', 2)
    e1.update_results('r1', 'pc', 3)
    e1.update_results('r2', 'lib', 10)
    e1.update_results('r2', 'pc', 20)
    e1.update_results('r3', 'ndp', 200)
    e1.update_results('r3', 'pc', 100)
    j = Jurisdiction('Canada')
    j._history[date(2000, 2, 8)] = e1
    res1 = j.party_wins('lib')
    assert res1 == []


def test_party_wins_2_election_all_lose() -> None:
    """Test party_wins for 1 election and the party losing."""
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r1', 'lib', 2)
    e1.update_results('r1', 'pc', 3)
    e1.update_results('r2', 'lib', 10)
    e1.update_results('r2', 'pc', 20)
    e1.update_results('r3', 'ndp', 200)
    e1.update_results('r3', 'pc', 100)
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r1', 'ndp', 10)
    e2.update_results('r1', 'lib', 2)
    e2.update_results('r2', 'lib', 3)
    e2.update_results('r2', 'pc', 5)
    j = Jurisdiction('Canada')
    j._history[date(2000, 2, 8)] = e1
    j._history[date(2004, 5, 16)] = e2
    res1 = j.party_wins('lib')
    assert res1 == []


def test_party_wins_2_election_all_win() -> None:
    """Test party_wins for 1 election and the party losing."""
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 100)
    e1.update_results('r1', 'lib', 2)
    e1.update_results('r1', 'pc', 3)
    e1.update_results('r2', 'lib', 10)
    e1.update_results('r2', 'pc', 20)
    e1.update_results('r3', 'ndp', 200)
    e1.update_results('r3', 'pc', 100)
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r1', 'ndp', 10)
    e2.update_results('r1', 'lib', 2)
    e2.update_results('r2', 'lib', 3)
    e2.update_results('r2', 'ndp', 5)
    j = Jurisdiction('Canada')
    j._history[date(2000, 2, 8)] = e1
    j._history[date(2004, 5, 16)] = e2
    res1 = j.party_wins('ndp')
    assert res1 == [date(2000, 2, 8), date(2004, 5, 16)]


def test_party_wins_2_election_all_tie() -> None:
    """Test party_wins for 1 election and the party losing."""
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 10)
    e1.update_results('r1', 'lib', 100)
    e1.update_results('r1', 'pc', 100)
    e1.update_results('r2', 'lib', 10)
    e1.update_results('r2', 'pc', 20)
    e1.update_results('r3', 'ndp', 200)
    e1.update_results('r3', 'pc', 100)
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r1', 'ndp', 10)
    e2.update_results('r1', 'lib', 2)
    e2.update_results('r2', 'lib', 30)
    e2.update_results('r2', 'ndp', 5)
    j = Jurisdiction('Canada')
    j._history[date(2000, 2, 8)] = e1
    j._history[date(2004, 5, 16)] = e2
    res1 = j.party_wins('ndp')
    assert res1 == [date(2000, 2, 8), date(2004, 5, 16)]


def test_party_history_1_election_random_vote() -> None:
    """Test party_wins for 1 election and random vote."""
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 14)
    e1.update_results('r1', 'lib', 22)
    e1.update_results('r1', 'pc', 35)
    e1.update_results('r2', 'lib', 10)
    e1.update_results('r2', 'pc', 20)
    e1.update_results('r3', 'ndp', 199)
    e1.update_results('r3', 'pc', 100)
    j = Jurisdiction('Canada')
    j._history[date(2000, 2, 8)] = e1
    res1 = j.party_history('pc')
    assert res1 == {date(2000, 2, 8): 0.3875}


def test_party_history_1_election_zero_vote() -> None:
    """Test party_wins for 1 election and 0 vote."""
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 14)
    e1.update_results('r1', 'lib', 22)
    e1.update_results('r1', 'pc', 0)
    e1.update_results('r2', 'lib', 10)
    e1.update_results('r2', 'pc', 0)
    e1.update_results('r3', 'ndp', 199)
    e1.update_results('r3', 'pc', 0)
    j = Jurisdiction('Canada')
    j._history[date(2000, 2, 8)] = e1
    res1 = j.party_history('pc')
    assert res1 == {date(2000, 2, 8): 0.0}


def test_party_history_1_election_all_vote() -> None:
    """Test party_wins for 1 election and all vote."""
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 0)
    e1.update_results('r1', 'lib', 0)
    e1.update_results('r1', 'pc', 10)
    e1.update_results('r2', 'lib', 0)
    e1.update_results('r2', 'pc', 200)
    e1.update_results('r3', 'ndp', 0)
    e1.update_results('r3', 'pc', 50)
    j = Jurisdiction('Canada')
    j._history[date(2000, 2, 8)] = e1
    res1 = j.party_history('pc')
    assert res1 == {date(2000, 2, 8): 1.0}


def test_riding_changes_1_election() -> None:
    """Test riding_changes with 1 election"""
    j = Jurisdiction('Canada')
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r1', 'lib', 1)
    e1.update_results('r1', 'pc', 1)
    e1.update_results('r2', 'pc', 1)
    e1.update_results('r2', 'lib', 1)
    e1.update_results('r2', 'green', 1)
    e1.update_results('r2', 'ndp', 1)
    j._history[date(2000, 2, 8)] = e1
    res1 = j.riding_changes()
    assert res1 == []


def test_riding_changes_2_election_same_ridings() -> None:
    """Test riding_changes with 2 elections of same ridings"""
    j = Jurisdiction('Canada')
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r1', 'lib', 1)
    e1.update_results('r1', 'pc', 1)
    e1.update_results('r2', 'pc', 1)
    e1.update_results('r2', 'lib', 1)
    e1.update_results('r2', 'green', 1)
    e1.update_results('r2', 'ndp', 1)
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r1', 'ndp', 1)
    e2.update_results('r2', 'pc', 1)
    j._history[date(2004, 5, 16)] = e2
    j._history[date(2000, 2, 8)] = e1
    res1 = j.riding_changes()
    assert res1 == [(set(), set())]


def test_riding_changes_2_election_different_ridings() -> None:
    """Test riding_changes with 2 elections of totally different ridings"""
    j = Jurisdiction('Canada')
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r1', 'lib', 1)
    e1.update_results('r1', 'pc', 1)
    e1.update_results('r2', 'pc', 1)
    e1.update_results('r2', 'lib', 1)
    e1.update_results('r2', 'green', 1)
    e1.update_results('r2', 'ndp', 1)
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r3', 'ndp', 1)
    e2.update_results('r4', 'pc', 1)
    j._history[date(2004, 5, 16)] = e2
    j._history[date(2000, 2, 8)] = e1
    res1 = j.riding_changes()
    assert res1 == [({'r1', 'r2'}, {'r3', 'r4'})]


def test_riding_changes_3_election_different_ridings() -> None:
    """Test riding_changes with 3 elections of totally different ridings"""
    j = Jurisdiction('Canada')
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r2', 'ndp', 1)
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r3', 'ndp', 1)
    e2.update_results('r4', 'pc', 1)
    e3 = Election(date(2005, 5, 16))
    e3.update_results('r5', 'ndp', 1)
    e3.update_results('r6', 'pc', 1)
    j._history[date(2005, 5, 16)] = e3
    j._history[date(2004, 5, 16)] = e2
    j._history[date(2000, 2, 8)] = e1
    res1 = j.riding_changes()
    assert res1 == [({'r1', 'r2'}, {'r3', 'r4'}), ({'r3', 'r4'}, {'r5', 'r6'})]


def test_riding_changes_3_election_same_ridings() -> None:
    """Test riding_changes with 3 elections of same ridings"""
    j = Jurisdiction('Canada')
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r1', 'lib', 1)
    e1.update_results('r1', 'pc', 1)
    e1.update_results('r2', 'pc', 1)
    e1.update_results('r2', 'lib', 1)
    e1.update_results('r2', 'green', 1)
    e1.update_results('r2', 'ndp', 1)
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r1', 'ndp', 1)
    e2.update_results('r2', 'pc', 1)
    e3 = Election(date(2005, 5, 16))
    e3.update_results('r1', 'ndp', 1)
    e3.update_results('r2', 'pc', 1)
    j._history[date(2005, 5,16)] = e3
    j._history[date(2004, 5, 16)] = e2
    j._history[date(2000, 2, 8)] = e1
    res1 = j.riding_changes()
    assert res1 == [(set(), set()), (set(), set())]


def test_riding_changes_4_election_recuring_ridings() -> None:
    """Test riding_changes with 3 elections of same ridings"""
    j = Jurisdiction('Canada')
    e1 = Election(date(2000, 2, 8))
    e1.update_results('r1', 'ndp', 1)
    e1.update_results('r5', 'lib', 1)
    e1.update_results('r6', 'pc', 1)
    e1.update_results('r2', 'pc', 1)
    e1.update_results('r2', 'lib', 1)
    e1.update_results('r2', 'green', 1)
    e1.update_results('r2', 'ndp', 1)
    e2 = Election(date(2004, 5, 16))
    e2.update_results('r3', 'ndp', 1)
    e2.update_results('r4', 'pc', 1)
    e3 = Election(date(2005, 5, 16))
    e3.update_results('r1', 'ndp', 1)
    e3.update_results('r2', 'pc', 1)
    e4 = Election(date(2006, 5, 16))
    e4.update_results('r3', 'ndp', 1)
    e4.update_results('r2', 'pc', 1)
    e4.update_results('r1', 'pc', 1)
    e4.update_results('r4', 'pc', 1)
    e4.update_results('r5', 'pc', 1)
    j._history[date(2006, 5, 16)] = e4
    j._history[date(2005, 5,16)] = e3
    j._history[date(2004, 5, 16)] = e2
    j._history[date(2000, 2, 8)] = e1
    res1 = j.riding_changes()
    assert res1 == [({'r1', 'r2', 'r5', 'r6'}, {'r3', 'r4'}),
                    ({'r3', 'r4'}, {'r1', 'r2'}), (set(), {'r3', 'r4', 'r5'})]


if __name__ == '__main__':
    import pytest
    pytest.main(['a0_sample_test.py'])
