# coding=utf-8
__author__ = 'Yuheng Chen'

from tornado.tcpserver import TCPServer
from Connection.Connection import Connection
_START_TIMEOUT=3

class BaseServer(TCPServer):
    '''
    base type of TCPServer that override handle_stream method here
    in order to maintain the connection between servers
    through IOStream.
    '''

    def handle_stream(self, stream, address):
        con=Connection(address=address, stream=stream)
        con.set_timeout(_START_TIMEOUT)

        