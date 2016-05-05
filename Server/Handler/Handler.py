# coding=utf-8
__author__ = 'Yuheng Chen'

import urls
import constant
from Request.Request import Request
from Logger.Logger import testLogger
from Logger.Logger import baseLogger
import time
import json

class BaseHandler(object):
    '''
    Base Class for Handler.
    You can custom your db connections or logger here.
    '''
    res = None

    def process(self,request):
        '''
        This method needs to be overridden.
        If not, raise `NotImplementedError`
        '''
        raise NotImplementedError

@urls.handler(constant.TEST_CMDID)
class TestHandler(BaseHandler):

    TAG = 'TestHandler'

    def process(self,request):
        if isinstance(request, Request):
            testLogger.info(request.params)
            self.ext=True
            self.res = "{'code':0}"
        else:
            raise TypeError

@urls.handler(constant.SEND_DATA_CMDID)
class Write_data_Handler(BaseHandler):

    TAG = 'Write_data_Handler'

    def process(self,request):
        if isinstance(request, Request):
            
            '''add handler
            '''
            self.ext=True
            self.res=json.dumps({'T':int(time.time()),'R':constant.R_DOK})
            sl= request.params['SL']
            baseLogger.info(msg=("[Write_data_Handler]:sensor list is :",sl))
        else:
            raise TypeError

@urls.handler(constant.INVALID_CMDID)
class Invalid_Handler(BaseHandler):
	
    TAG = 'Invalid_Handler'

    def process(self, request):
        if isinstance(request,Request):
                
            '''add handler
            '''
            self.ext = False
            self.res=json.dumps({'T':int(time.time()),'R':constant.R_INVALID})
        else:
            raise TypeError 

@urls.handler(constant.LOGIN_CMDID)
class Login_Handler(BaseHandler):
    
    TAG = 'Login_Handler'
    def process(self, request):
        if isinstance(request,Request):
    
            '''add handler
            '''
            if request.params.has_key('U'):
                user = request.params['U']
                baseLogger.info(msg=("[Login_Handler]:Welcome to IoT:",user))
                self.ext = True
                self.res=json.dumps({'T':int(time.time()),'R':constant.R_POK})
            else:
                self.ext = False
                self.res=json.dumps({'T':int(time.time()),'R':constant.R_INVALID})
        else:
            raise TypeError 

@urls.handler(constant.LOGOUT_CMDID)
class Logout_Handler(BaseHandler):
    
    TAG = 'Logout_Handler'

    def process(self, request):
        if isinstance(request,Request):
                
            '''add handler
            '''
            self.ext = False
            self.res=json.dumps({'T':int(time.time()),'R':constant.R_OK})
        else:
            raise TypeError 

@urls.handler(constant.START_CMDID)
class Start_Handler(BaseHandler):
    
    TAG = 'Start_Handler'

    def process(self, request):
        if isinstance(request,Request):
                
            '''add handler
            '''
            self.ext = True
            self.res=json.dumps({'T':int(time.time()),'R':constant.R_CONNECT  })
        else:
            raise TypeError 


@urls.handler(constant.HEART_BEAT_CMDID)
class Heart_beat_Handler(BaseHandler):
    
    TAG = 'Heart_beat_Handler'

    def process(self, request):
        if isinstance(request,Request):
                
            '''add handler
            '''
            self.ext = True
            self.res=json.dumps({'T':int(time.time()),'R':constant.R_BEAT})
        else:
            raise TypeError 

@urls.handler(constant.LOGOUT_CMDID)
class Logout_Handler(BaseHandler):
    
    TAG = 'Logout_Handler'

    def process(self, request):
        if isinstance(request,Request):
                
            '''add handler
            '''
            self.ext = True
            self.res=json.dumps({'T':int(time.time()),'R':constant.R_UNCONNECT})
        else:
            raise TypeError 