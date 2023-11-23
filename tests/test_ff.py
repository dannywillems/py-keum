import pytest
from keum import FiniteField, PrimeFiniteField


class F13(PrimeFiniteField):
    ORDER = 13


class F17(PrimeFiniteField):
    ORDER = 17


@pytest.fixture(params=[F13, F17])
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


def test_cannot_multiply_when_different_fields():
    a = F13.random()
    b = F17.random()
    with pytest.raises(ValueError):
        a * b


# TODO
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


# def test_inverse_twice(Finite_field_instance):
#     a = Finite_field_instance.random()
#     assert a.inverse().inverse() == a


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
