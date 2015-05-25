#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import json

from Database import Database
from datetime import datetime

import time
import bottle

from Consts import Consts
from utility import Utility

__author__ = 'shenhailuanma'
__version__ = '0.1.0'


class InternalServer:
    def __init__(self, ip='0.0.0.0', port=9096 ,log_level=logging.DEBUG):


        self.ip   = ip
        self.port = port

        self.author  = __author__
        self.version = __version__

        self.file_path = os.path.realpath(__file__)
        self.dir_path  = os.path.dirname(self.file_path)

        # the database
        self.database = Database()

        self.utility = Utility()


        # mark system start time
        self.system_initialized = datetime.now()


        # set the logger
        self.log_level = logging.DEBUG
        self.log_path = 'Server.log'

        self.logger = logging.getLogger('Server')
        self.logger.setLevel(self.log_level)

        # create a handler for write the log to file.
        fh = logging.FileHandler(self.log_path)
        fh.setLevel(self.log_level)

        # create a handler for print the log info on console.
        ch = logging.StreamHandler()
        ch.setLevel(self.log_level)

        # set the log format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # add the handlers to logger
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        #################
        #API
        #################
        @bottle.route('/api0/create/license', method="POST")
        def api_create_license():
            response = {}
            response['result']  = 'error'
            response['license'] = ''

            try:
                self.logger.debug('handle a request: /api0/create/license ')   
                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))
                '''
                    {
                        "logo"   : "xxx",
                        "name"   : "xxx"
                    }
                '''
                post_data_json = json.loads(post_data)

                # check must params
                if not post_data_json.has_key('logo'):
                    response['result'] = 'error'
                    response['message'] = 'need param: logo.'
                    return "%s" %(json.dumps(response)) 

                if not post_data_json.has_key('name'):
                    response['result'] = 'error'
                    response['message'] = 'need param: name.'
                    return "%s" %(json.dumps(response)) 

                if not isinstance(post_data_json['logo'], basestring):
                    response['result'] = 'error'
                    response['message'] = 'The type error, the param: logo type should be string.'
                    return "%s" %(json.dumps(response)) 

                if not isinstance(post_data_json['name'], basestring):
                    response['result'] = 'error'
                    response['message'] = 'The type error, the param: name type should be string.'
                    return "%s" %(json.dumps(response)) 

                # create license by now time
                now = time.time() - 1430000000
                now *= 1000
            
                now = int(now)
                self.logger.debug('[api_create_license] base value:%s.' %(now))

                ret, code62 = self.utility.base62_encode(now)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'create license error:%s.' %(code62)
                    return "%s" %(json.dumps(response)) 
                else:
                    self.logger.debug('[api_create_license] license:%s.' %(code62))

                # create license
                post_data_json['license'] = code62
                ret,msg,license = self.database.db_create_license(post_data_json)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'create license error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 
                else:
                    self.logger.debug('create license ok, license:%s.' %(license))


                response['license'] = code62
                response['result'] = "success"
                return "%s" %(json.dumps(response)) 
            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 




    def run(self):
        bottle.run(host=self.ip, port=self.port, debug=True)

if __name__ == "__main__":
    server = InternalServer('0.0.0.0', 9096, logging.DEBUG)
    server.run()

else:
    #os.chdir(os.path.dirname(__file__))
    server = InternalServer('0.0.0.0', 9096, logging.DEBUG)
    application = bottle.default_app()