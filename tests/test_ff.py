import pytest
from keum import FiniteField, PrimeFiniteField


class F13(PrimeFiniteField):
    ORDER = 13


@pytest.fixture
def Finite_field_instance():
    return F13


# TODO
def test_cannot_divide_when_different_fields(
    Finite_field_instance1, Finite_field_instance2
):
    # TODO
    pass


# TODO
def test_cannot_substract_when_different_fields(
    Finite_field_instance1, Finite_field_instance2
):
    # TODO
    pass


# TODO
def test_cannot_add_when_different_fields(
    Finite_field_instance1, Finite_field_instance2
):
    # TODO
    pass


# TODO
def test_cannot_multiply_when_different_fields(
    Finite_field_instance1, Finite_field_instance2
):
    # TODO
    pass


# TODO
def test_cannot_divide_by_zero(Finite_field_instance):
    x = Finite_field_instance.random()
    # Check exception raised
    x / 0


def test_addition_commutative(Finite_field_instance):
    a = Finite_field_instance.random()
    b = Finite_field_instance.random()
    assert a + b == b + a

def test_addition_associativity(Finite_field_instance):
    a = Finite_field_instance.random()
    b = Finite_field_instance.random()
    c = Finite_field_instance.random()
    return a + (b + c) == (a + b) + c


def test_distributivity(Finite_field_instance):
    a = Finite_field_instance.random()
    b = Finite_field_instance.random()
    c = Finite_field_instance.random()
    return a * (b + c) == a * b + a * c


def test_multiplication_commutative(Finite_field_instance):
    a = Finite_field_instance.random()
    b = Finite_field_instance.random()
    assert a * b == b * a


def test_inverse_twice(Finite_field_instance):
    a = Finite_field_instance.random()
    assert a.inverse().inverse() == 0


def test_one_is_identity_for_multiplication(Finite_field_instance):
    r = Finite_field_instance.random()
    return r * Finite_field_instance.one() == r


def test_zero_is_identity_for_addition(Finite_field_instance):
    r = Finite_field_instance.random()
    return r + Finite_field_instance.zero() == r
