from abc import ABCMeta


class Polynomial(metaclass=ABCMeta):
    Fp = None

    @classmethod
    def __check_parameters(cls):
        assert cls.Fp is not None

    def __init__(self, coefficients):
        self.__check_parameters()
        self.coefficients = coefficients

    @classmethod
    def zero(cls):
        cls.__check_parameters()
        return cls(coefficients=[cls.Fp.zero()])

    @classmethod
    def constant(cls, v):
        cls.__check_parameters()
        return cls(coefficients=v)

    @property
    def degree(self):
        return len(self.coefficients)

    @classmethod
    def of_coefficients(cls, coefficients):
        pass

    def to_coefficients(self):
        return self.coefficients
