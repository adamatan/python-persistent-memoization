import random
from memoize.memoize import Memoize

@Memoize()
def get_random():
    return random.random()

@Memoize()
def get_random_with_args(n):
    return random.random() + n

@Memoize()
def get_random_with_kwargs(n=0):
    return random.random() + n

def test_basic_memoization():
    assert get_random() == get_random()

def test_args_memoization():
    assert get_random_with_args(1) == get_random_with_args(1)
    assert get_random_with_args(1) != get_random_with_args(2)

def test_kwargs_memoization():
    assert get_random_with_kwargs(n=5) == get_random_with_kwargs(n=5)
    assert get_random_with_kwargs(n=5) != get_random_with_kwargs(n=6)
