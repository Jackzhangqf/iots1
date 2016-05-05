# coding=utf-8
__author__ = 'Yuheng Chen'

from Request.Request import Request
import Handler.Handler
from Logger.Logger import baseLogger
from Handler.Handler import BaseHandler
import urls
from tornado.iostream import StreamClosedError
import constant
import json
import constant
import time

_TIME_OUT=200
class Connection(object):
    '''
    Connection is the base Class for server and client communication.
    Each connection between Server and client-server will be
    maintained by a `Connection` instance.
    Connection will read the request from IOStream and handle
    the requests.
    When a request handling is over, the Connection will automatically
    read the stream to get the next request.
    '''

    clients = set()

    def __init__(self, stream, address):
        Connection.clients.add(self)

        self._stream = stream
        self._address = address
        self._stream.set_close_callback(self.on_close)
        self.read_request()
        baseLogger.info(msg=("New Connection from server: ",address))
        self.is_permission = False
        self.bao_count = 0
        self.start=False
        baseLogger.info(msg=("Now Clients count is : ",len(Connection.clients)))



        self.timeout = None
        self.io_loop = self._stream.io_loop
        
    def set_timeout(self,timeout):
        self.timeout = self.io_loop.add_timeout(self.io_loop.time() + timeout,
                                                self.on_timeout)

    def on_timeout(self):
        self.timeout = None
        baseLogger.info("Timeout!")
        self._stream.close()
    def clear_timeout(self):
        if self.timeout is not None:
            self.io_loop.remove_timeout(self.timeout)



    def read_request(self):
        try:
            self._stream.read_until('\n', self.handle_request)
        except StreamClosedError:
            pass

    def handle_request(self, data):
        tmp_body = data[:-1]
        self.clear_timeout()
        if self.bao_count==0:
            try:
                tmp_json = json.loads(tmp_body)

                if tmp_json.has_key('F'):
                    if tmp_json['F']==constant.START_CMDID:
                        self.start=True      
                        baseLogger.info(msg=("First : ",tmp_json['F']))
                if tmp_json.has_key('J'):
                    if tmp_json['J']==0 and tmp_json["F"]==constant.LOGIN_CMDID:
                        self.start=True
                        baseLogger.info(msg=("Second: ",tmp_json['F']))
            except Exception, e:
                baseLogger.error(e.message)

        if self.is_permission or self.start:
            self.start=False
            request = Request(address=self._address, Body=tmp_body)
            handler = urls.Handler_mapping.get(request.cmdid)
            handler_instance = handler()
            if isinstance(handler_instance,BaseHandler):
                try:
                    handler_instance.process(request=request)
                    self._stream.write(handler_instance.res)

                    if self.bao_count==0 and request.cmdid==constant.LOGIN_CMDID:
                        self.is_permission=handler_instance.ext
                       
 
                    if handler_instance.ext and (not request.cmdid ==constant.START_CMDID):
                        #Here can bijiao

                        #-------------------
                        if not request.cmdid == constant.HEART_BEAT_CMDID:
                            baseLogger.info(self.bao_count)
                            self.bao_count=self.bao_count+1
                        else:
                            baseLogger.info("Beat!")
                        
 
                    if not handler_instance.ext:
                        self._stream.close()
                except Exception as e:
                    baseLogger.error(e.message)
                    self._stream.close()

                self.read_request()
        else:
            self._stream.write(json.dumps({'T':int(time.time()),'R':constant.R_INVALID}))
            baseLogger.info(msg=("This client is",self._address))
            self._stream.close()
        self.set_timeout(_TIME_OUT)
    def on_close(self):
        baseLogger.info(msg=("Server connection has been closed: ", self._address))
        Connection.clients.remove(self)
