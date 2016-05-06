# coding=utf-8
__author__ = 'Yuheng Chen'

import urls
import constant
from Request.Request import Request
from Logger.Logger import testLogger
from Logger.Logger import baseLogger
import time
import json
import torndb
QUERY_REGION='SELECT * FROM iot_regionm  WHERE region_id =%s'
QUERY_DEV='SELECT * FROM iot_devm  WHERE dev_id =%s'
QUERY_SENSOR='SELECT * FROM iot_sensorm  WHERE sensor_id =%s'
INSERT_DATA = 'INSERT INTO iot_datam (date_time,data,sensor_id) VALUES (%s,%s,%s)'
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
            try:
                baseLogger.info(msg=("[Write_data_Handler]request.params is:",request.params))
                data=request.params['L']
                data_time = request.params['D']-3600*8
                data_date=time.strftime("%Y-%m-%d  %H:%M:%S",time.localtime(data_time))
                
                region=request.params['R']
                db_region = None

                dev=request.params['ID']
                db_dev = None

                sensor=request.params['SL']#This is a list
                db_sensor = None

                db = torndb.Connection(constant.DB_HOST,constant.DB_NAME,user=constant.DB_USER,password=constant.DB_PW)
                db_region = db.get(QUERY_REGION,region)
                if db_region ==None:
                    self.ext=False #exit client
                    self.res=json.dumps({'T':int(time.time()),'R':constant.R_INVALID})
                else:

                    db_dev = db.get(QUERY_DEV,region*256+dev)
                    if db_dev ==None:
                        self.ext=False
                        self.res=json.dumps({'T':int(time.time()),'R':constant.R_INVALID})
                    else:
                        if isinstance(sensor,list):
                            i=0
                            section_invalid = False
                            for s in sensor:
                                db_sensor=db.get(QUERY_SENSOR,region*(2**24)+dev*(2**16)+s)
                                if db_sensor ==None:
                                    self.ext=False
                                    self.res=json.dumps({'T':int(time.time()),'R':constant.R_INVALID})
                                else:
                                    db.insertmany(INSERT_DATA,[[data_date,data[i],db_sensor['id']]])
                                    section_invalid = True
                                    i=i+1

                            if section_invalid:
                                self.ext=True
                                self.res=json.dumps({'T':int(time.time()),'R':constant.R_DOK})
                db.close()
            except Exception as e:
                baseLogger.error(e.message)
                self.ext=False
                self.res=json.dumps({'T':int(time.time()),'R':constant.R_INVALID})

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
                self.res=json.dumps({'T':int(time.time()),'R':constant.R_PER})
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
            self.ext = False
            self.res=json.dumps({'T':int(time.time()),'R':constant.R_UNCONNECT})
        else:
            raise TypeError 