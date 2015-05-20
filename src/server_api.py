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



        @bottle.route('/api/verify/license', method="POST")
        def api_verify_license():
            response = {}
            response['result'] = 'error'
            response['logo_url'] = ''

            # just for test
            response['result'] = 'success'
            response['logo_url'] = '/images/agency/teamnxxt.png'
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
                ret, msg, guild_id = self.database.db_create_guild(post_data_json)
                if  ret != 'success':
                    response['result'] = 'error'
                    response['message'] = 'create guild error:%s.' %(msg)
                    return "%s" %(json.dumps(response)) 
                else:
                    self.logger.debug('guild create success, id: %s' %(guild_id))



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
                    ret,msg,guilds = self.database.db_search_guild(20)
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
            response['result'] = 'error'

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

                response['result'] = "success"
                response['guild_info'] = guild_info
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


    def run(self):
        bottle.run(host=self.ip, port=self.port, debug=True)



if __name__ == "__main__":
    server = Server('0.0.0.0', 80, logging.DEBUG)
    server.run()

else:
    #os.chdir(os.path.dirname(__file__))
    server = Server('0.0.0.0', 80, logging.DEBUG)
    application = default_app()