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

# Generators (2)


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

## Coroutines

    !py3
    def abc():                   def xyz():     
        print("A")                   print("X")
        yield                        yield
        print("B")                   print("Y")
        yield                        yield
        print("C")                   print("Z")
        yield                        yield  


    def main():
        g1 = abc()
        g2 = xyz()

        next(g1); next(g2)
        next(g1); next(g2)
        next(g1); next(g2)

Output:

    A
    X
    B
    Y
    C
    Z

--- 
## Coroutines


    !py3
    def display(values):
        for v in values:
            print(v)
            yield

    def interweave(generators):
        while True:
            for g in generators:
                yield next(g)
                 
    def run_all(generators):
        for x in interweave(generators):
            pass

    def main():
        run_all([display("ABC"), display("123")])


Output:
    
    A
    1
    B
    2
    C
    3

---
### Earlier Limitations

The implementation of generators until Python 3.3 had the following limitations.

It was not possible to:

* delegate control to a sub-generator
* return a value from a generator

--- 
### Delegate control to a sub-generator

    !py3
    def display2(values1, values2):
        """This doesn't work"""
        display(values1)
        display(values2)


The new construct `yield from` was introduced to sovle this:

    !py3
    def display2(values1, values2):
        yield from display(values1)
        yield from display(values2)

---

### Returning a value from a generator

    !py3
    def square(x):
        """Computes square of a numnber using square microservice.
        """
        response = send_request("http://square.io/", x=x)

        # It'll take a while to get the response data,
        # something else can run in the meanwhile.
        yield

        return response.json()['result']

Support for returning values from generators was added in Python 3.3.

 
    !py3
    def sum_of_squares(x, y):
        x2 = yield from square(x)
        y2 = yield from square(y)
        return x2 + y2
