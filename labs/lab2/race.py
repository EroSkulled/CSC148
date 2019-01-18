class Race:
    """
    5k race
    === Attributes ===
    cat: the runner's speed category.

    === Sample Usage ===
    >>> r = Race(1)
    >>> r.cat
    1
    >>> r.runners
    []
    """

    cat: int
    runners: list

    def __init__(self, category: int) -> None:
        """
        Initialize a new race with category

        === Sample Usage ===
        >>> r = Race(3)
        >>> r.cat
        3
        """
        self.cat = category
        self.runners = []

    def register(self, name: str, email: str) -> None:
        """
        Register a runner

        === Sample Usage ===
        >>> r = Race(1)
        >>> r.register('Allen', 'xxx@hotmail.com')
        >>> r.runners
        ['Allen']
        """
        Runner(name, self.cat, email)
        self.runners.append(name)


class Runner:
    """
    Runner
    === Attributes ===
    name: runner's name.
    email: their email address

    === Sample Usage ===

    """
    name: str
    email: str

    def __init__(self, name: str, cat: int, email: str) -> None:
        self.cat = cat
        self.name = name
        self.email = email

    def change_email(self, new_email: str) -> None:
        self.email = new_email

    def change_category(self, new_category: int) -> None:
        self.cat = new_category


if __name__ == '__main__':
    import doctest
    doctest.testmod()
