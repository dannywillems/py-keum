from keum import PrimeFiniteField
from keum import AffineWeierstrass


class Fq(PrimeFiniteField):
    ORDER = (
        28948022309329048855892746252171976963322203655954433126947083963168578338817
    )


class Fr(PrimeFiniteField):
    ORDER = (
        28948022309329048855892746252171976963322203655955319056773317069363642105857
    )


class AffineWeierstrass(AffineWeierstrass):
    Fq = Fq
    Fr = Fr
    A = Fq(0)
    B = Fq(5)
    COFACTOR = 1
    GENERATOR_X = Fq(1).negate()
    GENERATOR_Y = Fq(2)
