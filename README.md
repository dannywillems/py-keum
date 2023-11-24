# py-keum

Modular elliptic curve library in Python. Do not use in production.

## API

### Finite fields

For a more complete documentation, have a look at [ff.py](./keum/ff.py).

```python
from keum import PrimeFiniteField

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

```python
from keum import pallas

# generate random values
p1 = pallas.AffineWeierstrass.random()
p2 = pallas.AffineWeierstrass.random()

# add two points
p1 + p2
```
