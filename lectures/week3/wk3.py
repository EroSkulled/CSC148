"""Prep 3 Synthesize

=== CSC148 Winter 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains an illustration of *inheritance* through an abstract
Employee class that defines a common interface for all of its subclasses.
"""
from datetime import date
from typing import List


class Employee:
    """An employee of a company.

    This is an abstract class. Only child classes should be instantiated.

    === Public attributes ===
    id_: This employee's ID number.
    name: This employee's name.
    """

    #Q: Any variable should be private?
    id_: int
    name: str
    paid: float
    days: [date]
    pay_history: {date, int}

    def __init__(self, id_: int, name: str) -> None:
        """Initialize this employee.

        Note: This initializer is meant for internal use only;
        Employee is an abstract class and should not be instantiated directly.
        """
        self.id_ = id_
        self.name = name
        self.days = []
        self.paid = 0

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.
        """
        return 10.00

    def pay(self, pay_date: date) -> None:
        """Pay this Employee on the given date and record the payment.

        (Assume this is called once per month.)
        """
        payment = self.get_monthly_payment()
        print(f'An employee was paid {payment} on {pay_date}.')
        self.paid += payment
        self.pay_history(pay_date, payment)

    def day_off(self, day: date) -> None:
        if len(self.days) < 10:
            self.days.append(day)


class SalariedEmployee(Employee):
    """An employee whose pay is computed based on an annual salary.

    === Public attributes ===
    salary: This employee's annual salary

    === Representation invariants ===
    - salary >= 0
    """
    id_: int
    name: str
    salary: float

    def __init__(self, id_: int, name: str, salary: float) -> None:
        """Initialize this salaried Employee.

        >>> e = SalariedEmployee(14, 'Fred Flintstone', 5200.0)
        >>> e.salary
        5200.0
        """
        # Note that to call the superclass' initializer, we need to use the
        # full name '__init__'. This is the only time we write '__init__'
        # explicitly.
        Employee.__init__(self, id_, name)
        self.salary = salary

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.

        >>> e = SalariedEmployee(99, 'Mr Slate', 120000.0)
        >>> e.get_monthly_payment()
        10000.0
        """
        return round(self.salary / 12, 2)


class HourlyEmployee(Employee):
    """An employee whose pay is computed based on an hourly rate.

    === Public attributes ===
    hourly_wage:
        This employee's hourly rate of pay.
    hours_per_month:
        The number of hours this employee works each month.

    === Representation invariants ===
    - hourly_wage >= 0
    - hours_per_month >= 0
    """
    id_: int
    name: str
    hourly_wage: float
    hours_per_month: float
    hours_this_month: float

    def __init__(self, id_: int, name: str, hourly_wage: float,
                 hours_per_month: float) -> None:
        """Initialize this HourlyEmployee.

        >>> barney = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> barney.hourly_wage
        1.25
        >>> barney.hours_per_month
        50.0
        """
        Employee.__init__(self, id_, name)
        self.hourly_wage = hourly_wage
        self.hours_per_month = hours_per_month
        self.hours_this_month = hours_per_month

    def get_monthly_payment(self) -> float:
        """Return the amount that this Employee should be paid in one month.

        Round the amount to the nearest cent.

        >>> e = HourlyEmployee(23, 'Barney Rubble', 1.25, 50.0)
        >>> e.get_monthly_payment()
        62.5
        """
        return round(self.hours_per_month * self.hourly_wage, 2)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Remember: you'll need to *run this file* to actually get the lines below
    # to run. This is different than just running doctests.
    # To run this file in PyCharm, right-click in the file and select
    # "Run...", and then select "prep3" from the menu that appears.
    # DON'T select "Doctests in prep3", as that command will not actually
    # run this file, but instead only run its doctests.
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['datetime'],
        'allowed-io': ['pay']
    })
