import pytest
from keum import FiniteField, PrimeFiniteField
from keum import (
    babyjubjub,
    secp256k1,
    secp256r1,
    pallas,
    vesta,
    tweedledee,
    tweedledum,
    bn254,
    grumpkin,
)


@pytest.fixture(
    params=[
        secp256k1.AffineWeierstrass,
        secp256r1.AffineWeierstrass,
        pallas.AffineWeierstrass,
        bn254.AffineWeierstrass,
        grumpkin.AffineWeierstrass,
        tweedledee.AffineWeierstrass,
        tweedledum.AffineWeierstrass,
        vesta.AffineWeierstrass,
    ]
)
def Ec(request):
    return request.param


def test_random_is_on_the_curve(Ec):
    a = Ec.random()
    assert Ec.is_on_curve(a.x, a.y)


def test_generator_is_on_curve(Ec):
    g = Ec.generator()
    assert Ec.is_on_curve(g.x, g.y)


def test_zero_is_identity_for_addition(Ec):
    a = Ec.random()
    zero = Ec.zero()
    assert a + zero == a
    assert zero + a == a


def test_equality_handles_zero(Ec):
    a = Ec.random()
    zero = Ec.zero()
    assert a != zero
    assert Ec.zero() == Ec.zero()


def test_negate_identity(Ec):
    assert Ec.zero().negate() == Ec.zero()


def test_negate(Ec):
    a = Ec.random()
    assert a == a.negate().negate()


def test_addition_support_same_points(Ec):
    p = Ec.random()
    assert p + p == p.double()


def test_addition_of_two_points_is_on_the_curve(Ec):
    p1 = Ec.random()
    p2 = Ec.random()
    p = p1 + p2
    assert Ec.is_on_curve(x=p.x, y=p.y)


def test_mul_zero_gives_identity(Ec):
    p = Ec.random()
    assert p.mul(Ec.Fr(0)) == Ec.zero()


def test_mul_one_gives_same_point(Ec):
    p = Ec.random()
    assert p.mul(Ec.Fr(1)) == p


def test_mul_by_two_gives_double(Ec):
    p = Ec.random()
    assert p.mul(Ec.Fr(2)) == p.double()


def test_add_is_commutative(Ec):
    p1 = Ec.random()
    p2 = Ec.random()
    lhs = p1 + p2
    rhs = p2 + p1
    assert lhs == rhs


def test_distributivity_scalar_multiplication(Ec):
    a = Ec.Fr.random()
    p1 = Ec.random()
    p2 = Ec.random()
    lhs = (p1 + p2).mul(a)
    rhs = p1.mul(a) + p2.mul(a)
    assert lhs == rhs
