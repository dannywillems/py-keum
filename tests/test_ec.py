import pytest
from keum import FiniteField, PrimeFiniteField
from keum import babyjubjub, secp256k1, secp256r1, pallas, vesta, tweedledee, tweedledum


@pytest.fixture(
    params=[
        secp256k1.AffineWeierstrass,
        secp256r1.AffineWeierstrass,
        pallas.AffineWeierstrass,
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
    assert (a == a.negate().negate())

def test_addition_of_two_points_is_on_the_curve(Ec):
    p1 = Ec.random()
    p2 = Ec.random()
    p = p1 + p2
    assert Ec.is_on_curve(p.x, p.y)


# def test_add_is_commutative(Ec):
#     p1 = Ec.random()
#     p2 = Ec.random()
#     print(p1.x)
#     print(p1.y)
#     print(p2.x)
#     print(p2.y)
#     lhs = p1 + p2
#     rhs = p2 + p1
#     print(lhs.x)
#     print(lhs.y)
#     print(rhs.x)
#     print(rhs.y)

#     assert lhs == rhs
