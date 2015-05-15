#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import json


from datetime import datetime

import bottle

#from bottle import route, run, template, error, static_file, default_app



__author__ = 'shenhailuanma'
__version__ = '0.1.0'


class Server:
    def __init__(self, ip='0.0.0.0', port=9090 ,log_level=logging.DEBUG):

        self.ip   = ip
        self.port = port

        self.author  = __author__
        self.version = __version__


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

        # init the schools data
        if os.path.exists('juniorschool.json'):
            self.schools_json = json.load(file('juniorschool.json'))
            '''
                schools_json format:
                {
                    "version": "1.0.1",
                    "schools": [
                        {
                            "id": "1101",
                            "name": "北京",
                            "data" : [
                                {
                                    "name": "东城区",
                                    "schoollist": ["北京一七一中", "北京一六四中", "地安门中学", "北京二中亦庄学校", "和平北路学校"],
                                    "id": "city_qu_110101"
                                },
                                ......
                                {

                                }
                            ]
                        },
                        ......    
                        {

                        }
                    ]

                }
            '''
        else:
            self.schools_json = {}


        self.logger.info('init over.')

    



        #######  web test ######
        @bottle.route('/')
        @bottle.route('/index')
        def index():
            return "Hello, this is biubiuServer2."

        @bottle.error(404)
        def error404(error):
            return "Nothing here, sorry."

        @bottle.route('/images/:filename')
        def send_image(filename=None):
            # FIXME: the param 'root' should be define in other place, now just for test.
            return bottle.static_file(filename, root='../images')

        #################
        #API
        #################
        @bottle.route('/api/gettime')
        def gettime():
            return "%s" %(datetime.now())

        @bottle.route('/api/get/schools/:number')
        def get_schools(number=None):
            '''
                Get schools info by area code.
                The area code can get more info by http://www.stats.gov.cn/tjsj/tjbz/xzqhdm/
                The area code is defined with 6 number, 
                    e.g: 430104, the 43 means hunan, 4301 means changsha, 430104 means yueluqu.
            '''
            
            response = {}
            response['result'] = 'error'
            response['schools'] = []

            try:

                self.logger.debug('[get_schools] The number:%s, type:%s.' %(number,type(number)))
                if not isinstance(number,basestring):
                    response['message'] = "The number type error."
                    return "%s" %(json.dumps(response))

                # parse the area code
                if len(number)==2:
                    province_code = number
                    city_code = ""
                    county_code = ""

                elif len(number)==4:
                    province_code = number[:2]
                    city_code = number[2:4]
                    county_code = ""

                elif len(number)==6:
                    province_code = number[:2]
                    city_code = number[2:4]
                    county_code = number[4:6]
                else:
                    response['message'] = "The area code's length should be 2,4 or 6."
                    return "%s" %(json.dumps(response))

                self.logger.debug('[get_schools] province_code:%s, city_code:%s, county_code:%s.' %(province_code,city_code,county_code))    


                # get the school info
                for city_one in self.schools_json['schools']:
                    if city_one['id'][:2] == province_code:
                        if city_code == "" or city_code == city_one['id'][2:4]:
                            for county_one in city_one['data']:
                                if county_code == "" or county_code == county_one['id'][-2:]:
                                    
                                    for school_one in county_one['schoollist']:
                                        school_json = {}
                                        #FIXME: school id shoud be define
                                        school_json['id'] = "%s" %(county_one['id'][-6:])
                                        school_json['name'] = school_one

                                        ret['schools'].append(school_json)

                response['result'] = 'success'
                return "%s" %(json.dumps(response))

            except Exception,ex: 
                response['result'] = 'error'
                response['message'] = "error:%s" %(ex)
                return "%s" %(json.dumps(response))

        @bottle.route('/api/get/province')
        def get_city_info():

            response = {}
            response['result'] = 'error'
            response['schools'] = []

            return "%s" %(json.dumps(response))

        @bottle.route('/api/get/:province/city')
        def get_city_info(province=None):

            response = {}
            response['result'] = 'error'
            response['schools'] = []

            print "province:%s, type:%s" %(province,type(province))

            return "%s" %(json.dumps(response))


        @bottle.route('/api/get/:province/:city/county')
        def get_county_info(province=None, city=None):
            response = {}
            response['result'] = 'error'
            response['county'] = []

            print "province:%s, type:%s, city:%s, type:%s" %(province,type(province), city, type(city))

            # check the area code

            # get the city id
            city_id = "%s%s" %(province,city)

            # get the city json
            city_json = None
            for city_one in self.schools_json['schools']:
                if city_one['id'] == city_id:
                    city_json = city_one
                    break
           
            if city_json == None:
                self.logger.debug('not found the city which area code is %s.' %(city_id))
                return "%s" %(json.dumps(response))


            for county_one in city_json['data']:
                county_json = {}
                county_json['name'] = county_one['name']
                county_json['id'] = county_one['id'][-6:]
                ret['county'].append(county_json)

            response['result'] = 'success'

            return "%s" %(json.dumps(response))



        @bottle.route('/api/verify/license', method="POST")
        def verify_license():
            response = {}
            response['result'] = 'error'
            response['logo_url'] = ''

            # just for test
            response['result'] = 'success'
            response['logo_url'] = '/images/agency/teamnxxt.png'       
            return "%s" %(json.dumps(response))

    def run(self):
        bottle.run(host=self.ip, port=self.port, debug=True)



if __name__ == "__main__":
    server = Server('0.0.0.0', 80, logging.DEBUG)
    server.run()

else:
    #os.chdir(os.path.dirname(__file__))
    server = Server('0.0.0.0', 80, logging.DEBUG)
    application = default_app()