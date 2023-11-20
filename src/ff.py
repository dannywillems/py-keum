from abc import ABC, abstractmethod
import sympy
import random


class FiniteField(ABC):
    ORDER = None
    # This is set to True when a first object is instantiated. It avoids potential heavy computation
    ORDER_CHECK_PERFORMED = False

    def __init__(self, v):
        if not self.ORDER_CHECK_PERFORMED:
            assert self.ORDER is not None
            self.ORDER_CHECK_PERFORMED = True
        self.v = v % self.ORDER

    def __repr__(self):
        return "F_%d(%d)" % (self.ORDER, self.v)

    def __str__(self):
        return "F_%d(%d)" % (self.ORDER, self.v)

    def __eq__(self, other):
        # Hypothesis: both are smaller than the order.
        return self.v == other.v

    def __add__(self, other):
        return self.__class__((self.v + other.v) % self.ORDER)

    def __mul__(self, other):
        return self.__class__((self.v * other.v) % self.ORDER)

    def __sub__(self, other):
        return self.__class__((self.v - other.v) % self.ORDER)

    def __div__(self, other):
        if other.v == 0:
            raise ValueError("Division by zero")
        return self.__class__((self.v / other.v) % self.ORDER)

    @classmethod
    def random(cls):
        v = random.randint(0, cls.ORDER - 1)
        return cls(v)


class PrimeFiniteField(FiniteField):
    PRIME_DECOMPOSITION = None

    @classmethod
    def prime_decomposition_multiplicative_subgroup(cls):
        if cls.PRIME_DECOMPOSITION is None:
            cls.__check_order()
            res = sympy.ntheory.factorint(cls.ORDER - 1)
            cls.PRIME_DECOMPOSITION = res
        return cls.PRIME_DECOMPOSITION

    @classmethod
    def highest_power_of_two(cls):
        prime_decomposition = cls.prime_decomposition_multiplicative_subgroup()
        return prime_decomposition[2] if 2 in prime_decomposition else 0

    @classmethod
    def __check_order(cls):
        if not cls.ORDER_CHECK_PERFORMED:
            assert cls.ORDER is not None
            assert sympy.isprime(cls.ORDER), "%d is not prime" % cls.ORDER
            cls.ORDER_CHECK_PERFORMED = True

    def __init__(self, v):
        self.__check_order()
        self.v = v


class F13(PrimeFiniteField):
    ORDER = 13


if __name__ == "__main__":
    print(F13.random() + F13.random())
    print(F13.prime_decomposition_multiplicative_subgroup())
    print(F13.highest_power_of_two())
