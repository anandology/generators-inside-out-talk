slidenumbers: true
footer: PyCon India 2016

# [fit] Generators Inside Out
---

# About Me

Anand Chitipothu
Software Consultant & Trainer

@anandology
http://anandology.com/

![left](images/anand-speaking2.png)

---

# What is this talk about?

* Iterators
* Generators
* Coroutines
* Async
* Async IO

---

# [fit] How does *iteration* work?

---

# Iterating over a list

```python
for x in [1, 2, 3, 4]:
    print(x) 
```

```
-------------------------------------------------------
```

```python
1
2
3
4
```
---

# Iterating over a string

```python
for c in "hello":
    print(c)
```

```
-------------------------------------------------------
```

```python
h
e
l
l
o
```

---

# Iterating over a dictionary

```python
for k in {"x": 1, "y": 2, "z": 3}:
    print(k)
```

```
-------------------------------------------------------
```

```python
y
x
z
```

---

# The Iteration Protocol

```python
>>> x = iter(["a", "b", "c"])

>>> next(x)
'a'
>>> next(x)
'b'
>>> next(x)
'c'
>>> next(x)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
StopIteration
```

---

# win!

```python
# Largest word in the dictionary
>>> max(open('/usr/share/dict/words'), key=len)
'formaldehydesulphoxylate\n'
```

---

# Generators

---

# What is a generator? 

```python
def squares(numbers):
    for n in numbers:
        yield n*n
```

```
-------------------------------------------------------
```


```python
>>> for x in squares([1, 2, 3]):
...     print(x)
1
4
9
```

---

Let me add some prints to understand it better.

```python
def squares(numbers):
    print("BEGIN squares")
    for n in numbers:
        print("Computing square of", n)
        yield n*n
    print("END squares")
``` 


```
-------------------------------------------------------
```

```python
>>> sq = squares([1, 2, 3])
>>> sq
<generator object squares at 0xb6c73720>
```

---

```python
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
```
---

```python
>>> for x in squares([1, 2, 3]):
...     print(x)
BEGIN squares
Computing square of 1
1
Computing square of 2
4
Computing square of 3
9
END squares
```

---

# [fit] Example: Fibbonacci Numbers

---
Write a program to find $$n^{th}$$  fibbonacci number.

```python
def fibn(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibn(n-1) + fibn(n-2)
```        

```
-------------------------------------------------------
```

```python
>>> fibn(10)
55
```


---

Write a program to compute first n fibbonacci numbers.

```python
def fibs(n):
    result = []
    a, b = 1, 1
    for i in range(n):
        result.append(a)
        a, b = b, a+b
    return result
```

```
-------------------------------------------------------
```

```python
>>> fibs(10)
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
```

---

What is the largest fibbonacci number below one million?

```python
def largest_fib(upperbound):
    a, b = 1, 1
    while b < upperbound:
        a, b = b, a+b
    return a
```
```
-------------------------------------------------------
```

```python
>>> largest_fib(1000000)
832040
```

---

## Issue

Three different implementations to compute fibbonacci numbers!

---

## The generator-based solution

```python
def gen_fibs():
    """Generates sequence of fibbonacci numbers.
    """
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a + b
```

---

Let's write some generic generator utilities. 

```python
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
```

---

```python
def take(n, seq):
    """Takes first n elements of a sequence.
    """
    seq = iter(seq)
    return (next(seq) for i in range(n))

def nth(n, seq):
    """Returns n'th element of a sequence.
    """
    return last(take(n, seq))    
```

---

```python
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
```

---

```python
# what is 10th fibbonacci number?
>>> nth(10, gen_fibs())
55

# find first 10 fibbinacci numbers
>>> list(take(10, gen_fibs()))
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

# find all fibbonacci numbers below 100
>>> list(upto(100, gen_fibs())
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
```

---

```python
# What is the largest fibbonacci number 
# below one million?
>>> last(upto(1000000, gen_fibs()))
832040

# How many fibbonacci numbes are there 
# below one million?
>>> count(upto(1000000, gen_fibs()))
30
```

---

# [fit] Building data pipelines

---
```python
import os

def find(root): 
    """Finds all the files in the given 
    directory tree.
    """
    for path, dirnames, filenames in os.walk(root):
        for f in filenames:
            yield os.path.join(path, f)
```
---

```python
def readlines(paths):
    """Returns a generator over lines in
    all the files specified.
    """
    for path in paths:
        yield from open(path)
```

---

```python
def grep(pattern, lines):
    """Returns only the lines that 
    contain given pattern.
    """
    return (line for line in lines 
                 if pattern in line)
```

---

```python
def main(): 
    # find all files in the project
    filenames = find("project")  

    # pick only python files
    filenames = grep('.py', filenames)

    # read all the lines
    lines = readlines(filenames)

    # pick only function definitions
    lines = grep('def ', lines)

    # count the total number of functions in your project
    print(count(lines))
```

---

# Coroutines

---

Let's look at this strange example:

```python
def display(values):
    for v in values:
        print(v)
        yield

def main():
    g1 = display("ABC")
    g2 = display("123")

    next(g1); next(g2)
    next(g1); next(g2)
    next(g1); next(g2)

```

---

```
>>> main()
A
1
B
2
C
3
```
---

Slightly generalized.

```python
def run_all(generators):
    # Runs all the generators concurrently
    # stop when any one of them stops
    try:
        while True:
            for g in generators:
                next(g)
    except StopIteration:
        pass

def main2():
    g1 = display("ABC")
    g2 = display("123")
    run_all([g1, g2])
```

---

```
>>> main2()
A
1
B
2
C
3
```

--- 

How about writing a function to print two sets of values?

```python
def display2(values1, values2):
    # WARNING: this doesn't work
    display(values1)
    display(values2)
```

---

```python
def display2(values1, values2):
    yield from display(values1)
    yield from display(values2)

def main3():
    g1 = display2("ABC", "XYZ")
    g2 = display2("...", "...")
    run_all([g1, g2])
```

---

```python
>>> main3()
A
.
B
.
C
.
X
.
Y
.
Z
.
```
---

Let's try to build a simple concurrency library based on coroutines.

```python
from collections import deque
_tasks = deque()

def run(task):
    _tasks.append(task)
    run_all()

def spawn(task):
    _tasks.appendleft(task)
    yield
```

---

```python

def run_all():
    while _tasks:
        task = _tasks.popleft()
        try:
            next(task)
        except StopIteration:
            pass
        else:
            _tasks.append(task)
```

---

## Returning a value from a generator

```python
def square(x):
    """Computes square of a number using
    square microservice.
    """
    response = send_request("/api/square", number=x)
    
    # Let something else run while square is being computed.
    yield
    
    return response.json()['result']
```
---

```python
def sum_of_squares(x, y):
    x2 = yield from square(x)
    y2 = yield from square(y)
    return x2 + y2
```
---

# Generators are overloaded

* Used to build and process data streams
* Also used as coroutines

Confusing!

---

# Native Coroutines

---

```python
async def square(x):
    return x*x

async def sum_of_squares(x, y):
    x2 = await square(x)
    y2 = await square(y)
    return x2+y2
```
---

## Coroutine Protocol

```python

>>> square(4)
<coroutine object square at 0xb57a6510>

>>> x = square(4)
>>> x.send(None)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  StopIteration: 16
```

--- 

# Running Coroutines

```python
def run(coroutine):
    try:
        while True:
            coroutine.send(None)
    except StopIteration as e:
        return e.value
```

```
-------------------------------------------------------
```

```python
>>> run(square(4))
16
```

---
## Generator-based coroutines

```python
import types

@types.coroutine
def aprint(x):
    print(x)
    yield
```

---

```python
async def display(values):
    for v in values:
        await aprint(v)
```

```
-------------------------------------------------------
```

```python
>>> run(display("ABC"))
A
B
C
```

---
# Coroutine Library

---
```python
"""coro.py - a simple coroutine conncurrency library.
"""
import types
from collections import deque

_tasks = deque()

def run(task):
    _tasks.append(task)
    run_all()

@types.coroutine
def spawn(task):
    _tasks.appendleft(task)
    yield
```

---

```python
def run_all():
    while _tasks:
        task = _tasks.popleft()
        try:
            task.send(None)
        except StopIteration: 
            pass
        else:
            _tasks.append(task)
```

---

# Async Example

```python
from coro import spawn, run
import types

@types.coroutine
def aprint(x):
    print(x)
    yield
```

---

```python
async def display(values):
    for v in values:
        await aprint(v)
 
async def main():
    await spawn(display("ABC"))
    await spawn(display("123"))    
    
if __name__ == "__main__":
    run(main())
```

---

Output:

```
A
1
B
2
C
3
```
---

# Async IO?

--- 

```python
"""asocket - simple async socket implementation.
"""
from socket import *
import types
import select

# Rename the original socket as _socket as 
# we are going to write a new socket class
_socket = socket
```

---

```python
class socket:
    """Simple async socket.
    """
    def __init__(self, *args):
        self._sock = _socket(*args)
        self._sock.setblocking(0)

    def __getattr__(self, name):
        return getattr(self._sock, name)            
```

---
```python

    def connect(self, addr):
        try:
            self._sock.connect(addr)
        except BlockingIOError: pass

    async def send(self, data):
        await wait_for_write(self._sock)
        return self._sock.send(data)        

    async def recv(self, size):
        await wait_for_read(self._sock)
        return self._sock.recv(size)
```
---
```python
@types.coroutine
def wait_for_read(sock):
    while True:
        r, w, e = select.select([sock], [], [], 0)
        if r: break
        yield

@types.coroutine
def wait_for_write(sock):
    while True:
        r, w, e = select.select([], [sock], [], 0)
        if w: break
        yield
```

---
# Async IO Example
```python
from asocket import *
from coro import spawn, run

async def echo_client(host, port, label):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect((host, port))

    for i in range(3):
        await sock.send(str(i).encode('ascii'))
        data = await sock.recv(1024)
        print(label, data.decode('ascii'))
```
---
```python
async def main():
    host, port = 'localhost', 1234
    await spawn(echo_client(host, port, 'A'))
    await spawn(echo_client(host, port, 'B'))
    await spawn(echo_client(host, port, 'C'))
    await spawn(echo_client(host, port, 'D'))

if __name__ == "__main__":
    run(main())
```

---
```
$ python echo_client.py
B 0
A 0
D 0
C 0
B 1
B 2
A 1
D 1
C 1
A 2
D 2
C 2
```

--- 

# Summary

Generators are awesome. 
Use them for everything!

Coroutines are good vehicles for concurrency. 
Explore them more!

^ Generators are elegant. They often lead to more reusability. You can build data pipelines easily with generators.

^ Coroutines are still very new. 

---
# Questions?

Anand Chitipothu
@anandology

http://bit.ly/pygen0