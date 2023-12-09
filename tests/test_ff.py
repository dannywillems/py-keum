import pytest
from keum import FiniteField, PrimeFiniteField
from keum import secp256k1


class F13(PrimeFiniteField):
    ORDER = 13


class F17(PrimeFiniteField):
    ORDER = 17


class F17_2(FiniteField):
    Fp = F17
    nsqrt = F17.one().negate()

@pytest.fixture(params=[F13, F17, secp256k1.AffineWeierstrass.Fr, F17_2])
def Finite_field_instance(request):
    return request.param


def test_cannot_divide_when_different_fields():
    a = F13.random()
    b = F17.random()
    with pytest.raises(ValueError):
        a / b


def test_cannot_substract_when_different_fields():
    a = F13.random()
    b = F17.random()
    with pytest.raises(ValueError):
        a - b


def test_cannot_add_when_different_fields():
    a = F13.random()
    b = F17.random()
    with pytest.raises(ValueError):
        a + b


def test_negate(Finite_field_instance):
    a = Finite_field_instance.random()
    assert a + a.negate() == Finite_field_instance.zero()


def test_cannot_multiply_when_different_fields():
    a = F13.random()
    b = F17.random()
    with pytest.raises(ValueError):
        a * b


def test_sqrt(Finite_field_instance):
    a = Finite_field_instance.random()
    a_sqrt = a.sqrt_opt(sign=True)
    while a_sqrt is None:
        a = Finite_field_instance.random()
        a_sqrt = a.sqrt_opt(sign=True)
    assert a_sqrt * a_sqrt == a
    # Opposite
    a_sqrt = a.sqrt_opt(sign=False)
    assert a_sqrt * a_sqrt == a


def test_cannot_divide_by_zero(Finite_field_instance):
    x = Finite_field_instance.random()
    # Check exception raised
    with pytest.raises(ValueError):
        x / Finite_field_instance.zero()


def test_addition_commutative(Finite_field_instance):
    a = Finite_field_instance.random()
    b = Finite_field_instance.random()
    assert a + b == b + a


def test_addition_associativity(Finite_field_instance):
    a = Finite_field_instance.random()
    b = Finite_field_instance.random()
    c = Finite_field_instance.random()
    assert a + (b + c) == (a + b) + c


def test_distributivity(Finite_field_instance):
    a = Finite_field_instance.random()
    b = Finite_field_instance.random()
    c = Finite_field_instance.random()
    assert a * (b + c) == a * b + a * c


def test_multiplication_commutative(Finite_field_instance):
    a = Finite_field_instance.random()
    b = Finite_field_instance.random()
    assert a * b == b * a


def test_inverse_twice(Finite_field_instance):
    a = Finite_field_instance.random()
    while a.is_zero():
        a = Finite_field_instance.random()
    assert a.inverse().inverse() == a


def test_one_is_identity_for_multiplication(Finite_field_instance):
    r = Finite_field_instance.random()
    assert r * Finite_field_instance.one() == r


def test_zero_is_identity_for_addition(Finite_field_instance):
    r = Finite_field_instance.random()
    assert r + Finite_field_instance.zero() == r


def test_inverse_of_one_is_one(Finite_field_instance):
    one = Finite_field_instance.one()
    assert one.inverse() == one


def test_zero_has_no_inverse(Finite_field_instance):
    with pytest.raises(ValueError):
        Finite_field_instance.zero().inverse()


def test_inverse(Finite_field_instance):
    a = Finite_field_instance.random()
    while a.is_zero():
        a = Finite_field_instance.random()
    assert a.inverse() * a == Finite_field_instance.one()


def test_inverse_in_f13():
    two = F13(2)
    two_inverse = F13(7)
    assert two.inverse() == two_inverse


def test_is_zero(Finite_field_instance):
    two = Finite_field_instance(2)
    assert not two.is_zero()


def test_is_one(Finite_field_instance):
    two = Finite_field_instance(2)
    assert not two.is_one()


def test_pow_zero_random_value_is_zero(Finite_field_instance):
    a = Finite_field_instance.random()
    assert a.pow(0) == Finite_field_instance.one()


def test_pow_one_random_value(Finite_field_instance):
    a = Finite_field_instance.random()
    assert a.pow(1) == a


def test_pow_two_is_square(Finite_field_instance):
    a = Finite_field_instance.random()
    assert a.pow(2) == a * a


def test_pow_three(Finite_field_instance):
    a = Finite_field_instance.random()
    assert a.pow(3) == a * a * a


def test_pow_four(Finite_field_instance):
    a = Finite_field_instance.random()
    assert a.pow(4) == a.pow(2).pow(2)


def test_square(Finite_field_instance):
    a = Finite_field_instance.random()
    assert a.square() == a * a


def test_encoding_decoding(Finite_field_instance):
    r = Finite_field_instance.random()
    assert Finite_field_instance.of_be_bytes_opt(r.to_be_bytes()) == r
    assert Finite_field_instance.of_be_bytes_exn(r.to_be_bytes()) == r
