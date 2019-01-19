"""CSC148 Prep 3: Inheritance

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Prep 3.

WARNING: THIS IS AN EXTREMELY INCOMPLETE SET OF TESTS!
Add your own to practice writing tests and to be confident your code is correct.

For more information on hypothesis (one of the testing libraries we're using),
please see
<http://www.teach.cs.toronto.edu/~csc148h/fall/software/hypothesis.html>.

Note: this file is for support purposes only, and is not part of your
submission.
"""
from datetime import date

from prep3 import SalariedEmployee, HourlyEmployee, Company


def test_total_pay_basic() -> None:
    e = SalariedEmployee(14, 'Gilbert the cat', 1200.0)
    e.pay(date(2018, 6, 28))
    e.pay(date(2018, 7, 28))
    e.pay(date(2018, 8, 28))
    assert e.total_pay() == 300.0


def test_total_pay_mixed() -> None:
    e = SalariedEmployee(14, 'Gilbert the cat', 1200.0)
    f = HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)
    e.pay(date(2018, 6, 28))
    e.pay(date(2018, 7, 28))
    f.pay(date(2018, 8, 28))
    assert e.total_pay() == 200.0
    assert f.total_pay() == 500.25


def test_total_payroll_mixed() -> None:
    my_corp = Company([SalariedEmployee(24, 'Gilbert the cat', 1200.0),
                       HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)])
    my_corp.pay_all(date(2018, 6, 28))
    assert my_corp.total_payroll() == 600.25


def test_total_payroll_advanced() -> None:
    my_corp = Company([SalariedEmployee(24, 'Gilbert the cat', 1200.0),
                       HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)])
    my_corp1 = Company([SalariedEmployee(24, 'Gilbert the cat', 1200.0),
                       HourlyEmployee(25, 'Chairman Meow', 500.25, 1.0)])
    my_corp.pay_all(date(2018, 6, 28))
    my_corp1.pay_all(date(2018, 6, 28))
    my_corp1.pay_all(date(2018, 7, 28))
    assert my_corp.total_payroll() == 600.25
    assert my_corp1.total_payroll() == 1200.5


if __name__ == '__main__':
    import pytest
    pytest.main(['prep3_sample_test.py'])