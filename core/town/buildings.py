__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from ..life.person import Person
from ..life import time
from ..objects.product import Product, QuantifiedProduct


class Building:
    def __init__(self, name: str, street: object, *interests_involved):
        self.name = name
        self.street = street
        self.interests_involved = interests_involved
        self.persons = []

    def can_interest(self, person: Person) -> float:
        """Return a percentage of possibility to interest someone"""
        score = 0
        for interest in person.interests:
            if interest in self.interests_involved:
                score += 1
        return score / len(self.interests_involved)

    def _update(self, clock: object):
        """This will update some parts of the building"""
        for person in self.persons:
            person.handle_event(time.Condition("persons", [_ for _ in self.persons if _ != person], 0.1))
            person.evolve(clock)

    def evolve(self, clock: object) -> object:
        """
            Allow all the components to evolve. All the update() of these elements will be launched
            one time
        """
        print("\t\t {} is evolving".format(self))
        self._update(clock)
        return self

    def get_location(self) -> object:
        """Get the Street where this building is located"""
        return self.street

    def quit(self, person: object) -> object:
        """Allow a member of the building to quit it in order, for example, to go to work"""
        return self.street.add_a_person(person)

    def _has_person(self, person: Person):
        """Return True or False whether an habitant is in the house or not"""
        return person in self.persons

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name + " Building's"


class House(Building):
    def __init__(self, name: str, on_street: object, *interests_involved):
        super().__init__(name, on_street, *interests_involved)

    def has_habitant(self, habitant: Person) -> bool:
        """Return True or False whether an habitant is in the house or not"""
        return self._has_person(habitant)

    def has_habitant_name(self, habitant_name: str) -> bool:
        """Return True or False whether an habitant with the name given is in the house or not"""
        for habitant in self.persons:
            if habitant.name == habitant_name:
                return True
        return False

    def get_habitant_by_name(self, habitant_name: str) -> Person:
        """Return a Person object, which matches the name given"""
        if self.has_habitant_name(habitant_name):
            for habitant in self.persons:
                if habitant.name == habitant_name:
                    return habitant
        else:
            raise ValueError("'{}' does not match any habitant".format(habitant_name))

    def add_settler(self, habitant: Person) -> object:
        """Add a person in a house (he/she is not in the house, but living in)"""
        self.persons.append(habitant)
        return self

    def remove_settler(self, habitant_name: str) -> object:
        """Remove someone from the house (he/she can be outside the house, he/she will just have to found
           a new house)"""
        for i in range(len(self.persons)):
            if self.persons[i].name == habitant_name:
                self.persons.pop(i)
                break
        return self

    def evolve(self, clock: object) -> object:
        """
            Allow all the components to evolve. All the update() of these elements will be launched
            one time
        """
        print("\t\t {} is evolving".format(self))

        self._update(clock)
        return self


class CommercialBuilding(Building):
    def __init__(self, name: str="", chief: Person=Person(), *interests_involved):
        super().__init__(name, *interests_involved)
        self.capital = 0
        self._last_capital = self.capital
        self._capital_history = {}
        self.available_goods = {}
        self.chief = chief
        self.employees = []
        self._is_searching_for_applicants = False

    def hire_somebody(self, somebody: Person) -> object:
        """Hire a new person in the enterprise / shop"""
        self.employees.append(somebody)
        return self

    def is_searching_for_applicants(self) -> bool:
        """Return True or False whether the entreprise / shop is searching for someone"""
        return self._is_searching_for_applicants

    def is_in_deficit(self) -> bool:
        """Check if the CommercialBuilding is in deficit and return True or False"""
        if self.capital <= 0:
            return True
        return False

    def has_product_name(self, product_name: str) -> bool:
        """Check if the CommercialBuilding has product_name in his available_goods"""
        if product_name in self.available_goods.keys():
            return True
        return False

    def buy(self, product: Product, quantity: int) -> object:
        """Buy a product whom quantity is given, and deduce the calculated price from the capital"""
        self.capital -= product.price * quantity
        if product.name not in self.available_goods.keys():
            self.available_goods[product.name] = QuantifiedProduct().construct_from_product(product, quantity)
        else:
            self.available_goods[product.name].quantity += quantity
        return self

    def evolve(self, clock: time.Time) -> object:
        """
            Allow all the components to evolve. All the update() of these elements will be launched
            one time
        """
        print("\t\t {} is evolving".format(self))

        if self.is_in_deficit():
            self._is_searching_for_applicants = False
        if self.capital != self._last_capital:
            self._capital_history[clock.time] = self.capital
        self._last_capital = self.capital

        self._update(clock)

        return self


class Shop(CommercialBuilding):
    def __init__(self, name: str="", *interests_involved):
        super().__init__(name, *interests_involved)


class Enterprise(CommercialBuilding):
    def __init__(self, name: str="", *interests_involved):
        super().__init__(name, *interests_involved)