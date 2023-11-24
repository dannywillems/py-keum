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

    @abstractmethod
    def double(self):
        pass

    @abstractmethod
    def negate(self):
        pass

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

    def copy(self):
        return self.__class__(self.x.copy(), self.y.copy())

    def double(self):
        if self.is_zero():
            return self.zero()
        xx = self.x.square()
        xx_3_plus_a = xx.double() + xx + self.A
        double_x = self.x.double()
        double_y = self.y.double()
        square_double_y = double_y.square()
        x3 = xx_3_plus_a.square() / square_double_y - double_x
        triple_x = self.x + double_x
        tmp1 = triple_x * xx_3_plus_a / double_y
        tmp2 = xx_3_plus_a.square() * xx_3_plus_a
        tmp3 = square_double_y * double_y
        y3 = tmp1 - (tmp2 / tmp3) - self.y
        return self.__class__(x3, y3)

    def mul(self, n):
        def aux(x, n):
            if n == 0:
                return self.__class__.zero()
            elif n == 1:
                return x.copy()
            elif n % 2 == 0:
                return aux(x.double(), n / 2)
            else:
                return x + aux(x, n - 1)

        return aux(self, n.to_int())

    def __eq__(self, other):
        if self.is_zero() and other.is_zero():
            return True
        elif self.is_zero():
            return False
        elif other.is_zero():
            return False
        return (self.x == other.x) and (self.y == other.y)

    # https://hyperelliptic.org/EFD/g1p/auto-shortw.html
    def __add__(self, other):
        if self.is_zero() and other.is_zero():
            return self.__class__(x=None, y=None)
        if self.is_zero():
            return self.__class__(other.x, other.y)
        elif other.is_zero():
            return self.__class__(self.x, self.y)
        elif self.x == other.x and self.y == other.y.negate():
            return self.__class__.zero()
        elif self.x == other.x and self.y == other.y:
            return self.double()
        # y2 - y1
        y2_min_y1 = other.y - self.y
        # x2 - x1
        x2_min_x1 = other.x - self.x
        # (y2 - y1) / (x2 - x1)
        slope = y2_min_y1 / x2_min_x1
        # [(y2 - y1) / (x2 - x1)]^2
        square_slope = slope.square()
        # [(y2 - y1) / (x2 - x1)]^2 - x2 - x1
        x3 = square_slope - self.x - other.x
        # 2 * x1
        double_x1 = self.x.double()
        # 2 * x1 + x2
        double_x1_plus_x2 = double_x1 + other.x
        # 2 * x1 + x2 * [(y2 - y1) / (x2 - x1)]
        tmp1 = double_x1_plus_x2 * slope
        cube_slope = square_slope * slope
        y3 = tmp1 - cube_slope - self.y
        return self.__class__(x3, y3)

    def negate(self):
        if self.is_zero():
            return self.__class__.zero()
        return self.__class__(self.x, self.y.negate())

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
        return cls(x, y).mul(cls.Fr(cls.COFACTOR))

    def to_bytes(self):
        pass

    def to_compressed_bytes(self):
        pass
