from keum import PrimeFiniteField
from keum import AffineWeierstrass


class Fr(PrimeFiniteField):
    ORDER = 2736030358979909402780800718157159386076813972158567259200215660948447373041


class Fq(PrimeFiniteField):
    ORDER = (
        21888242871839275222246405745257275088548364400416034343698204186575808495617
    )


class AffineWeierstrass(AffineWeierstrass):
    Fq = Fq
    Fr = Fr
    A = Fq(168700)
    B = Fq(168696)
    COFACTOR = Fq(8)
