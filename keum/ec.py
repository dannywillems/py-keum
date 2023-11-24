from abc import ABCMeta, abstractmethod
import random

# From 3.11
from typing import Self, Optional


class EllipticCurve(metaclass=ABCMeta):
    Fr = None
    Fq = None
    COFACTOR = None

    # @classmethod
    # @abstractmethod
    # def check_bytes(cls):
    #     pass

    @classmethod
    @abstractmethod
    def is_in_prime_subgroup(cls, x: Fq, y: Fq) -> bool:
        pass

    @classmethod
    @abstractmethod
    def zero(cls) -> Self:
        pass

    @classmethod
    @abstractmethod
    def generator(cls) -> Self:
        pass

    @classmethod
    def one(cls) -> Self:
        return cls.generator()

    @abstractmethod
    def is_zero(self) -> bool:
        pass

    @abstractmethod
    def double(self) -> Self:
        pass

    @abstractmethod
    def negate(self) -> Self:
        pass

    @classmethod
    @abstractmethod
    def random(cls) -> Self:
        pass

    @abstractmethod
    def __eq__(self: Self, other: Self) -> bool:
        pass

    @abstractmethod
    def __add__(self: Self, other: Self) -> Self:
        pass

    # @abstractmethod
    # def __mul__(self, other):
    #     pass


class Weierstrass(EllipticCurve, metaclass=ABCMeta):
    A = None
    B = None


class AffineWeierstrass(Weierstrass, metaclass=ABCMeta):
    CHECKED_PARAMETERS = False
    GENERATOR_X = None
    GENERATOR_Y = None
    # Redefining for typing
    Fq = None
    Fr = None

    @classmethod
    def generator(cls):
        return cls.from_coordinates_exn(cls.GENERATOR_X, cls.GENERATOR_Y)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_zero(self) -> bool:
        return self.x is None and self.y is None

    @classmethod
    def zero(cls) -> Self:
        return cls(x=None, y=None)

    @classmethod
    def is_on_curve(cls, x: Fq, y: Fq) -> bool:
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
    def from_coordinates_exn(cls, x: Fq, y: Fq) -> Self:
        cls.__check_parameters()
        assert isinstance(x, cls.Fq)
        assert isinstance(y, cls.Fq)
        if cls.is_on_curve(x, y) and cls.is_in_prime_subgroup(x=x, y=y):
            return cls(x, y)
        else:
            raise ValueError("This is not a valid point on the curve")

    @classmethod
    def from_coordinates_opt(cls, x: Fq, y: Fq) -> Self:
        cls.__check_parameters()
        assert isinstance(x, cls.Fq)
        assert isinstance(y, cls.Fq)
        # Check it is on curve
        if cls.is_on_curve(x=x, y=y) and cls.is_in_prime_subgroup(x=x, y=y):
            return cls(x=x, y=y)
        else:
            return None

    def copy(self) -> Self:
        return self.__class__(self.x.copy(), self.y.copy())

    def double(self) -> Self:
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

    def to_compressed_bytes(self):
        raise Exception("Not implemented")

    @classmethod
    def is_in_prime_subgroup(cls, x, y):
        p = cls(x, y)
        if p.is_zero():
            return True
        p_cof = p.mul(cls.Fr(cls.COFACTOR))
        return not p_cof.is_zero()


class ProjectiveWeierstrass(Weierstrass, metaclass=ABCMeta):
    CHECKED_PARAMETERS = False
    GENERATOR_X = None
    GENERATOR_Y = None
    GENERATOR_Z = None
    # Redefining for typing
    Fq = None
    Fr = None

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def zero(cls):
        return cls(x=cls.Fq.zero(), y=cls.Fq.one(), z=cls.Fq.zero())

    def is_zero(self):
        return self.x.is_zero() and self.z.is_zero()

    def copy(self):
        return self.__class__(x=self.x.copy(), y=self.y.copy(), z=self.z.copy())

    def __add__(self, other):
        if self.is_zero():
            return other.copy()
        elif other.is_zero():
            return self.copy()
        else:
            x1z2 = self.x * other.z
            x2z1 = self.z * other.x
            y1z2 = self.y * other.z
            y2z1 = self.z * other.y
            if x1z2 == x2z1 and y1z2 == y2z1:
                xx = self.x.square()
                zz = self.z.square()
                w = (self.A * zz) + (xx + xx + xx)
                y1z1 = self.y * self.z
                s = y1z1 + y1z1
                ss = s.square()
                sss = s * ss
                r = self.y * s
                rr = r.square()
                b = (self.x + r).square() - xx - rr
                h = w.square() - (b + b)
                x3 = h * s
                y3 = (w * (b - h)) - (rr + rr)
                z3 = sss
                return self.__class__(x=x3, y=y3, z=z3)
            else:
                z1z2 = self.z * other.z
                u = y2z1 - y1z2
                uu = u.square()
                v = x2z1 - x1z2
                vv = v.square()
                vvv = v * vv
                r = vv * x1z2
                a = (uu * z1z2) - (vvv + r + r)
                x3 = v * a
                y3 = (u * (r - a)) - (vvv * y1z2)
                z3 = vvv * z1z2
                return self.__class__(x=x3, y=y3, z=z3)

    def double(self):
        return self + self

    def __eq__(self, other):
        if self.z.is_zero() and other.z.is_zero():
            return True
        elif self.z.is_zero() or other.z.is_zero():
            return False
        else:
            x1 = self.x / self.z
            x2 = other.x / other.z
            y1 = self.y / self.z
            y2 = other.y / other.z
            return x1 == x2 and y1 == y2

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

    def to_be_bytes(self):
        x_be = self.x.to_be_bytes()
        y_be = self.y.to_be_bytes()
        z_be = self.z.to_be_bytes()
        return "%s%s%s" % (x_be, y_be, z_be)

    @classmethod
    def of_be_bytes_opt(cls, bs: str) -> Self:
        if len(bs) != 3 * cls.Fq.bytes_length() * 2:
            return None
        x_bs = bs[0:64]
        y_bs = bs[64:128]
        z_bs = bs[128:192]
        x = cls.Fq.of_be_bytes_opt(x_bs)
        y = cls.Fq.of_be_bytes_opt(y_bs)
        z = cls.Fq.of_be_bytes_opt(z_bs)
        if x is None or y is None or z is None:
            return None
        return cls.from_coordinates_opt(x=x, y=y, z=z)

    @classmethod
    def of_be_bytes_exn(cls, bs: str) -> Self:
        if len(bs) != 3 * cls.Fq.bytes_length() * 2:
            return None
        x_bs = bs[0:64]
        y_bs = bs[64:128]
        z_bs = bs[128:192]
        x = cls.Fq.of_be_bytes_exn(x_bs)
        y = cls.Fq.of_be_bytes_exn(y_bs)
        z = cls.Fq.of_be_bytes_exn(z_bs)
        return cls.from_coordinates_exn(x=x, y=y, z=z)

    def to_compressed_bytes(self):
        raise Exception("Not implemented")

    @classmethod
    def __check_parameters(cls):
        if not cls.CHECKED_PARAMETERS:
            assert cls.A is not None
            assert cls.B is not None
            assert cls.COFACTOR is not None
            assert cls.GENERATOR_X is not None
            assert cls.GENERATOR_Y is not None
            assert cls.GENERATOR_Z is not None
            cls.CHECKED_PARAMETERS = True

    @classmethod
    def is_on_curve(cls, x: Fq, y: Fq, z: Fq) -> bool:
        if x.is_zero() and z.is_zero():
            return True
        elif z.is_zero():
            return False
        x_ = x / z
        y_ = y / z
        y2 = y_ * y_
        ax = cls.A * x_
        x2 = x_ * x_
        x3 = x2 * x_
        lhs = y2
        rhs = x3 + ax + cls.B
        return lhs == rhs

    @classmethod
    def is_in_prime_subgroup(cls, x: Fq, y: Fq, z: Fq):
        p = cls(x=x, y=y, z=z)
        if p.is_zero():
            return True
        p_cof = p.mul(cls.Fr(cls.COFACTOR))
        return not p_cof.is_zero()

    @classmethod
    def from_affine_coordinates_exn(cls, x: Fq, y: Fq) -> Self:
        z = cls.Fq.one()
        cls.__check_parameters()
        assert isinstance(x, cls.Fq)
        assert isinstance(y, cls.Fq)
        if cls.is_on_curve(x=x, y=y, z=z) and cls.is_in_prime_subgroup(x=x, y=y, z=z):
            return cls(x=x, y=y, z=cls.Fq.one())
        else:
            raise ValueError("This is not a valid point on the curve")

    @classmethod
    def from_affine_coordinates_opt(cls, x: Fq, y: Fq) -> Self:
        z = cls.Fq.one()
        cls.__check_parameters()
        assert isinstance(x, cls.Fq)
        assert isinstance(y, cls.Fq)
        # Check it is on curve
        if cls.is_on_curve(x=x, y=y, z=z) and cls.is_in_prime_subgroup(x=x, y=y, z=z):
            return cls(x=x, y=y, z=cls.Fq.one())
        else:
            return None

    @classmethod
    def random(cls):
        z = cls.Fq.one()
        y = None
        while y is None:
            x = cls.Fq.random()
            x2 = x * x
            x3 = x2 * x
            y2 = x3 + cls.A * x + cls.B
            # FIXME: seed
            sign = bool(random.getrandbits(1))
            y = y2.sqrt_opt(sign=sign)
        return cls(x=x, y=y, z=z).mul(cls.Fr(cls.COFACTOR))

    @classmethod
    def from_coordinates_opt(cls, x: Fq, y: Fq, z: Fq) -> Optional[Self]:
        if cls.is_on_curve(x=x, y=y, z=z) and cls.is_in_prime_subgroup(x=x, y=y, z=z):
            return cls(x=x, y=y, z=z)
        else:
            return None

    @classmethod
    def from_coordinates_exn(cls, x: Fq, y: Fq, z: Fq) -> Optional[Self]:
        if cls.is_on_curve(x=x, y=y, z=z) and cls.is_in_prime_subgroup(x=x, y=y, z=z):
            return cls(x=x, y=y, z=z)
        else:
            raise ValueError("This is not a valid point on the curve")

    def negate(self):
        return self.__class__(x=self.x, y=self.y.negate(), z=self.z)

    @classmethod
    def generator(cls):
        return cls.from_coordinates_exn(
            x=cls.GENERATOR_X, y=cls.GENERATOR_Y, z=cls.GENERATOR_Z
        )
