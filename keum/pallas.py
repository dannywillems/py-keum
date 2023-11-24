from keum import PrimeFiniteField
from keum import AffineWeierstrass, ProjectiveWeierstrass


class Fr(PrimeFiniteField):
    ORDER = (
        28948022309329048855892746252171976963363056481941647379679742748393362948097
    )


class Fq(PrimeFiniteField):
    ORDER = (
        28948022309329048855892746252171976963363056481941560715954676764349967630337
    )


class AffineWeierstrass(AffineWeierstrass):
    Fq = Fq
    Fr = Fr
    A = Fq(0)
    B = Fq(5)
    COFACTOR = 1
    GENERATOR_X = Fq(1).negate()
    GENERATOR_Y = Fq(2)


class ProjectiveWeierstrass(ProjectiveWeierstrass):
    Fq = Fq
    Fr = Fr
    A = Fq(0)
    B = Fq(5)
    COFACTOR = 1
    GENERATOR_X = Fq(1).negate()
    GENERATOR_Y = Fq(2)
    GENERATOR_Z = Fq(1)
