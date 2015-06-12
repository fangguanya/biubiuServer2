#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import json

from Database import Database
from datetime import datetime

import bottle

from Consts import Consts

#from bottle import route, run, template, error, static_file, default_app



__author__ = 'shenhailuanma'
__version__ = '0.1.0'


class Server:
    def __init__(self, ip='0.0.0.0', port=9090 ,log_level=logging.DEBUG):

        self.ip   = ip
        self.port = port

        self.author  = __author__
        self.version = __version__

        self.file_path = os.path.realpath(__file__)
        self.dir_path  = os.path.dirname(self.file_path)

        # the database
        self.database = Database()

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
            root_path = "%s/../images" %(self.dir_path)
            return bottle.static_file(filename, root=root_path)

        @bottle.route('/images/agency/:filename')
        def send_image_agency(filename=None):
            # FIXME: the param 'root' should be define in other place, now just for test.
            root_path = "%s/../images/agency" %(self.dir_path)
            return bottle.static_file(filename, root=root_path)

        @bottle.route('/images/agencys/:filename')
        def send_image_agencys(filename=None):
            # FIXME: the param 'root' should be define in other place, now just for test.
            root_path = "%s/../images/agencys" %(self.dir_path)
            return bottle.static_file(filename, root=root_path)

        @bottle.route('/configs/:filename')
        def send_files(filename=None):
            # FIXME: the param 'root' should be define in other place, now just for test.
            root_path = "%s/../files" %(self.dir_path)
            return bottle.static_file(filename, root=root_path)


        #################
        #API
        #################
        @bottle.route('/api/gettime')
        def gettime():
            return "%s" %(datetime.now())

        @bottle.route('/api/get/schools/:number')
        def api_get_schools(number=None):
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

                                        response['schools'].append(school_json)

                response['result'] = 'success'
                return "%s" %(json.dumps(response))

            except Exception,ex: 
                response['result'] = 'error'
                response['message'] = "error:%s" %(ex)
                return "%s" %(json.dumps(response))

        @bottle.route('/api/get/province')
        def api_get_city_info():

            response = {}
            response['result'] = 'error'
            response['schools'] = []

            return "%s" %(json.dumps(response))

        @bottle.route('/api/get/:province/city')
        def api_get_city_info(province=None):

            response = {}
            response['result'] = 'error'
            response['schools'] = []

            print "province:%s, type:%s" %(province,type(province))

            return "%s" %(json.dumps(response))


        @bottle.route('/api/get/:province/:city/county')
        def api_get_county_info(province=None, city=None):

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
                response['county'].append(county_json)

            response['result'] = 'success'

            return "%s" %(json.dumps(response))


        @bottle.route('/api2/qq/login', method="POST")
        def api2_qq_login():
            response = {}
            response['result'] = 'error'
            response['logo_url'] = ''

            try:
                self.logger.debug('handle a request: /api2/qq/login, ')

                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))
                '''
                {
                    "openid"   : "OPENID",
                    "openkey"  : "OPEN_KEY",
                    "name"     : "The player name(nickname)",
                    "head_url" : "http://ip/the_player_head_url"
                }
                '''
                post_data_json = json.loads(post_data)


                # check the must params


                # just for test
                response['result'] = 'success'


                return "%s" %(json.dumps(response))

            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['code']   = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 




        @bottle.route('/api/verify/license', method="POST")
        def api_verify_license():
            response = {}
            response['result'] = 'error'
            response['logo_url'] = ''

            try:
                self.logger.debug('handle a request:/api/verify/license, ')

                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))
                '''
                    {
                        "license" : "LICENSE_CODE",
                        "player" : "PLAYER_ID"
                    }
                '''
                post_data_json = json.loads(post_data)


                # check the must params
                if not post_data_json.has_key('license'):
                    response['result'] = 'error'
                    response['message'] = 'need param license.'
                    return "%s" %(json.dumps(response))   


                # get the license info by param:license
                ret,msg,license_info = self.database.db_get_license(post_data_json['license'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get license error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(license_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no license:%s.' %(post_data_json['license'])
                    return "%s" %(json.dumps(response)) 

                # if license has been used, return 'error'
                if license_info[0]['status'] != Consts.license_active:
                    response['result'] = 'error'
                    response['message'] = 'The license:%s has been used.' %(post_data_json['license'])
                    return "%s" %(json.dumps(response)) 



                # just for test
                response['result'] = 'success'
                response['logo_url'] = license_info[0]['logo'] 

                return "%s" %(json.dumps(response))

            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 

        @bottle.route('/api/create/guild', method="POST")
        def api_create_guild():
            try:
                
                response = {}
                response['result'] = 'error'
                response['logo_url'] = ''

                self.logger.debug('handle a request:/api/create/guild, ')

                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))
                '''
                    The data format should be:
                    {
                        "player" : "PLAYER_OPEN_ID",
                        "license": "LICENSE_CODE",
                        "name" : "NAME",
                        "logo" : "Logo_ID"
                    }
                '''
                post_data_json = json.loads(post_data)

                # chekc license
                # check the must params
                if not post_data_json.has_key('license'):
                    response['result'] = 'error'
                    response['message'] = 'need param license.'
                    return "%s" %(json.dumps(response))   


                # get the license info by param:license
                ret,msg,license_info = self.database.db_get_license(post_data_json['license'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get license error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(license_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no license:%s.' %(post_data_json['license'])
                    return "%s" %(json.dumps(response)) 

                # if license has been used, return 'error'
                if license_info[0]['status'] != Consts.license_active:
                    response['result'] = 'error'
                    response['message'] = 'The license:%s has been used.' %(post_data_json['license'])
                    return "%s" %(json.dumps(response)) 

                # check the params
                if post_data_json.has_key('player'):
                    # check the player
                    # 1. get the player info
                    ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                    if ret != 'success':
                        response['result'] = 'error'
                        response['message'] = 'get player error:%s.' %(msg)
                        return "%s" %(json.dumps(response)) 

                    if len(player_info) < 1:
                        response['result'] = 'error'
                        response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                        return "%s" %(json.dumps(response)) 

                    self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                    # 2. check player has if or not join guild.
                    if player_info[0]['guildID'] > 0:
                        response['result'] = 'error'
                        response['message'] = 'player:%s is in other guild:%s.' %(post_data_json['player'],player_info[0]['guildID'])
                        return "%s" %(json.dumps(response)) 

                    # 3. check the player can or not to create guild.
                    
                else:
                    response['result'] = 'error'
                    response['message'] = 'need param player.'
                    return "%s" %(json.dumps(response)) 

                guild_id = -1
                # create the guild
                if license_info[0]['logo'] != '':
                    post_data_json['logo'] = license_info[0]['logo']

                response['logo_url'] = post_data_json['logo']

                ret, msg, guild_id = self.database.db_create_guild(post_data_json)
                if  ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'create guild error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 
                else:
                    self.logger.debug('guild create success, id: %s' %(guild_id))


                # update the license info
                license_update_params = {}
                license_update_params['license'] = post_data_json['license']
                license_update_params['playerOpenID'] = post_data_json['player']
                license_update_params['playerID'] = player_info[0]['id']
                license_update_params['status'] = Consts.license_used
                ret, msg = self.database.db_update_license(license_update_params)
                if  ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update license error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 



                # add the player to guild
                create_member_params = {}
                create_member_params['player'] = post_data_json['player']
                create_member_params['player_id'] = player_info[0]['id']
                create_member_params['guild_id'] = guild_id
                ret,msg,member_id = self.database.db_create_guildMember(create_member_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'Add player:%s to guild error:%s.' %(create_member_params['player'],create_member_params['guild_id'])
                    return "%s" %(json.dumps(response)) 
                else:
                    self.logger.debug('Add the player member:%s ok.' %(member_id))

                # update the guild info
                update_guild_params = {}
                update_guild_params['guild_id'] = guild_id
                update_guild_params['number'] =  1

                ret,msg = self.database.db_update_guild_info(update_guild_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the number to guild error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 
                else:
                    self.logger.debug('update the guild info success.')

                # update the player info
                update_player_params = {}
                update_player_params['player_openid'] = post_data_json['player']
                update_player_params['guild_id'] = guild_id

                ret,msg = self.database.db_update_player_info(update_player_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the player info error:%s.' %(msg)
                    return "%s" %(json.dumps(response))   
                else:
                    self.logger.debug('update the player info success.')

                response['result'] = 'success'
                response['id'] = guild_id

                return "%s" %(json.dumps(response))

            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 



        @bottle.route('/api/search/guild', method="POST")
        def api_search_guild():
            response = {}
            response['result'] = 'error'
            response['guilds'] = []
            #response['number'] = 0


            player_openid = ''
            guilds = []
            try:
                self.logger.debug('handle a request:/api/searchsearch/guild, ')

                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))
                '''
                    The data format should be:
                    {
                        "player" : "PLAYER_ID",
                        "mode": "",         # support 'all', 'city', 'nearby', 'id', 'name'
                        "range_min" : 1, 
                        "range_max" : 20,
                        "sort_type" : "exp", 
                        
                        "city_name" : "",       # for mode 'city'
                        "longitude" : 12.334    # for mode 'nearby'
                        "latitude"  : 23.345    # for mode 'nearby'
                        "guild_id"  : 23        # for mode 'id'
                        "guild_name": "name"    # for mode 'name'
                    }
                '''

                post_data_json = json.loads(post_data)

                # check the params
                if post_data_json.has_key('mode'):
                    if post_data_json['mode'] not in ['all', 'city', 'nearby', 'id', 'name']:
                        response['result'] = 'error'
                        response['message'] = 'mode:%s not support.' %(post_data_json['mode'])
                        return "%s" %(json.dumps(response)) 
                else:
                    response['result'] = 'error'
                    response['message'] = 'need must key:mode.'
                    return "%s" %(json.dumps(response))        

                if post_data_json['mode'] == 'all':
                    offset = 0
                    number = 25
                    if post_data_json.has_key('range_min'):
                        if isinstance(post_data_json['range_min'],int):
                            offset = post_data_json['range_min'] - 1
                    
                    if post_data_json.has_key('range_max'):
                        if isinstance(post_data_json['range_max'],int):
                            number = post_data_json['range_max'] - offset

                    ret,msg,guilds = self.database.db_search_guild(offset, number)
                #elif 

                else:
                    response['result'] = 'error'
                    response['message'] = 'mode:%s not support.' %(post_data_json['mode'])
                    return "%s" %(json.dumps(response))  


                # if has player, check the player if in one guild, if true set the 'if_in_guild' to 'yes'
                if post_data_json.has_key('player'):
                    # get player info 
                    ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                    if ret != 'success':
                        response['result'] = 'error'
                        response['message'] = 'get player error:%s.' %(msg)
                        return "%s" %(json.dumps(response)) 

                    if len(player_info) >= 1:
                        self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                        if player_info[0]['guildID'] > 0:

                            for guild_one in guilds:
                                if player_info[0]['guildID'] == guild_one['guild_id']:
                                    guild_one['if_in_guild'] = 1

                                if post_data_json['player'] == guild_one['createrOpenID']:
                                    guild_one['if_in_guild'] = 2




                response['guilds'] = guilds
                # just for test
                response['result'] = 'success'
                #response['logo_url'] = '/images/agency/teamnxxt.png'
                return "%s" %(json.dumps(response))


            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 


        @bottle.route('/api/add/guildmember', method="POST")
        def api_add_guildmember():
            response = {}
            response['result'] = 'error'
            response['member_id'] = -1
            try:
                self.logger.debug('handle a request:/api/add/guildmember')   
                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))

                '''
                    post data format:
                    {
                        "player" : "PLAYER_ID",  
                        "guild_id" : 92    
                    }
                '''
                post_data_json = json.loads(post_data)

                # check must key
                if not post_data_json.has_key('player'):
                    response['result'] = 'error'
                    response['message'] = 'need param: player.'
                    return "%s" %(json.dumps(response)) 

                if not post_data_json.has_key('guild_id'):
                    response['result'] = 'error'
                    response['message'] = 'need param: guild_id.'
                    return "%s" %(json.dumps(response)) 

                # get the player info
                ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                # check player has if or not join guild.
                if player_info[0]['guildID'] > 0:
                    response['result'] = 'error'
                    response['message'] = 'player:%s is in other guild:%s.' %(post_data_json['player'],player_info[0]['guildID'])
                    return "%s" %(json.dumps(response)) 


                # check the guild and if can be add new one
                ret,msg,guild_info = self.database.db_get_guild_by_guildID(post_data_json['guild_id'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get guild info error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(guild_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no guild for id:%s.' %(post_data_json['guild_id'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get guild info: %s.' %(json.dumps(guild_info)))

                # check the guild can join new one
                if guild_info[0]['people_number'] >= guild_info[0]['people_limits']:
                    response['result'] = 'error'
                    response['message'] = 'The guild has full.'
                    return "%s" %(json.dumps(response)) 

                # add the player to guild
                post_data_json['player_id'] = player_info[0]['id']
                ret,msg,member_id = self.database.db_create_guildMember(post_data_json)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'Add player:%s to guild error:%s.' %(post_data_json['player'],post_data_json['guild_id'])
                    return "%s" %(json.dumps(response)) 

                # update the guild info
                update_guild_params = {}
                update_guild_params['guild_id'] = guild_info[0]['guild_id']
                update_guild_params['number'] = guild_info[0]['people_number'] + 1

                ret,msg = self.database.db_update_guild_info(update_guild_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the number to guild error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                # update the player info
                update_player_params = {}
                update_player_params['player_openid'] = post_data_json['player']
                update_player_params['guild_id'] = guild_info[0]['guild_id']

                ret,msg = self.database.db_update_player_info(update_player_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the player info error:%s.' %(msg)
                    return "%s" %(json.dumps(response))           


                response['result'] = 'success'
                response['member_id'] = member_id
                return "%s" %(json.dumps(response))

            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 

        @bottle.route('/api/get/guild' , method="POST")
        def api_get_guild_info():
            response = {}
            response['result']  = 'error'
            response['members'] = []

            guild_id = None
            try:
                self.logger.debug('handle a request: /api/get/guild ')   
                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))

                '''
                    post data format:
                    {
                        "mode" : "guild",
                        "guild_id" : 22,
                        "player" : "PLAYER_ID"
                    }
                '''
                post_data_json = json.loads(post_data)

                # check params
                if not post_data_json.has_key('mode'):
                    response['result'] = 'error'
                    response['message'] = 'need param: mode.'
                    return "%s" %(json.dumps(response)) 

                if post_data_json['mode'] == 'guild':
                    if not post_data_json.has_key('guild_id'):
                        response['result'] = 'error'
                        response['message'] = 'need param: guild_id.'
                        return "%s" %(json.dumps(response)) 

                elif post_data_json['mode'] == 'player':
                    if not post_data_json.has_key('player'):
                        response['result'] = 'error'
                        response['message'] = 'need param: player.'
                        return "%s" %(json.dumps(response))  
                else:
                    response['result'] = 'error'
                    response['message'] = 'mode:%s not support.' %(post_data_json['mode'])
                    return "%s" %(json.dumps(response)) 


                # different mode only neet guild_id to get the detil info.
                if  post_data_json['mode'] == 'player':
                    # get the player info
                    ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                    if ret != 'success':
                        response['result'] = 'error'
                        response['message'] = 'get player error:%s.' %(msg)
                        return "%s" %(json.dumps(response)) 

                    if len(player_info) < 1:
                        response['result'] = 'error'
                        response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                        return "%s" %(json.dumps(response)) 

                    self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))
                    guild_id = player_info[0]['guildID']

                
                elif post_data_json['mode'] == 'guild':
                    guild_id = post_data_json['guild_id']



                if guild_id == None:
                    response['result'] = 'error'
                    response['message'] = "guild id not difined."
                    return "%s" %(json.dumps(response))


                # get the guild info by id
                # check the guild and if can be add new one
                ret,msg,guild_info = self.database.db_get_guild_by_guildID(guild_id)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get guild info error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(guild_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no guild for id:%s.' %(guild_id)
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get guild info: %s.' %(json.dumps(guild_info)))
                
                response['guild_info'] = guild_info[0]

                # get the guild members info
                ret,msg,guild_members = self.database.db_get_guildMembers_by_guildID(guild_id)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get guild info error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get guild member info: %s.' %(json.dumps(guild_members)))
                # get the guild members more info
                for member_one in guild_members:
                    ret,msg,player_info = self.database.db_get_player_by_openid(member_one['openid'])
                    if  ret != 'success':
                        self.logger.error('Get guild member:%s player info error: %s.' %(member_one['openid'], msg))

                        member_one['name']  = ''
                        member_one['head']  = ''
                        member_one['level'] = 0
                    else:
                        self.logger.debug('Get guild member:%s player info : %s.' %(member_one['openid'], player_info[0]))
                        member_one['name']  = player_info[0]['name']
                        member_one['head']  = player_info[0]['head']
                        member_one['level'] = player_info[0]['level']

                    if member_one['openid'] == guild_info[0]['createrOpenID']:
                        member_one['iscreater'] = 1


                response['members'] = guild_members
                
                response['result'] = "success"
                return "%s" %(json.dumps(response)) 

            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 


        @bottle.route('/api/quit/guild', method="POST")
        def api_quit_guild():
            response = {}
            response['result'] = 'error'

            try:
                self.logger.debug('handle a request: /api/quit/guild ')   
                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))

                '''
                    post data format:
                    {
                        "player" : "PLAYER_ID"
                    }
                '''
                post_data_json = json.loads(post_data)


                # check must key
                if not post_data_json.has_key('player'):
                    response['result'] = 'error'
                    response['message'] = 'need param: player.'
                    return "%s" %(json.dumps(response)) 


                # get the player info
                ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                # check player has if or not join guild.
                if player_info[0]['guildID'] <= 0:
                    response['result'] = 'success'
                    response['message'] = 'player:%s not in any guild, so no need to quit guild.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 


                post_data_json['guild_id'] = player_info[0]['guildID']
                # check the guild 
                ret,msg,guild_info = self.database.db_get_guild_by_guildID(post_data_json['guild_id'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get guild info error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(guild_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no guild for id:%s.' %(post_data_json['guild_id'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get guild info: %s.' %(json.dumps(guild_info)))


                # if the player is the guild creater, return error
                if  post_data_json['player'] ==  guild_info[0]['createrOpenID']:
                    response['result'] = 'error'
                    response['message'] = 'The player is guild guild creater, can not quit.'
                    return "%s" %(json.dumps(response)) 

                # the player quit the guild
                quit_guild_params = {}
                quit_guild_params['guild_id'] = post_data_json['guild_id']
                quit_guild_params['player_openid'] = post_data_json['player']
                quit_guild_params['status'] = Consts.guildMember_status_leave
                ret, msg = self.database.db_update_guildMember_info(quit_guild_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the guildMember info error:%s.' %(msg)
                    return "%s" %(json.dumps(response))  

                # update the guild info
                update_guild_params = {}
                update_guild_params['guild_id'] = guild_info[0]['guild_id']
                update_guild_params['number'] = guild_info[0]['people_number'] - 1

                ret,msg = self.database.db_update_guild_info(update_guild_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the number to guild error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 


                # update the player info
                update_player_params = {}
                update_player_params['player_openid'] = post_data_json['player']
                update_player_params['guild_id'] = 0

                ret,msg = self.database.db_update_player_info(update_player_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the player info error:%s.' %(msg)
                    return "%s" %(json.dumps(response))    


                response['result'] = "success"
                return "%s" %(json.dumps(response)) 
            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 


        @bottle.route('/api/delete/guild', method="POST")
        def api_delete_guild():
            response = {}
            response['result'] = 'error'

            try:
                self.logger.debug('handle a request: /api/delete/guild ')   
                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))

                '''
                    post data format:
                    {
                        "player" : "PLAYER_ID"
                    }
                '''
                post_data_json = json.loads(post_data)


                # check must key
                if not post_data_json.has_key('player'):
                    response['result'] = 'error'
                    response['message'] = 'need param: player.'
                    return "%s" %(json.dumps(response)) 


                # get the player info
                ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                # check player has if or not join guild.
                if player_info[0]['guildID'] <= 0:
                    response['result'] = 'success'
                    response['message'] = 'player:%s not in any guild, so no need to quit guild.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 


                post_data_json['guild_id'] = player_info[0]['guildID']
                # check the guild 
                ret,msg,guild_info = self.database.db_get_guild_by_guildID(post_data_json['guild_id'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get guild info error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(guild_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no guild for id:%s.' %(post_data_json['guild_id'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get guild info: %s.' %(json.dumps(guild_info)))


                # if the player is not the guild creater, return error
                if  post_data_json['player'] !=  guild_info[0]['createrOpenID']:
                    response['result'] = 'error'
                    response['message'] = 'The player is not guild guild creater, can not to delete the guild.'
                    return "%s" %(json.dumps(response)) 

                # the player quit the guild
                quit_guild_params = {}
                quit_guild_params['guild_id'] = post_data_json['guild_id']
                quit_guild_params['status'] = Consts.guildMember_status_leave
                ret, msg = self.database.db_update_all_guildMember_info(quit_guild_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the guildMember info error:%s.' %(msg)
                    return "%s" %(json.dumps(response))  

                # update the guild info
                update_guild_params = {}
                update_guild_params['guild_id'] = guild_info[0]['guild_id']
                update_guild_params['status'] = Consts.guild_status_delete
                ret,msg = self.database.db_update_guild_info(update_guild_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the number to guild error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 


                # update the player info
                update_player_params = {}
                update_player_params['guild_id'] = 0

                ret,msg = self.database.db_update_player_info_by_guildId(update_player_params, guild_info[0]['guild_id'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the player info error:%s.' %(msg)
                    return "%s" %(json.dumps(response))    


                response['result'] = "success"
                return "%s" %(json.dumps(response)) 
            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 



        @bottle.route('/api/update/guild', method="POST")
        def api_update_guild():
            response = {}
            response['result'] = 'error'

            try:
                self.logger.debug('handle a request: /api/update/guild ')   
                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))

                '''
                    post data format:
                    {
                        "player" : "PLAYER_ID",         
                        "guild_id" : 92 ,              
                        
                        
                        "head": "xxx",            
                        "headID" : 23,
                        "province" : 8, 
                        "city": 23,
                        "county" : 11, 
                        "longitude" : 23.456, 
                        "latitude" : 33.456, 
                    }
                '''
                post_data_json = json.loads(post_data)


                # check must key
                if not post_data_json.has_key('player'):
                    response['result'] = 'error'
                    response['message'] = 'need param: player.'
                    return "%s" %(json.dumps(response)) 
                if not post_data_json.has_key('guild_id'):
                    response['result'] = 'error'
                    response['message'] = 'need param: guild_id.'
                    return "%s" %(json.dumps(response)) 

                # check the params value
                if  post_data_json.has_key('player'):
                    if not isinstance(post_data_json['player'], basestring):
                        response['result'] = 'error'
                        response['message'] = 'The type error, the param: player type should be string.'
                        return "%s" %(json.dumps(response)) 

                if  post_data_json.has_key('guild_id'):
                    if not isinstance(post_data_json['guild_id'], int):
                        response['result'] = 'error'
                        response['message'] = 'The type error, the param: guild_id type should be int.'
                        return "%s" %(json.dumps(response)) 


                # get the player info
                ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                # check player has if or not join guild.
                if player_info[0]['guildID'] <= 0:
                    response['result'] = 'success'
                    response['message'] = 'player:%s not in any guild, so cant update guild.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 

                post_data_json['guild_id'] = player_info[0]['guildID']
                # check the guild 
                ret,msg,guild_info = self.database.db_get_guild_by_guildID(post_data_json['guild_id'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get guild info error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(guild_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no guild for id:%s.' %(post_data_json['guild_id'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get guild info: %s.' %(json.dumps(guild_info)))


                # if the player is not the guild creater, return error
                if  post_data_json['player'] !=  guild_info[0]['createrOpenID']:
                    response['result'] = 'error'
                    response['message'] = 'The player is not guild guild creater, can not to update the guild.'
                    return "%s" %(json.dumps(response)) 

                # update the guild info
                update_guild_params = {}
                update_guild_params['guild_id'] = post_data_json['guild_id']
                if  post_data_json.has_key('head'):
                    update_guild_params['head'] = post_data_json['head']

                if  post_data_json.has_key('headID'):
                    update_guild_params['headID'] = post_data_json['headID']             

                if  post_data_json.has_key('province'):
                    update_guild_params['province'] = post_data_json['province']   

                if  post_data_json.has_key('city'):
                    update_guild_params['city'] = post_data_json['city']  

                if  post_data_json.has_key('county'):
                    update_guild_params['county'] = post_data_json['county']  

                if  post_data_json.has_key('longitude'):
                    update_guild_params['longitude'] = post_data_json['longitude']  

                if  post_data_json.has_key('latitude'):
                    update_guild_params['latitude'] = post_data_json['latitude']  

                ret,msg = self.database.db_update_guild_info(update_guild_params)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'update the number to guild error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 
                else:
                    self.logger.debug('update the guild info success.')


                response['result'] = "success"
                return "%s" %(json.dumps(response)) 
            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 


        @bottle.route('/api/update/props', method="POST")
        def api_update_props():
            response = {}
            response['result'] = 'error'

            try:
                self.logger.debug('handle a request: /api/update/props ')   
                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))

                '''
                    {
                        "who" : "player",
                        "openid" : "xxx",
                        "guildid" : 23,

                        "exp" : 100,
                        "gold": -200,
                        "gem": 1000,
                        "prop": {
                                "bomb" : 20,
                                "glass": 30,
                                "delay": 10,
                                "point": 10
                        }
                    }
                '''
                post_data_json = json.loads(post_data)


                # check must key
                if not post_data_json.has_key('who'):
                    response['result'] = 'error'
                    response['message'] = 'need param: who.'
                    return "%s" %(json.dumps(response)) 

                if  post_data_json['who'] == 'player':
                    if not post_data_json.has_key('openid'):
                        response['result'] = 'error'
                        response['message'] = 'need param: openid.'
                        return "%s" %(json.dumps(response)) 

                elif post_data_json['who'] == 'guild':
                    if not post_data_json.has_key('guildid'):
                        response['result'] = 'error'
                        response['message'] = 'need param: guildid.'
                        return "%s" %(json.dumps(response)) 

                else:
                    response['result'] = 'error'
                    response['message'] = 'param: who not support value:%s.' %(post_data_json['who'])
                    return "%s" %(json.dumps(response)) 


                # check the params value
                if  post_data_json.has_key('openid'):
                    if not isinstance(post_data_json['openid'], basestring):
                        response['result'] = 'error'
                        response['message'] = 'The type error, the param: openid type should be string.'
                        return "%s" %(json.dumps(response)) 

                if  post_data_json.has_key('guildid'):
                    if not isinstance(post_data_json['guildid'], int):
                        response['result'] = 'error'
                        response['message'] = 'The type error, the param: guildid type should be int.'
                        return "%s" %(json.dumps(response)) 



                if  post_data_json.has_key('exp'):
                    if not isinstance(post_data_json['exp'], int):
                        response['result'] = 'error'
                        response['message'] = 'The type error, the param: exp type should be int.'
                        return "%s" %(json.dumps(response))             



                if  post_data_json.has_key('gold'):
                    if not isinstance(post_data_json['gold'], int):
                        response['result'] = 'error'
                        response['message'] = 'The type error, the param: gold type should be int.'
                        return "%s" %(json.dumps(response))   

                if  post_data_json.has_key('gem'):
                    if not isinstance(post_data_json['gem'], int):
                        response['result'] = 'error'
                        response['message'] = 'The type error, the param: gem type should be int.'
                        return "%s" %(json.dumps(response))  


                if  post_data_json.has_key('prop'):
                    if not isinstance(post_data_json['prop'], dict):
                        response['result'] = 'error'
                        response['message'] = 'The type error, the param: prop type should be int.'
                        return "%s" %(json.dumps(response)) 


                if  post_data_json['who'] == 'player':
                    # get the player info
                    ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['openid'])
                    if ret != 'success':
                        response['result'] = 'error'
                        response['message'] = 'get player error:%s.' %(msg)
                        return "%s" %(json.dumps(response)) 

                    if len(player_info) < 1:
                        response['result'] = 'error'
                        response['message'] = 'there is no player for id:%s.' %(post_data_json['openid'])
                        return "%s" %(json.dumps(response)) 

                    self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                    # update the player info
                    update_player_params = {}
                    update_player_params['player_openid'] = post_data_json['openid']

                    if post_data_json.has_key('exp'):
                        update_player_params['exp'] = player_info[0]['exp'] + post_data_json['exp']

                    if post_data_json.has_key('gold'):
                        update_player_params['gold'] = player_info[0]['gold'] + post_data_json['gold']

                    # player not support gem yeat
                    #if post_data_json.has_key('gem'):
                    #    update_player_params['gem'] = player_info[0]['gem'] + post_data_json['gem']

                    if post_data_json.has_key('prop'):
                        update_player_param_prop = {}
                        if player_info[0]['prop'].has_key('bomb'):
                            update_player_param_prop['bomb']  = player_info[0]['prop']['bomb']
                        else:
                            update_player_param_prop['bomb'] = 0

                        if player_info[0]['prop'].has_key('glass'):
                            update_player_param_prop['glass'] = player_info[0]['prop']['glass']
                        else:
                            update_player_param_prop['glass'] = 0

                        if player_info[0]['prop'].has_key('delay'):
                            update_player_param_prop['delay'] = player_info[0]['prop']['delay']
                        else:
                            update_player_param_prop['delay'] = 0

                        if player_info[0]['prop'].has_key('point'):
                            update_player_param_prop['point'] = player_info[0]['prop']['point']
                        else:
                            update_player_param_prop['point'] = 0


                        if post_data_json['prop'].has_key('bomb'):
                            update_player_param_prop['bomb'] += post_data_json['prop']['bomb']

                        if post_data_json['prop'].has_key('glass'):
                            update_player_param_prop['glass'] += post_data_json['prop']['glass']
 
                        if post_data_json['prop'].has_key('delay'):
                            update_player_param_prop['delay'] += post_data_json['prop']['delay']

                        if post_data_json['prop'].has_key('point'):
                            update_player_param_prop['point'] += post_data_json['prop']['point']

                        update_player_params['prop'] = json.dumps(update_player_param_prop)

                    ret,msg = self.database.db_update_player_info(update_player_params)
                    if ret != 'success':
                        response['result'] = 'error'
                        response['message'] = 'update the player info error:%s.' %(msg)
                        return "%s" %(json.dumps(response))   
                    else:
                        self.logger.debug('update the player info success.')

                    # if has exp, update guild member exp
                    if player_info[0]['guildID'] > 0 and post_data_json.has_key('exp'):
                        # check the guild 
                        ret,msg,guild_info = self.database.db_get_guild_by_guildID(player_info[0]['guildID'])
                        if ret != 'success':
                            response['result'] = 'error'
                            response['message'] = 'get guild info error:%s.' %(msg)
                            return "%s" %(json.dumps(response)) 

                        if len(guild_info) < 1:
                            response['result'] = 'error'
                            response['message'] = 'there is no guild for id:%s.' %(player_info[0]['guildID'])
                            return "%s" %(json.dumps(response)) 

                        self.logger.debug('Get guild info: %s.' %(json.dumps(guild_info)))

                        # update the guild exp
                        update_guild_params = {}
                        update_guild_params['guild_id'] = player_info[0]['guildID']
                        
                        update_guild_params['exp'] = guild_info[0]['exp'] + post_data_json['exp']


                        ret,msg = self.database.db_update_guild_info(update_guild_params)
                        if ret != 'success':
                            response['result'] = 'error'
                            response['message'] = 'update the number to guild error:%s.' %(msg)
                            return "%s" %(json.dumps(response)) 
                        else:
                            self.logger.debug('update the guild info success.')


                        # if has exp, update guild member exp
                        quit_guild_params = {}
                        quit_guild_params['guild_id'] = player_info[0]['guildID']
                        quit_guild_params['player_openid'] = post_data_json['openid']
                        quit_guild_params['exp'] = post_data_json['exp']
                        ret, msg = self.database.db_update_guildMember_info(quit_guild_params)
                        if ret != 'success':
                            response['result'] = 'error'
                            response['message'] = 'update the guildMember info error:%s.' %(msg)
                            return "%s" %(json.dumps(response))  


                elif post_data_json['who'] == 'guild':
                    # check the guild 
                    ret,msg,guild_info = self.database.db_get_guild_by_guildID(post_data_json['guildid'])
                    if ret != 'success':
                        response['result'] = 'error'
                        response['message'] = 'get guild info error:%s.' %(msg)
                        return "%s" %(json.dumps(response)) 

                    if len(guild_info) < 1:
                        response['result'] = 'error'
                        response['message'] = 'there is no guild for id:%s.' %(post_data_json['guildid'])
                        return "%s" %(json.dumps(response)) 

                    self.logger.debug('Get guild info: %s.' %(json.dumps(guild_info)))

                    # update the guild info
                    update_guild_params = {}
                    update_guild_params['guild_id'] = post_data_json['guildid']
                    
                    #update_guild_params['exp'] = guild_info[0]['exp'] + post_data_json['exp']
                    if post_data_json.has_key('gold'):
                        update_guild_params['gold'] = guild_info[0]['gold'] + post_data_json['gold']

                    if post_data_json.has_key('gem'):
                        update_guild_params['gem'] = guild_info[0]['gem'] + post_data_json['gem']


                    if post_data_json.has_key('prop'):
                        update_guild_param_prop = {}
                        if guild_info[0]['prop'].has_key('bomb'):
                            update_guild_param_prop['bomb']  = guild_info[0]['prop']['bomb']
                        else:
                            update_guild_param_prop['bomb'] = 0

                        if guild_info[0]['prop'].has_key('glass'):
                            update_guild_param_prop['glass'] = guild_info[0]['prop']['glass']
                        else:
                            update_guild_param_prop['glass'] = 0

                        if guild_info[0]['prop'].has_key('delay'):
                            update_guild_param_prop['delay'] = guild_info[0]['prop']['delay']
                        else:
                            update_guild_param_prop['delay'] = 0

                        if guild_info[0]['prop'].has_key('point'):
                            update_guild_param_prop['point'] = guild_info[0]['prop']['point']
                        else:
                            update_guild_param_prop['point'] = 0


                        if post_data_json['prop'].has_key('bomb'):
                            update_guild_param_prop['bomb'] += post_data_json['prop']['bomb']

                        if post_data_json['prop'].has_key('glass'):
                            update_guild_param_prop['glass'] += post_data_json['prop']['glass']
 
                        if post_data_json['prop'].has_key('delay'):
                            update_guild_param_prop['delay'] += post_data_json['prop']['delay']

                        if post_data_json['prop'].has_key('point'):
                            update_guild_param_prop['point'] += post_data_json['prop']['point']

                        update_guild_params['prop'] = json.dumps(update_guild_param_prop)



                    ret,msg = self.database.db_update_guild_info(update_guild_params)
                    if ret != 'success':
                        response['result'] = 'error'
                        response['message'] = 'update the number to guild error:%s.' %(msg)
                        return "%s" %(json.dumps(response)) 
                    else:
                        self.logger.debug('update the guild info success.')



                response['result'] = "success"
                return "%s" %(json.dumps(response)) 
            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 


        @bottle.route('/api/ranklist/:player/:index')
        def api_get_ranklist(player=None,index=None):
            response = {}
            response['result']  = 'error'

            guild_id = None
            try:
                self.logger.debug('handle a request: /api/ranklist/:player/:index')   
                self.logger.debug('player:%s, type:%s, index:%s, type:%s.' %(player,type(player), index, type(index)))   
                # check the params
                if player == None:
                    response['result'] = 'error'
                    response['message'] = 'params player is None.'
                    return "%s" %(json.dumps(response))

                if index == None:
                    response['result'] = 'error'
                    response['message'] = 'params index error.'
                    return "%s" %(json.dumps(response))   



                post_data_json = {}
                post_data_json['player'] = player
                post_data_json['index']  = index

                response['index'] = index

                # get the player info , if not get player info ,just get by index
                ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))


                # get the first 3
                ret,msg,firsts_player_info = self.database.db_get_ranklist_range(index, 0,3)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(firsts_player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no index:%s.' %(index)
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get ranklist firsts player info: %s.' %(json.dumps(firsts_player_info)))



                # get the player ranking
                ret,msg,player_ranking_info = self.database.db_get_ranking_number(index, player_info[0]['id'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get ranking error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 
                else:
                    self.logger.debug('Get player ranking info, ret:%s, info: %s.' %(ret, json.dumps(player_ranking_info)))

                ranklist_offset = 0
                ranklist_number = 11

                if len(player_ranking_info) < 1:
                    self.logger.debug( 'there is no id:%s in ranklist:%s.' %(player_info[0]['id'], index))
                else:
                    self.logger.debug('ranking info: %s.' %(json.dumps(player_ranking_info)))
                    if player_ranking_info[0]['number'] >= 5:
                        ranklist_offset = player_ranking_info[0]['number']-5


                response['first'] = []
                member_cnt = 0
                for firsts_player_info_one in firsts_player_info:
                    # get player info
                    ranklist_member_one = {}
                    
                    ret,msg,member_info = self.database.db_get_player_by_id(firsts_player_info_one['playerID'])
                    if ret == 'success' and len(member_info) > 0:
                        ranklist_member_one['name'] = member_info[0]['name']
                        ranklist_member_one['head'] = member_info[0]['head']
                        ranklist_member_one['guild_id'] = member_info[0]['guildID']
                    else:
                        ranklist_member_one['name'] = ""
                        ranklist_member_one['head'] = ""
                        ranklist_member_one['guild_id'] = 0

                    if member_info[0]['account'] == player:
                        ranklist_member_one['isplayer'] = 1
                    else:
                        ranklist_member_one['isplayer'] = 0

                    member_cnt += 1
                    ranklist_member_one['ranking'] = member_cnt
                    ranklist_member_one['count']   = firsts_player_info_one['count']

                    # get guild info
                    if ranklist_member_one['guild_id'] > 0:
                        ret, msg, member_guild_info = self.database.db_get_guild_by_guildID(ranklist_member_one['guild_id'])
                        if ret == 'success' and len(member_guild_info) > 0:
                            ranklist_member_one['guild_name'] = member_guild_info[0]['guild_name']
                            ranklist_member_one['guild_head'] = member_guild_info[0]['head']

                    else:
                        ranklist_member_one['guild_name'] = ""
                        ranklist_member_one['guild_head'] = ""

                    response['first'].append(ranklist_member_one)

                # get the members around the player ,  if the player not active, just get the first members
                ret,msg,around_player_info = self.database.db_get_ranklist_range(index, ranklist_offset, ranklist_number)
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(around_player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no index:%s.' %(index)
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get ranklist firsts player info: %s.' %(json.dumps(around_player_info)))
                response['ranklist'] = []
                member_cnt = ranklist_offset
                for around_player_info_one in around_player_info:
                    # get player info
                    ranklist_member_one = {}
                    ret,msg,member_info = self.database.db_get_player_by_id(around_player_info_one['playerID'])
                    if ret == 'success' and len(member_info) > 0:
                        ranklist_member_one['name'] = member_info[0]['name']
                        ranklist_member_one['head'] = member_info[0]['head']
                        ranklist_member_one['guild_id'] = member_info[0]['guildID']
                    else:
                        ranklist_member_one['name'] = ""
                        ranklist_member_one['head'] = ""
                        ranklist_member_one['guild_id'] = 0

                    if member_info[0]['account'] == player:
                        ranklist_member_one['isplayer'] = 1
                    else:
                        ranklist_member_one['isplayer'] = 0

                    member_cnt += 1
                    ranklist_member_one['ranking'] = member_cnt
                    ranklist_member_one['count']   = around_player_info_one['count']

                    # get guild info
                    if ranklist_member_one['guild_id'] > 0:
                        ret, msg, member_guild_info = self.database.db_get_guild_by_guildID(ranklist_member_one['guild_id'])
                        if ret == 'success' and len(member_guild_info) > 0:
                            ranklist_member_one['guild_name'] = member_guild_info[0]['guild_name']
                            ranklist_member_one['guild_head'] = member_guild_info[0]['head']

                    else:
                        ranklist_member_one['guild_name'] = ""
                        ranklist_member_one['guild_head'] = ""

                    response['ranklist'].append(ranklist_member_one)


                
                response['result'] = "success"
                return "%s" %(json.dumps(response)) 

            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 

        @bottle.route('/api/info/player/:playerid')
        def api_get_player_detal_info(playerid=None):
            response = {}
            response['result']  = 'error'

            try:
                self.logger.debug('handle a request: /api/info/player/:playerid')   
                self.logger.debug('playerid:%s, type:%s.' %(playerid,type(playerid)))   
                # check the params
                if playerid == None:
                    response['result'] = 'error'
                    response['message'] = 'params playerid is None.'
                    return "%s" %(json.dumps(response))


                post_data_json = {}
                post_data_json['player'] = playerid

                # get the player info , if not get player info ,just get by index
                ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                response['player'] = player_info[0]
                response['result'] = "success"
                return "%s" %(json.dumps(response)) 

            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 



        @bottle.route('/api/add/inviter', method="POST")
        def api_add_inviter():
            response = {}
            response['result'] = 'error'

            try:
                self.logger.debug('handle a request:/api/add/inviter')   
                # get the data
                post_data = bottle.request.body.getvalue()
                self.logger.debug('handle the request data: %s' %(post_data))

                '''
                    post data format:
                    {
                        "inviter": 123456,
                        "player" : "xxx"
                    }

                '''
                post_data_json = json.loads(post_data)

                # check must key
                if not post_data_json.has_key('player'):
                    response['result'] = 'error'
                    response['message'] = 'need param: player.'
                    return "%s" %(json.dumps(response)) 

                if not post_data_json.has_key('inviter'):
                    response['result'] = 'error'
                    response['message'] = 'need param: inviter.'
                    return "%s" %(json.dumps(response)) 

                self.logger.debug('get player info') 
                # get the player info
                ret,msg,player_info = self.database.db_get_player_by_openid(post_data_json['player'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                if len(player_info) < 1:
                    response['result'] = 'error'
                    response['message'] = 'there is no player for id:%s.' %(post_data_json['player'])
                    return "%s" %(json.dumps(response)) 

                else:
                    self.logger.debug('Get player info: %s.' %(json.dumps(player_info)))

                    # if the player has not been invited, add the inviter
                    if player_info[0]['inviter'] == 0:
                        update_player_params = {}
                        update_player_params['player_openid'] = post_data_json['player']
                        update_player_params['inviter'] = post_data_json['inviter']

                        ret,msg = self.database.db_update_player_info(update_player_params)
                        if ret != 'success':
                            response['result'] = 'error'
                            response['message'] = 'update the player info error:%s.' %(msg)
                            return "%s" %(json.dumps(response))           
                    else:
                        response['result'] = 'error'
                        response['message'] = 'the player has been invited by player:%s.' %(player_info[0]['inviter'])
                        return "%s" %(json.dumps(response)) 


                response['result'] = 'success'
                return "%s" %(json.dumps(response))

            except Exception,ex:
                response = {}
                response['result'] = 'error'
                response['message'] = '%s' %(str(ex))
                return "%s" %(json.dumps(response)) 


        @bottle.route('/api/number/inviter/:playerid')
        def api_get_number_of_inviters(playerid=None):
            response = {}
            response['result']  = 'error'

            try:
                self.logger.debug('handle a request: /api/number/inviter/:playerid')   
                self.logger.debug('playerid:%s, type:%s.' %(playerid,type(playerid)))   
                # check the params
                if playerid == None:
                    response['result'] = 'error'
                    response['message'] = 'params playerid is None.'
                    return "%s" %(json.dumps(response))


                post_data_json = {}
                post_data_json['player'] = playerid

                # get the player info , if not get player info ,just get by index
                ret,msg,number = self.database.db_get_number_of_inviters(post_data_json['player'])
                if ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'get player error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 

                response['number'] = number
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
    server = Server('0.0.0.0', 9092, logging.DEBUG)
    server.run()

else:
    #os.chdir(os.path.dirname(__file__))
    server = Server('0.0.0.0', 9090, logging.DEBUG)
    application = bottle.default_app()