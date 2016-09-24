"""Simple async socket implementation.
"""
from socket import *
import types
import select

# Rename the original socket as _socket as we are going to write a new socket class
_socket = socket

class socket:
    """Simple async socket.
    """
    def __init__(self, family=AF_INET, type=SOCK_STREAM, *args):
        self._sock = _socket()
        self._sock.setblocking(0)

    def connect(self, addr):
        try:
            self._sock.connect(addr)
        except BlockingIOError:
            pass

    async def accept(self):
        await wait_for_read(self._sock)    
        client_sock, client_addr = self._sock.accept()
        return socket(client_sock), client_addr

    async def recv(self, size):
        await wait_for_read(self._sock)
        return self._sock.recv(size)        

    async def send(self, data):
        await wait_for_write(self._sock)
        return self._sock.send(data)

    async def sendall(self, data):
        while data:
            n = await self.send(data)
            data = data[n:]

    def __getattr__(self, name):
        return getattr(self._sock, name)

@types.coroutine
def wait_for_read(sock):
    while True:
        reads, writes, excs = select.select([sock], [], [], 0)
        if reads:
            break
        yield

@types.coroutine
def wait_for_write(sock):
    while True:
        reads, writes, excs = select.select([], [sock], [], 0)
        if writes:
            break
        yield
