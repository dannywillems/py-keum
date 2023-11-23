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

    @classmethod
    def zero(cls):
        return cls(0)

    @classmethod
    def one(cls):
        return cls(1)

    def is_zero(self):
        return self.v == 0

    def is_one(self):
        return self.v == 1

    def __repr__(self):
        return "F_%d(%d)" % (self.ORDER, self.v)

    def __str__(self):
        return "F_%d(%d)" % (self.ORDER, self.v)

    def __eq__(self, other):
        # Hypothesis: both are smaller than the order.
        if isinstance(other, self.__class__):
            return self.v == other.v
        raise ValueError("Equality only possible between element of the same field")

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__((self.v + other.v) % self.ORDER)
        raise ValueError("Addition only possible between element of the same field")

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__((self.v * other.v) % self.ORDER)
        raise ValueError(
            "Multiplication only possible between element of the same field"
        )

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__((self.v - other.v) % self.ORDER)
        raise ValueError("Substraction only possible between element of the same field")

    # Verify it corresponds to `/`
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            if other.is_zero():
                raise ValueError("Division by zero")
            return self.__class__((self.v / other.v) % self.ORDER)
        raise ValueError("Division only possible between element of the same field")

    # To test
    def pow(self, n):
        def aux(x, acc, n):
            if n == 1:
                return acc * x
            elif n % 2 == 0:
                return aux(x, acc * acc, n // 2)
            else:
                return aux(x, acc * x, n - 1)

        if n == 0:
            return self.__class__.one()
        elif n == 1:
            return self.__class__(self.v)
        else:
            return aux(self, self, n)

    # To test
    def inverse(self):
        if self.is_zero():
            raise ValueError("Zero has no inverse")
        return self.pow(self.ORDER - 1)

    # Add a seed
    @classmethod
    def random(cls):
        v = random.randint(0, cls.ORDER - 1)
        return cls(v)


class PrimeFiniteField(FiniteField):
    PRIME_DECOMPOSITION = None

    def __div__(self, other):
        if isinstance(other, self.__class__):
            if other.is_zero():
                raise ValueError("Division by zero")
            return self.__class__((self.v / other.v) % self.ORDER)

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
