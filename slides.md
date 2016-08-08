# Async IO From Group Up

---

# What is "async"?

---

## Synchronous - blocking

[cartoon will come here]

- X visits Bangalore Iyengar Bakery
- Orders a veg puff
- waits until it is ready 
- takes it and walks away

---

## Asynchronous - callback

[Cartoon will come here]

- X visits Starbucks
- Orders black coffee
- Sits and reads about asyncio
- The bartista calls his name and gives his coffee

---

## Async - callback style programming

    !javascript
    // node.js application to download a URL
    var http = require('http');

    function wget(url, callback) {
        http.get(url, function (response) {
            var data = '';

            response.setEncoding('utf8');

            response.on('data', function(chunk) {
                data += chunk;
            }).on('end', function() {
                callback(data);
            });
        });
    }

---

## Async - python with yield

    !python3
    import asyncio
    import aiohttp

    @asyncio.coroutine
    def wget(url):
        with aiohttp.ClientSession() as client:
            response = yield from client.get(url)
            data = yield from response.text()
            return data


---
## Async - python with async/await

    !py3
    import asyncio
    import aiohttp

    async def wget(url):
        with aiohttp.ClientSession() as client:
            response = await client.get(url)
            data = await response.text()
            return data

---

# How does that work?

---

# Async <strike>IO</strike> from Ground Up

---

# Outline

* Generators
* Coroutines
* Event Loops
* `async` and `await`

---

# Generators

---

# Generators - Example

    !py3
    def squares(numbers):
        for n in numbers:
            yield n*n


Lets try it out:


    !py3
    >>> for x in squares([1, 2, 3, 4]):
    ...     print(x)
    1
    4
    9
    16

---

# Generators - Example (2)


    !py3
    def squares(numbers):
        print("BEGIN squares")
        for n in numbers:
            print("Computing square of", n)
            yield n*n
        print("END squares")
 

Lets try it out:


    !py3
    >>> sq = squares([1, 2, 3])
    >>> sq
    <generator object squares at 0xb6c73720>
    >>> next(sq)
    BEGIN squares
    Computing square of 1
    1
    >>> next(sq)
    Computing square of 2
    4
    >>> next(sq)
    Computing square of 3
    9
    >>> next(sq)
    END squares
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      StopIteration

---

## Generators - Another Example

    !py3
    def fibs():
        """Generates fibbonacci numbers"""
        a, b = 1, 1
        while True:
            yield a
            a, b = b, a+b

    def take(n, seq):
        """Returns first n numbers of the given sequence."""
        seq = iter(seq)
        return (next(seq) for i in range(n))
	

First 10 fibbonacci numbers.

    !py3
    >>> list(take(10, fibs()))
    [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

Sum of first 100 fibbonacci numbers.

    !py3
    >>> sum(take(100, fibs()))
    927372692193078999175

---

### Generators - Another example

    !py3
    def first(seq):
        """Returns the first element of the given sequence."""
        return next(iter(seq))

    def last(seq):
        """Returns the last element of the given sequence."""
        x = None
        for x in seq:
            pass
        return x

    def nth(seq, n):
        """Returns the n'th element of the given sequence."""
        return last(take(n, seq))

What is the 100th fibbonacci number?

    !py3
    >>> nth(fibs(), 100) 
    354224848179261915075

---

### Generators - Another example

    !py3
    import itertools
    def take_until(seq, upperbound):
        """Returns all values of the given sequence until 
        those values are less than given bound."""
        return itertools.takewhile(lambda n: n < upperbound, seq)

    def count(seq):
        """Counts the number of elements in a sequence.
        """
        return sum(1 for x in seq)


What is the largest fibbonacci number less than one million?

    !py3
    >>> last(take_until(fibs(), 1000000))
    832040

Count the number of fibbonacci numbers which are below one million?

    !py3
    >>> count(take_until(fibs(), 1000000))
    30

---
### Generators: Deligating to subgenerators

    !py3
    def inorder(node):
        if node is None:
            return

       for n in inorder(left_child(node)):
           yield n

        yield node

       for n in inorder(right_child(node)):
           yield n

---

### Generators: Deligating to subgenerators

New syntax `yield from` is added to Python in version 3.3.

    !py3
    def inorder(node):
        if node is None:
            return

        yield from inorder(left_child(node))
        yield node
        yield from inorder(right_child(node))

---
### Generators: Summary

- Lazy evaluation
- Better program organization
- More reusability

---

# Coroutines

---
### Running generators concurrently - v1

    !py3
    def interweave(generators):
        while True:
            for g in generators:
                yield next(g)
                 
    def run_all(generators):
        for x in interweave(generators):
            pass

Lets try:
    
    
    >>> g1 = squares([1, 2, 3, 4])
    >>> g2 = squares([10, 20, 30, 40])
    >>> run_all([g1, g2])
    Computing square of 1
    Computing square of 10
    Computing square of 2
    Computing square of 20
    Computing square of 3
    Computing square of 30
    Computing square of 4
    Computing square of 40


