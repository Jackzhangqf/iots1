# coding=utf-8
__author__ = 'Qifang Zhang'

import json
import time
from Logger.Logger import baseLogger
import constant

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
        self.cmdid = None
        self.timestamp = int(time.time())
        self.params = dict()
        self.way = None
        self.ver = None
        try:
            data = json.loads(self.rawBody)#create a dict
        except:
            baseLogger.info(msg=("[Request]:RawData format is error data :",rawBody))
            self.cmdid = constant.INVALID_CMDID
        

        if data.has_key('F'):
            self.cmdid = int(data['F'])
        if data.has_key('T'):
            self.timestamp = int(data['T'])
        if data.has_key('P'):
            self.params = data['P']
        if data.has_key('V'):
            self.ver = data['V']
        if data.has_key('C'):
            self.way = int(data['C'])

    def serialization(self):
        '''
        used for serialization storage
        :return: a string value represents the reqeust
        '''
        tmp = {'address': self.address, 'body': self.rawBody}
        return json.dumps(tmp)
