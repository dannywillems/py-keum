from abc import ABCMeta, abstractmethod
from ff import FiniteField
import typing


class EllipticCurve(metaclass=ABCMeta):
    Fr = None
    Fq = None

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

    # @classmethod
    # def zero(cls):
    #     pass

    # @classmethod
    # def one(cls):
    #     pass

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
    def random(cls):
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


class Weierstrass(EllipticCurve, ABCMeta):
    A = None
    B = None
    COFACTOR = None


class AffineWeierstrass(Weierstrass, ABCMeta):
    CHECKED_PARAMETERS = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __check_parameters(self):
        if not self.CHECKED_PARAMETERS:
            assert self.A is not None
            assert self.B is not None
            assert self.COFACTOR is not None
            self.CHECKED_PARAMETERS = True

    @classmethod
    def from_coordinates_exn(cls, x, y):
        assert isinstance(x, cls.Fq)
        assert isinstance(y, cls.Fq)

    @classmethod
    def from_coordinates_opt(cls, x, y):
        cls.__check_parameters()
        assert isinstance(x, cls.Fq)
        assert isinstance(y, cls.Fq)
        # Check it is on curve
        return cls(x=x, y=y)

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __add__(self, other):
        # Handle zero
        y2_min_y1 = other.y - self.y
        x2_min_x1 = other.x - self.x
        slope = y2_min_y1 / x2_min_x1
        square_slope = slope * slope
        x3 = square_slope + self.x.negate() + other.x.negate()
        double_x1 = self.x + self.x
        double_x1_plus_x2 = double_x1 + other.x
        y3 = double_x1_plus_x2 * slope + (square_slope * slope).negate() + \
            self.y.negate()
        return self.__class__(x3, y3)


    def to_bytes(self):
        pass

    def to_compressed_bytes(self):
        pass

    def is_on_curve(self):
        y2 = self.y * self.y
        x2 = self.x * self.x
        x3 = x2 * self.x
        return y2 == (x3 + self.A * self.x + self.B)
