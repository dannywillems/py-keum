import pytest
from keum import FiniteField, PrimeFiniteField
from keum import babyjubjub


@pytest.fixture
def Ec():
    return babyjubjub.AffineWeierstrass


def test_random_is_on_the_curve(Ec):
    a = Ec.random()
    assert Ec.is_on_curve(a.x, a.y)


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


def test_add_is_commutative(Ec):
    p1 = Ec.random()
    p2 = Ec.random()
    assert p1 + p2 == p2 + p1
