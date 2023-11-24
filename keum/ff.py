from abc import ABC, abstractmethod
import sympy
import random
from typing import Self


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
    @abstractmethod
    def zero(cls):
        pass

    @classmethod
    @abstractmethod
    def one(cls):
        pass

    @abstractmethod
    def is_zero(self):
        pass

    @abstractmethod
    def is_one(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def negate(self):
        pass

    def square(self):
        return self.__class__(v=(self.v * self.v) % self.ORDER)

    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def sqrt_opt(self, sign: bool):
        pass

    @abstractmethod
    def pow(self, n):
        pass

    @abstractmethod
    def inverse(self):
        pass

    # Add a seed
    @classmethod
    @abstractmethod
    def random(cls):
        pass

    @abstractmethod
    def to_be_bytes(self):
        pass

    @classmethod
    @abstractmethod
    def of_be_bytes_exn(cls):
        pass


class PrimeFiniteField(FiniteField):
    PRIME_DECOMPOSITION = None

    @classmethod
    def zero(cls):
        return cls(0)

    @classmethod
    def one(cls):
        return cls(1)

    def double(self):
        return self + self

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

    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            if other.is_zero():
                raise ValueError("Division by zero")
            return self * other.inverse()
        raise ValueError("Division only possible between element of the same field")

    def copy(self):
        return self.__class__(self.v)

    @classmethod
    def prime_decomposition_multiplicative_subgroup(cls):
        if cls.PRIME_DECOMPOSITION is None:
            cls.__check_order()
            res = sympy.ntheory.factorint(cls.ORDER - 1)
            cls.PRIME_DECOMPOSITION = res
        return cls.PRIME_DECOMPOSITION

    def legendre_symbol(self):
        if self.is_zero():
            return 0
        tmp = self.pow(self.ORDER / 2)
        if tmp.is_one():
            return 1
        else:
            return -1

    def is_quadratic_residue(self):
        if self.is_zero():
            return True
        else:
            return self.legendre_symbol() == 1

    def negate(self):
        return self.__class__(self.ORDER - self.v)

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

    @classmethod
    def random(cls):
        v = random.randint(0, cls.ORDER - 1)
        return cls(v)

    def sqrt_opt(self, sign: bool):
        # TODO: reimplement
        from sympy.ntheory import sqrt_mod

        s = sqrt_mod(self.v, self.ORDER)
        if s is None:
            return s
        s = self.__class__(s)
        if sign:
            return s
        else:
            return s.negate()

    def pow(self, n):
        if n == 0:
            return self.__class__.one()
        n_bits = format(n, "b")[1:]
        acc = self.copy()
        for b in n_bits:
            acc *= acc
            if b == "1":
                acc = acc * self
        return acc

    def inverse(self):
        if self.is_zero():
            raise ValueError("Zero has no inverse")
        return self.pow(self.ORDER - 2)

    def __init__(self, v):
        self.__check_order()
        self.v = v

    def to_int(self):
        return self.v

    def to_be_bytes(self) -> str:
        return hex(self.v)[2:]

    @classmethod
    def of_be_bytes_opt(cls, bs: str) -> Self:
        bs = "0x%s" % bs
        v = int(bs, 16)
        if v >= cls.ORDER:
            return None
        return cls(v)

    @classmethod
    def of_be_bytes_exn(cls, bs: str) -> Self:
        bs = "0x%s" % bs
        v = int(bs, 16)
        if v >= cls.ORDER:
            raise ValueError("The value must be smaller than the order of the field")
        return cls(v)
