# coding=utf-8
__author__ = 'Yuheng Chen'

import json
import time


class Request(object):
    '''
    `Request` is the basic object type in the IOStream.
    Each `Request` is delimited by a delimiter '\n'.
    `Request` transported in a serialization mode, using normal json type.

    To extend `Request`, define a subclass and there is no need to override anything.

    `Request` has following parameters:

    1.`address`:simple ip address combined with port number representing
                the request origin server.

    2.`rawBody`:raw content of the request body

    3.`cmdid`:command id defines in Command

    4.`timestamp`:the date when request was sent

    5.`params`:a dict that storage all the data it takes
    '''

    def __init__(self, address=None, Body=None):
        self.address = address

        if not Body:
            self.rawBody = '{}'
        else:
            self.rawBody = Body

        data = eval(self.rawBody)#create a dict
        self.cmdid = None
        self.timestamp = int(time.time())
        self.params = dict()
	self.way = None
	self.type = None

        if data.has_key('C'):
            self.cmdid = int(data['C'])
        if data.has_key('timestamp'):
            self.timestamp = int(data['timestamp'])
        if data.has_key('D'):
            self.params = data['D']
	if data.has_key('T'):
	    self.type = int(data['T'])
	if data.has_key('W'):
	    self.way = int(data['W'])

    def serialization(self):
        '''
        used for serialization storage
        :return: a string value represents the reqeust
        '''
        tmp = {'address': self.address, 'body': self.rawBody}
        return json.dumps(tmp)
