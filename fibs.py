def gen_fibs():
    """Generates sequence of fibbonacci numbers.
    """
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b

def first(seq):
    """Returns the first element of a sequence.
    """
    return next(iter(seq))

def last(seq):
    """Returns the last element of a sequence.
    """
    for x in seq:
        pass
    return x

def take(n, seq):
    """Takes first n elements of a sequence.
    """
    seq = iter(seq)
    return (next(seq) for i in range(n))

def nth(n, seq):
    """Returns n'th element of a sequence.
    """
    return last(take(n, seq))    

def upto(upperbound, seq):
    """Returns elements in the sequence until 
    they are less than upper bound.
    """
    for x in seq:
        if x > upperbound:
            break
        yield x

def count(seq):
    """Counts the number of elements in a sequence."""
    return sum(1 for x in seq)        



