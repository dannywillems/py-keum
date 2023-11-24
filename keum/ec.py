from abc import ABCMeta, abstractmethod
from keum import FiniteField, PrimeFiniteField
import random
import typing


class EllipticCurve(metaclass=ABCMeta):
    Fr = None
    Fq = None

    @classmethod
    @abstractmethod
    def zero(cls):
        pass

    # @classmethod
    # @abstractmethod
    # def check_bytes(cls):
    #     pass

    # @classmethod
    # @abstractmethod
    # def of_bytes_opt(cls):
    #     pass

    # @classmethod
    # @abstractmethod
    # def of_bytes_exn(cls):
    #     pass

    @classmethod
    def zero(cls):
        pass

    @classmethod
    def one(cls):
        pass

    @abstractmethod
    def is_zero(self):
        pass

    # @abstractmethod
    # def double(self):
    #     pass

    # @abstractmethod
    # def negate(self):
    #     pass

    @abstractmethod
    def to_bytes(self):
        pass

    @classmethod
    @abstractmethod
    def random(cls):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __add__(self, other):
        pass

    # @abstractmethod
    # def __mul__(self, other):
    #     pass


class Weierstrass(EllipticCurve, metaclass=ABCMeta):
    A = None
    B = None
    COFACTOR = None
    GENERATOR_X = None
    GENERATOR_Y = None


class AffineWeierstrass(Weierstrass, metaclass=ABCMeta):
    CHECKED_PARAMETERS = False

    @classmethod
    def generator(cls):
        return cls.from_coordinates_exn(cls.GENERATOR_X, cls.GENERATOR_Y)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_zero(self):
        return self.x is None and self.y is None

    @classmethod
    def zero(cls):
        return cls(x=None, y=None)

    @classmethod
    def one(cls):
        return cls.generator()

    @classmethod
    def is_on_curve(cls, x, y):
        y2 = y * y
        ax = cls.A * x
        x2 = x * x
        x3 = x2 * x
        lhs = y2
        rhs = x3 + ax + cls.B
        print(lhs)
        print(rhs)
        return lhs == rhs

    @classmethod
    def __check_parameters(cls):
        if not cls.CHECKED_PARAMETERS:
            assert cls.A is not None
            assert cls.B is not None
            assert cls.COFACTOR is not None
            assert cls.GENERATOR_X is not None
            assert cls.GENERATOR_Y is not None
            cls.CHECKED_PARAMETERS = True

    @classmethod
    def from_coordinates_exn(cls, x, y):
        cls.__check_parameters()
        assert isinstance(x, cls.Fq)
        assert isinstance(y, cls.Fq)
        if cls.is_on_curve(x, y):
            return cls(x, y)
        else:
            raise ValueError("This is not a valid point on the curve")

    @classmethod
    def from_coordinates_opt(cls, x, y):
        cls.__check_parameters()
        assert isinstance(x, cls.Fq)
        assert isinstance(y, cls.Fq)
        # Check it is on curve
        if cls.is_on_curve(x, y):
            return cls(x=x, y=y)
        else:
            return None

    def __eq__(self, other):
        if self.is_zero() and other.is_zero():
            return True
        elif self.is_zero():
            return False
        elif other.is_zero():
            return False
        return (self.x == other.x) and (self.y == other.y)

    def __add__(self, other):
        if self.is_zero() and other.is_zero():
            return self.__class__(x=None, y=None)
        if self.is_zero():
            return self.__class__(other.x, other.y)
        elif other.is_zero():
            return self.__class__(self.x, self.y)
        elif self.x == other.x and self.y == other.y.negate():
            return self.__class__.zero()
        y2_min_y1 = other.y - self.y
        x2_min_x1 = other.x - self.x
        slope = y2_min_y1 / x2_min_x1
        square_slope = slope * slope
        x3 = square_slope - self.x - other.x
        double_x1 = self.x + self.x
        double_x1_plus_x2 = double_x1 + other.x
        y3 = double_x1_plus_x2 * slope - (square_slope * slope) - self.y
        return self.__class__(x3, y3)

    @classmethod
    def random(cls):
        y = None
        while y is None:
            x = cls.Fq.random()
            x2 = x * x
            x3 = x2 * x
            y2 = x3 + cls.A * x + cls.B
            # FIXME: seed
            sign = bool(random.getrandbits(1))
            y = y2.sqrt_opt(sign=sign)
        return cls(x, y)

    def to_bytes(self):
        pass

    def to_compressed_bytes(self):
        pass
