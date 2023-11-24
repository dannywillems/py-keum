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
        pallas.ProjectiveWeierstrass,
        bn254.AffineWeierstrass,
        grumpkin.AffineWeierstrass,
        tweedledee.AffineWeierstrass,
        tweedledum.AffineWeierstrass,
        vesta.AffineWeierstrass,
    ]
)
def Ec(request):
    return request.param


@pytest.fixture(
    params=[
        pallas.ProjectiveWeierstrass,
    ]
)
def ProjectiveEc(request):
    return request.param


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
def AffineEc(request):
    return request.param


def test_affine_random_is_on_the_curve(AffineEc):
    a = AffineEc.random()
    assert AffineEc.is_on_curve(a.x, a.y)


# def test_affine_encoding_decoding(AffineEc):
#     a = AffineEc.random()
#     assert AffineEc.of_be_bytes_exn(a.to_be_bytes()) == a
#     assert AffineEc.of_be_bytes_opt(a.to_be_bytes()) == a


def test_projective_encoding_decoding(ProjectiveEc):
    a = ProjectiveEc.random()
    assert ProjectiveEc.of_be_bytes_exn(a.to_be_bytes()) == a
    assert ProjectiveEc.of_be_bytes_opt(a.to_be_bytes()) == a


def test_affine_generator_is_on_curve(AffineEc):
    g = AffineEc.generator()
    assert AffineEc.is_on_curve(g.x, g.y)


def test_projective_random_is_on_the_curve(ProjectiveEc):
    a = ProjectiveEc.random()
    assert ProjectiveEc.is_on_curve(x=a.x, y=a.y, z=a.z)


def test_projective_generator_is_on_curve(ProjectiveEc):
    g = ProjectiveEc.generator()
    assert ProjectiveEc.is_on_curve(x=g.x, y=g.y, z=g.z)


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


def test_affine_addition_of_two_points_is_on_the_curve(AffineEc):
    p1 = AffineEc.random()
    p2 = AffineEc.random()
    p = p1 + p2
    assert AffineEc.is_on_curve(x=p.x, y=p.y)


def test_projective_addition_of_two_points_is_on_the_curve(ProjectiveEc):
    p1 = ProjectiveEc.random()
    p2 = ProjectiveEc.random()
    p = p1 + p2
    assert ProjectiveEc.is_on_curve(x=p.x, y=p.y, z=p.z)


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
