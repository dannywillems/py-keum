from keum import PrimeFiniteField
from keum import AffineWeierstrass


class Fq(PrimeFiniteField):
    ORDER = (
        21888242871839275222246405745257275088548364400416034343698204186575808495617
    )


class Fr(PrimeFiniteField):
    ORDER = (
        21888242871839275222246405745257275088696311157297823662689037894645226208583
    )


class AffineWeierstrass(AffineWeierstrass):
    Fq = Fq
    Fr = Fr
    A = Fq(0)
    B = Fq(3)
    COFACTOR = 1
    GENERATOR_X = Fq(1)
    GENERATOR_Y = Fq(2)
