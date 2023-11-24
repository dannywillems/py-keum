# py-keum

**This is a work in progress**

Keum is a modular implementation of cryptographic components which can be used
as a toolbox to bootstrap projects and experimentations. It is not supposed to
be used in production!
It is inefficient and not audited (and will never be).

For instance, keum includes (or will include):
- Finite field implementation
- Elliptic curve operations in different forms (Edwards, Montgomery,
  Weierstrass) and different coordinates (affine, jacobian, projective)
- Arithmetisation oriented hash functions (Poseidon, Griffin, Anemoi, Rescue)

The generic primitives are instantiated with standard parameters. For instance, the following elliptic curves are currently supported:
- [pallas](./keum/pallas.py)
- [vesta](./keum/vesta.py)
- [grumpkin](./keum/grumpkin.py)
- [tweedledee](./keum/tweedledee.py)
- [tweedledum](./keum/tweedledum.py)
- [secp256k1](./keum/secp256k1.py)
- [secp256r1](./keum/secp256r1.py)
- [bn254](./keum/bn254.py)

## API

### Finite fields

For a more complete documentation, have a look at [ff.py](./keum/ff.py).

```python
from keum import PrimeFiniteField

# Instantiate a finite field is easy as creating a subclass of PrimeFiniteField and define the class attribute ORDER to the actual order of the prime finite field
class F13(PrimeFiniteField):
    ORDER = 13

# generate random values
a = F13.random()
b = F13.random()

# add two field element
a + b
```

### Elliptic curves

For a more complete documentation, have a look at [ec.py](./keum/ec.py).

The following curves are currently supported:
- [pallas](./keum/pallas.py)
- [vesta](./keum/vesta.py)
- [grumpkin](./keum/grumpkin.py)
- [tweedledee](./keum/tweedledee.py)
- [tweedledum](./keum/tweedledum.py)
- [secp256k1](./keum/secp256k1.py)
- [secp256r1](./keum/secp256r1.py)
- [bn254](./keum/bn254.py)


```python
from keum import pallas

# generate random values
p1 = pallas.AffineWeierstrass.random()
p2 = pallas.AffineWeierstrass.random()

# add two points
p1 + p2
```
