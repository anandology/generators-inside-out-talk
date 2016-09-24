"""Simple coroutine conncurrency library.
"""
from collections import deque
import types

_tasks = deque()

@types.coroutine
def spawn(task):
    _tasks.appendleft(task)
    yield

def run(task):
    _tasks.append(task)
    run_all()

def run_all():
    while _tasks:
        task = _tasks.popleft()
        try:
            task.send(None)
        except StopIteration:
            pass
        else:
            _tasks.append(task)
