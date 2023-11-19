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
            assert sympy.isprime(self.ORDER), "%d is not prime" % self.v
            self.ORDER_CHECK_PERFORMED = True
        self.v = v

    def __repr__(self):
        return "F_%d(%d)" % (self.ORDER, self.v)

    def __str__(self):
        return "F_%d(%d)" % (self.ORDER, self.v)

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


class F13(FiniteField):
    ORDER = 13


if __name__ == "__main__":
    print(F13.random() + F13.random())
