#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import MySQLdb
from datetime import datetime
import time

from Config import Config
from Consts import Consts

class Database:

    player_id_offset = 121000

    def __connect_to_db(self):
        try:
            #print "mysqlHost:%s, mysqlUser:%s, mysqlPassword:%s, mysqlDatabase:%s" %(Config.mysqlHost, 
            #    Config.mysqlUser, Config.mysqlPassword, Config.mysqlDatabase)
            db = MySQLdb.connect(host=Config.mysqlHost,user=Config.mysqlUser, 
                passwd=Config.mysqlPassword, db=Config.mysqlDatabase, charset="utf8")

        except Exception,ex:
            summary = "connect to db '%s' failed. host=%s." %(Config.mysqlDatabase, Config.mysqlHost)
            # need to use logging to log
            print summary
            return "error",ex
            
        return "success",db;
    
    def __create_connection(self, db):
        try:
            conn = db.cursor();
            
            conn.execute("SET NAMES utf8");
            # no need to set the following two, the set names will do this.
            #conn.execute("SET CHARACTER_SET_CLIENT=utf8");
            #conn.execute("SET CHARACTER_SET_RESULTS=utf8");
            
            db.commit();
            
            return "success",conn

        except Exception,ex:
            print "__create_connection error: %s" %(ex)
            return "error",ex


    def __escape_tuple(self, *input_tuple):
        '''
        [private] escape all args.
        '''
        try:
            escaped_arr = [];
            
            for i in input_tuple:
                escaped_arr.append(MySQLdb.escape_string(str(i)));
            
            return tuple(escaped_arr);

        except Exception,ex:
            print "__escape_tuple error: %s" %(ex)
            return input_tuple


    def db_do_update_commond(self, sql=None):
        '''
            Update 
        '''  
        conn = None 
        try:

            conn = None

            if sql == None:
                return "error","sql None"

            print sql

            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);
            ret = conn.execute(sql);
            
            db.commit();

            if conn is not None:
                conn.close(); 

            return "success","ok"


        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex) 


    def db_do_select_commond(self, sql=None):
        '''
            select
        '''
        try:
            result = []
            conn = None;

            if sql == None:
                return "error","sql None",[]

            ret, db = self.__connect_to_db();

            ret,conn = self.__create_connection(db);

            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            if conn is not None:
                conn.close(); 

            
            return "success","ok",dataset

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error","not do",None

    def __string_value_list(self,value_list):

        try:
            string_name_list = ''
            string_value_list = ''

            '''
                value_list format:
                [{"name":"port", "value":9090},{"name":"server","value":"10.33.0.123"}]
            '''
            value_cnt = 0
            for value_one in value_list:

                if value_cnt == 0:
                    string_name_list = "{0}".format(value_one['name'])
                    if isinstance(value_one['value'], basestring):
                        string_value_list = "'{0}'".format(value_one['value'])
                    else:
                        string_value_list = "{0}".format(value_one['value'])
                    value_cnt += 1
                else:
                    string_name_list = "{0},{1}".format(string_name_list, value_one['name'])
                    if isinstance(value_one['value'], basestring):
                        string_value_list = "{0},'{1}'".format(string_value_list, value_one['value'])
                    else:
                        string_value_list = "{0}, {1}".format(string_value_list, value_one['value'])

            return 'success',string_name_list,string_value_list
        except Exception,ex:
            return 'error',str(ex),str(ex)

    def db_do_insert_commond(self, table_name, value_list):
        result = 'error'

        try:

            result, name_list_string, value_list_string = self.__string_value_list(value_list)
            if result != 'success':
                print "db_do_insert_commond, __string_where_list error:%s" %name_list_string
                return result,name_list_string  


            ret, db = self.__connect_to_db();

            ret,conn = self.__create_connection(db);
            
            sql = "INSERT INTO {0}({1})  VALUES({2});".format(table_name, name_list_string, value_list_string)

            print "[db_do_insert_commond]%s" %(sql)
            conn.execute(sql);
            db.commit()

            if conn is not None:
                conn.close(); 

            result = 'success'
            return result,'success'
        except Exception,ex:
            if conn is not None:
                conn.close()
            db.rollback()

            msg = "error:%s." %(str(ex))
            print "db_do_insert_commond, %s" %msg
            return result,msg   

    def db_create_guild(self, params):
        '''
            Create the guild, and return the guild id.
        '''
        conn = None 
        try:
            # default params
            createrID = 0
            name = ''
            head = ''

            # check the params

            if params.has_key('player'):
                createrOpenID = params['player']

            if params.has_key('name'):
                name = params['name'].encode('utf-8')

            if params.has_key('logo'):
                head = params['logo']

            ret, db = self.__connect_to_db();
            #print "__connect_to_db %s" %(ret)
            ret,conn = self.__create_connection(db);
            #print "__create_connection %s" %(ret)

            # insert project
            sql = "insert into guild2(createrOpenID, name, head, createTime, guild2.limit, guild2.status) values ('%s','%s','%s','%s','%s','%s');" \
                %self.__escape_tuple(createrOpenID,name,head,datetime.now(),"25", Consts.guild_status_active);

            print "sql: %s." %(sql)
            conn.execute(sql);
            
            # get the project id.
            conn.execute("select @@identity;");
            source_id_ret = conn.fetchone();
            if source_id_ret is None or len(source_id_ret) < 1:
                #raise TVieException(Consts.error_db_create_source_failed, "create transcode task failed! name=%s items=%s" %(name_str,items_str));
                msg = "create guild failed!"
                print msg
                #Factory.logger.error("%s" %(msg));
                return "error",msg, None
        
            db.commit();
            
            guild_id = source_id_ret[0];
            
            if conn is not None:
                conn.close(); 

            return "success","ok",guild_id;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error","not do",None

    def db_search_guild(self, offset=0, number=25):
        '''
            Search the guild, and return the guild list.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();

            ret,conn = self.__create_connection(db);


            
            sql = "select guild2.id,guild2.name,guild2.head,level,guild2.limit,guild2.number,createrOpenID,exp from guild2 where status!='delete' order by exp desc limit %s,%s;" %(offset, number)
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['guild_id'] = row[0]
                result_one['guild_name'] = row[1]
                result_one['head'] = row[2]
                result_one['level'] = row[3]
                result_one['people_limits'] = row[4]
                result_one['people_number'] = row[5]
                result_one['createrOpenID'] = row[6]
                result_one['exp'] = row[7]

                result_one['if_in_guild'] = 0
                result.append(result_one)

            if conn is not None:
                conn.close(); 

            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error","not do",None

    def db_search_guild2(self, params):
        '''
            Search the guild, and return the guild list.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();

            ret,conn = self.__create_connection(db);

            select_string = "id,name,head,level,guild2.limit,guild2.number,createrOpenID,exp,gold"
            if params.has_key('sort_type'):
                if params['sort_type'] == 'members_exp':
                    select_string = "%s,(select sum(exp) from guildMember2 where guildID=guild2.id and status='active') as members_exp " %(select_string)
            sql = "select %s from guild2 where status!='delete'" %(select_string)

            # where
            if params.has_key('mode'):
                if params['mode'] == 'city':
                    if params.has_key('city_id'):
                        city_id = str(params['city_id'])
                        if len(city_id) == 4 or len(city_id) == 6:
                            sql = "%s and province=%s and city=%s " %(sql, city_id[:2], city_id[2:4])

            if params.has_key('head'):
                sql = "%s and head='%s' " %(sql, params['head'])
            

            # order by
            if params.has_key('sort_type'):
                if params['sort_type'] in ['exp', 'level', 'gold', 'number', 'members_exp']:
                    sql = "%s order by %s desc" %(sql, params['sort_type'])

                elif params['sort_type'] == 'duration_exp':
                    sql = "%s order by exp-last_exp desc" %(sql)

                elif params['sort_type'] == 'id':
                    sql = "%s order by id " %(sql)

                else:
                    sql = "%s order by exp " %(sql)


            # limit
            if params.has_key('range_min') and params.has_key('range_max'):
                if params['range_min'] != 0 and params['range_max'] != 0 and params['range_max'] >= params['range_min']:
                    sql = "%s limit %s,%s" %(sql, params['range_min']-1, params['range_max']-params['range_min']+1)

            
            sql = "%s;" %(sql)

            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['guild_id'] = row[0]
                result_one['guild_name'] = row[1]
                result_one['head'] = row[2]
                result_one['level'] = row[3]
                result_one['people_limits'] = row[4]
                result_one['people_number'] = row[5]
                result_one['createrOpenID'] = row[6]
                result_one['exp'] = row[7]
                result_one['gold'] = row[8]

                result_one['if_in_guild'] = 0
                result.append(result_one)

            if conn is not None:
                conn.close(); 

            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error","not do",None


    def db_get_guild_by_guildID(self, guildID):
        '''
            Get the guild, and return the guild info.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            
            ret,conn = self.__create_connection(db);
            
            sql = "select id,name,head,level,createTime,createrID,createrOpenID,exp,gold,gem,prop,province,city,county,longitude,latitude,guild2.limit,guild2.number,address from guild2 where guild2.id=%s;" \
                %(guildID)

            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['guild_id'] = row[0]
                result_one['guild_name'] = row[1]
                result_one['head'] = row[2]
                result_one['level'] = row[3]
                result_one['createTime'] = str(row[4])
                result_one['createrID'] = row[5]+self.player_id_offset
                result_one['createrOpenID'] = row[6]
                result_one['exp'] = row[7]
                result_one['gold'] = row[8]
                result_one['gem'] = row[9]
                result_one['prop'] = json.loads(row[10])
                result_one['province'] = row[11]
                result_one['city'] = row[12]
                result_one['county'] = row[13]
                result_one['longitude'] = row[14]
                result_one['latitude'] = row[15]
                result_one['people_limits'] = row[16]
                result_one['people_number'] = row[17]
                result_one['address'] = row[18]
              
                result.append(result_one)

            if conn is not None:
                conn.close(); 

            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),None
     
    def db_update_guild_info(self, params):
        '''
            Update guild info by params
        '''  
        conn = None 
        try:
            sql = 'UPDATE guild2 SET '
            update_cmd = ''
            conn = None

            # check the must params
            if  not params.has_key('guild_id'):
                return "error", "need must param: guild_id. "

            if  params.has_key('head'):
                update_cmd = "%s head='%s'," %(update_cmd, params['head'])

            if  params.has_key('name'):
                update_cmd = "%s name='%s'," %(update_cmd, params['name'])

            if  params.has_key('headID'):
                update_cmd = "%s headID=%s," %(update_cmd, params['headID'])

            if  params.has_key('createrOpenID'):
                update_cmd = "%s createrOpenID='%s'," %(update_cmd, params['createrOpenID'])

            if  params.has_key('province'):
                update_cmd = "%s province=%s," %(update_cmd, params['province'])

            if  params.has_key('city'):
                update_cmd = "%s city=%s," %(update_cmd, params['city'])

            if  params.has_key('county'):
                update_cmd = "%s county=%s," %(update_cmd, params['county'])

            if  params.has_key('longitude'):
                update_cmd = "%s longitude=%s," %(update_cmd, params['longitude'])

            if  params.has_key('latitude'):
                update_cmd = "%s latitude=%s," %(update_cmd, params['latitude'])                     

            if  params.has_key('number'):
                update_cmd = "%s number=%s," %(update_cmd, params['number'])

            if  params.has_key('status'):
                update_cmd = "%s status='%s'," %(update_cmd, params['status'])



            if  params.has_key('exp'):
                update_cmd = "%s exp=%s," %(update_cmd, params['exp'])

            if  params.has_key('gold'):
                update_cmd = "%s gold=%s," %(update_cmd, params['gold'])

            if  params.has_key('gem'):
                update_cmd = "%s gem=%s," %(update_cmd, params['gem'])

            if  params.has_key('prop'):
                update_cmd = "%s prop='%s'," %(update_cmd, params['prop'])    


            if  params.has_key('address'):
                #update_cmd = "%s address='%s'," %(update_cmd, params['address']) 
                update_cmd = "{0} address='{1}',".format(update_cmd, params['address'])

            if  len(update_cmd) > 0:
                sql = "%s %s where id=%s;" %(sql, update_cmd[:-1], params['guild_id'])
            else:
                return "error","no param can be set"


            print sql

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);
            ret = conn.execute(sql);
            
            db.commit();

            if conn is not None:
                conn.close(); 

            return "success","ok"


        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex)    

    def db_add_player(self, params):
        '''
            add the player, and return the player id.
        '''
        conn = None
        try:
            # check the params
            '''
            {
                "openid"   : "OPENID",
                "openkey"  : "OPEN_KEY",
                "name"     : "The player name(nickname)",
                "head_url" : "http://ip/the_player_head_url"
            }
            '''

            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            sql = "insert into player2(id, account, name, headurl, login) values (%s,'%s','%s','%s','%s');" \
                %self.__escape_tuple(params['id'],params['openid'],params['name'].encode('utf-8'),params['head_url'], datetime.now());

            print "sql: %s." %(sql)
            conn.execute(sql);

            # get the project id.
            conn.execute("select @@identity;");
            source_id_ret = conn.fetchone();
            if source_id_ret is None or len(source_id_ret) < 1:
                msg = "add player failed!"
                print msg
                return "error",msg, None
        
            db.commit();
            
            player_id = source_id_ret[0];

            return "success","ok",player_id;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),None


    def db_get_player_by_openid(self, openid):
        '''
            get the player info by openid.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            # insert project
            sql = "select id, account, guildID, name, headurl, level, gold, exp, gem, prop, inviter,modify_cnt from player2 where player2.account='%s';"  %(openid)
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['id']      = row[0]+self.player_id_offset
                result_one['account'] = row[1]
                result_one['guildID'] = row[2]
                result_one['name']    = row[3]
                result_one['head']    = row[4]
                result_one['level']   = row[5]

                result_one['gold']   = row[6]
                result_one['exp']    = row[7]
                result_one['gem']    = row[8]
                result_one['prop']   = json.loads(row[9])
                result_one['inviter']    = row[10]
                result_one['modify_cnt']    = row[11]


                #print result_one
                result.append(result_one)

            if conn is not None:
                conn.close(); 


            if len(result) < 1:
                ret,msg,player_info = self.db_get_player_from_socket_server_by_openid(openid)
                if ret == 'success' and len(player_info) >= 1:
                    player_params = {}
                    player_params['id'] = player_info[0]['id']-self.player_id_offset
                    player_params['openid'] = player_info[0]['account']
                    player_params['name'] = player_info[0]['name']
                    player_params['head_url'] = player_info[0]['head']

                    ret,msg,player_id = self.db_add_player(player_params)
                    if ret == 'success':
                        result = player_info


            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result

    def db_get_player_from_socket_server_by_openid(self, openid):
        '''
            get the player info by openid.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            # insert project
            sql = "select id, account, guildID, name, headurl, level, gold, exp, gem, prop, inviter,modify_cnt from player where player.account='%s';"  %(openid)
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['id']      = row[0]+self.player_id_offset
                result_one['account'] = row[1]
                result_one['guildID'] = row[2]
                result_one['name']    = row[3]
                result_one['head']    = row[4]
                result_one['level']   = row[5]

                result_one['gold']   = row[6]
                result_one['exp']    = row[7]
                result_one['gem']    = row[8]
                result_one['prop']   = json.loads(row[9])
                result_one['inviter']    = row[10]
                result_one['modify_cnt']    = row[11]


                #print result_one
                result.append(result_one)

            if conn is not None:
                conn.close(); 
            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result

    def db_get_player_by_id(self, playerid):
        '''
            get the player info by openid.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            # insert project
            sql = "select id, account, guildID, name, headurl, level, gold, exp, gem, prop, inviter from player2 where player2.id=%s;"  %(playerid-self.player_id_offset)
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['id']      = row[0]+self.player_id_offset
                result_one['account'] = row[1]
                result_one['guildID'] = row[2]
                result_one['name']    = row[3]
                result_one['head']    = row[4]
                result_one['level']   = row[5]

                result_one['gold']   = row[6]
                result_one['exp']    = row[7]
                result_one['gem']    = row[8]
                result_one['prop']   = json.loads(row[9])
                result_one['inviter']    = row[10]  


                #print result_one
                result.append(result_one)

            if conn is not None:
                conn.close(); 
            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result

    def db_get_player_from_socket_server_by_id(self, playerid):
        '''
            get the player info by openid.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            # insert project
            sql = "select id, account, guildID, name, headurl, level, gold, exp, gem, prop, inviter from player where player.id=%s;"  %(playerid-self.player_id_offset)
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['id']      = row[0]+self.player_id_offset
                result_one['account'] = row[1]
                result_one['guildID'] = row[2]
                result_one['name']    = row[3]
                result_one['head']    = row[4]
                result_one['level']   = row[5]

                result_one['gold']   = row[6]
                result_one['exp']    = row[7]
                result_one['gem']    = row[8]
                result_one['prop']   = json.loads(row[9])
                result_one['inviter']    = row[10]  


                #print result_one
                result.append(result_one)

            if conn is not None:
                conn.close(); 
            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result


    def db_update_player_info(self, params):
        '''
            Update player info by params
        '''  
        conn = None 
        try:
            sql = 'UPDATE player2 SET '
            update_cmd = ''
            conn = None

            # check the must param
            if not params.has_key('player_openid'):
                return "error", "no must param: player_openid."


            # the flag for if need modify the modify_cnt
            modify_cnt_flag = 0


            if  params.has_key('guild_id'):
                update_cmd = "%s guildId=%s," %(update_cmd, params['guild_id'])
                modify_cnt_flag += 1

            if  params.has_key('exp'):
                update_cmd = "%s exp=%s," %(update_cmd, params['exp'])
                modify_cnt_flag += 1

            if  params.has_key('gold'):
                update_cmd = "%s gold=%s," %(update_cmd, params['gold'])
                modify_cnt_flag += 1

            if  params.has_key('prop'):
                update_cmd = "%s prop='%s'," %(update_cmd, params['prop'])
                modify_cnt_flag += 1

            if  params.has_key('gem'):
                update_cmd = "%s gem=%s," %(update_cmd, params['gem'])
                modify_cnt_flag += 1

            if  params.has_key('inviter'):
                update_cmd = "%s inviter=%s," %(update_cmd, params['inviter'])
                modify_cnt_flag += 1

            if  params.has_key('token'):
                update_cmd = "%s token='%s'," %(update_cmd, params['token'])


            if  modify_cnt_flag > 0:
                update_cmd = "%s modify_cnt=modify_cnt+%s," %(update_cmd, modify_cnt_flag)

                
            if  len(update_cmd) > 0:
                sql = "%s %s where account='%s';" %(sql, update_cmd[:-1], params['player_openid'])
            else:
                return "error","no param can be set"


            print sql

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);
            ret = conn.execute(sql);
            
            db.commit();

            if conn is not None:
                conn.close(); 

            return "success","ok"


        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex)    

    def db_update_player_info_by_id(self, params):
        '''
            Update player info by params
        '''  
        conn = None 
        try:
            sql = 'UPDATE player2 SET '
            update_cmd = u""
            conn = None

            # the flag for if need modify the modify_cnt
            modify_cnt_flag = 0

            # check the must param
            if not params.has_key('id'):
                return "error", "no must param: id."


            if  params.has_key('guild_id'):
                update_cmd = "%s guildId=%s," %(update_cmd, params['guild_id'])
                modify_cnt_flag += 1

            if  params.has_key('exp'):
                update_cmd = "%s exp=%s," %(update_cmd, params['exp'])
                modify_cnt_flag += 1

            if  params.has_key('gold'):
                update_cmd = "%s gold=%s," %(update_cmd, params['gold'])
                modify_cnt_flag += 1

            if  params.has_key('prop'):
                update_cmd = "%s prop='%s'," %(update_cmd, params['prop'])
                modify_cnt_flag += 1

            if  params.has_key('gem'):
                update_cmd = "%s gem=%s," %(update_cmd, params['gem'])
                modify_cnt_flag += 1

            if  params.has_key('inviter'):
                update_cmd = "%s inviter=%s," %(update_cmd, params['inviter'])
                modify_cnt_flag += 1

            if  params.has_key('token'):
                update_cmd = "%s token='%s'," %(update_cmd, params['token'])

            if  params.has_key('login'):
                update_cmd = "%s login='%s'," %(update_cmd, params['login'])

            if  modify_cnt_flag > 0:
                update_cmd = "%s modify_cnt=modify_cnt+%s," %(update_cmd, modify_cnt_flag)

            if  params.has_key('name'):
                print type(params['name'])
                #print params['name']
                params['name'] = params['name'].encode('utf-8')
                print type(params['name'])
                print params['name']
                #update_cmd = "%s name='%s'," %self.__escape_tuple(update_cmd, params['name'])
                update_cmd = "{0} name='{1}',".format(update_cmd.encode('utf-8'), params['name'])

                print update_cmd
                print type(update_cmd)

            if  params.has_key('headurl'):
                #update_cmd = "%s headurl='%s'," %(update_cmd.encode('utf-8'), params['headurl'])
                update_cmd = "{0} headurl='{1}',".format(update_cmd, params['headurl'])




            if  len(update_cmd) > 0:
                sql = "%s %s where id='%s';" %(sql, update_cmd[:-1], params['id']-self.player_id_offset)
            else:
                return "error","no param can be set"


            print sql

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);
            ret = conn.execute(sql);
            
            db.commit();

            if conn is not None:
                conn.close(); 

            return "success","ok"


        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex)    



    def db_update_player_info_by_guildId(self, params,guild_id):
        '''
            Update player info by params
        '''  
        conn = None 
        try:
            sql = 'UPDATE player2 SET '
            update_cmd = ''
            conn = None


            if  params.has_key('guild_id'):
                update_cmd = "%s guildId='%s'," %(update_cmd, params['guild_id'])


            if  len(update_cmd) > 0:
                sql = "%s %s where guildId=%s;" %(sql, update_cmd[:-1], guild_id)
            else:
                return "error","no param can be set"


            print sql

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);
            ret = conn.execute(sql);
            
            db.commit();

            if conn is not None:
                conn.close(); 

            return "success","ok"


        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex)    



    def db_create_guildMember(self, params):
        '''
            Create the guild member, and return the guild member id.
        '''
        conn = None
        try:
            # check the params
            guildID = params['guild_id']
            playerID = params['player_id']
            playerOpenID = params['player']

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            sql = "insert into guildMember2(guildID, playerID, playerOpenID, status, createTime) values ('%s','%s','%s','%s','%s');" \
                %self.__escape_tuple(guildID,playerID,playerOpenID, Consts.guildMember_status_active, datetime.now());

            print "sql: %s." %(sql)
            conn.execute(sql);

            # get the project id.
            conn.execute("select @@identity;");
            source_id_ret = conn.fetchone();
            if source_id_ret is None or len(source_id_ret) < 1:
                #raise TVieException(Consts.error_db_create_source_failed, "create transcode task failed! name=%s items=%s" %(name_str,items_str));
                msg = "create guild failed!"
                print msg
                #Factory.logger.error("%s" %(msg));
                return "error",msg, None
        
            db.commit();
            
            guildMemver_id = source_id_ret[0];

            return "success","ok",guildMemver_id;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),None

    def db_get_guildMembers_by_guildID(self, guildID):
        '''
            get the guildMembers.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            sql = "select playerOpenID, exp from guildMember2 where guildID=%s and status='%s' order by exp desc;"  %(guildID, Consts.guildMember_status_active)
            
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['openid'] = row[0]
                result_one['guild_exp'] = row[1]

                result_one['iscreater'] = 0
                result.append(result_one)

            if conn is not None:
                conn.close(); 
            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result

    def db_update_guildMember_info(self, params):
        '''
            Update guildMember info by params
        '''  
        conn = None 
        try:
            sql = 'UPDATE guildMember2 SET '
            update_cmd = ''
            conn = None

            # check the must params
            if  not params.has_key('guild_id'):
                return "error","no param: guild_id"

            if  not params.has_key('player_openid'):
                return "error","no param: player_openid"

            if  params.has_key('exp'):
                update_cmd = "%s exp=exp+(%s)," %(update_cmd, params['exp'])

            if  params.has_key('status'):
                update_cmd = "%s status='%s'," %(update_cmd, params['status'])


            if  len(update_cmd) > 0:
                sql = "%s %s where playerOpenID='%s' and guildID=%s;" %(sql, update_cmd[:-1], params['player_openid'], params['guild_id'])
            else:
                return "error","no param can be set"


            print sql

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);
            ret = conn.execute(sql);
            
            db.commit();

            if conn is not None:
                conn.close(); 

            return "success","ok"


        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex)   


    def db_update_all_guildMember_info(self, params):
        '''
            Update guildMember info by params
        '''  
        conn = None 
        try:
            sql = 'UPDATE guildMember2 SET '
            update_cmd = ''
            conn = None

            # check the must params
            if  not params.has_key('guild_id'):
                return "error","no param: guild_id"

            if  params.has_key('exp'):
                update_cmd = "%s exp=%s," %(update_cmd, params['exp'])

            if  params.has_key('status'):
                update_cmd = "%s status='%s'," %(update_cmd, params['status'])


            if  len(update_cmd) > 0:
                sql = "%s %s where guildID=%s;" %(sql, update_cmd[:-1], params['guild_id'])
            else:
                return "error","no param can be set"


            print sql

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);
            ret = conn.execute(sql);
            
            db.commit();

            if conn is not None:
                conn.close(); 

            return "success","ok"


        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex)   


    def db_create_license(self, params):
        '''
            Create the license
        '''
        conn = None
        try:
            # check must params
            logo = params['logo']
            name = params['name'].encode('utf-8')
            license = params['license']

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            sql = "insert into license(logo, name, license, status, createTime) values ('%s','%s','%s','%s','%s');" \
                %self.__escape_tuple(logo, name, license, Consts.license_active, datetime.now());

            print "sql: %s." %(sql)
            conn.execute(sql);

            # get the project id.
            conn.execute("select @@identity;");
            source_id_ret = conn.fetchone();
            if source_id_ret is None or len(source_id_ret) < 1:
                #raise TVieException(Consts.error_db_create_source_failed, "create transcode task failed! name=%s items=%s" %(name_str,items_str));
                msg = "create guild failed!"
                print msg
                #Factory.logger.error("%s" %(msg));
                return "error",msg, None
        
            db.commit();
            
            guildMemver_id = source_id_ret[0];

            return "success","ok",guildMemver_id;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),None

    def db_get_license(self, license):
        '''
            get the license info.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            sql = "select logo, name, status, playerID, playerOpenID from license where license='%s';"  %(license)
            
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['logo'] = row[0]
                result_one['name'] = row[1]
                result_one['status'] = row[2]
                result_one['playerID'] = row[3]+self.player_id_offset
                result_one['playerOpenID'] = row[4]


                result.append(result_one)

            if conn is not None:
                conn.close(); 
            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result


    def db_update_license(self, params):
        '''
            update the license
        '''
        conn = None 
        try:
            sql = 'UPDATE license SET '
            update_cmd = ''
            conn = None

            # check the must params
            if  not params.has_key('license'):
                return "error","no param: license"

            if  not params.has_key('playerOpenID'):
                return "error","no param: playerOpenID"

            if  params.has_key('playerOpenID'):
                update_cmd = "%s playerOpenID='%s'," %(update_cmd, params['playerOpenID'])

            if  params.has_key('playerID'):
                update_cmd = "%s playerID=%s," %(update_cmd, params['playerID']-self.player_id_offset)

            if  params.has_key('status'):
                update_cmd = "%s status='%s'," %(update_cmd, params['status'])

                if params['status'] == Consts.license_used:
                    update_cmd = "%s usedTime='%s'," %(update_cmd, datetime.now())


            if  len(update_cmd) > 0:
                sql = "%s %s where license='%s';" %(sql, update_cmd[:-1], params['license'])
            else:
                return "error","no param can be set"


            print sql

            
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);
            ret = conn.execute(sql);
            
            db.commit();

            if conn is not None:
                conn.close(); 

            return "success","ok"


        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex)   



    def db_get_ranklist_top(self, index, number):
        '''
            get the ranklist.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            # insert project
            sql = "select playerID, playerNamebrand.index, playerNamebrand.count from playerNamebrand where playerNamebrand.index=%s order by playerNamebrand.count desc limit 0,%s;"  %(index,number)
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['playerID'] = row[0]+self.player_id_offset
                result_one['index'] = row[1]
                result_one['count'] = row[2]


                #print result_one
                result.append(result_one)

            if conn is not None:
                conn.close(); 
            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result


    def db_get_ranklist_range(self, index, offset, number, sort_type='exp'):
        '''
            get the ranklist.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            if sort_type == 'exp':
                sql = "select playerID, playerNamebrand.index, playerNamebrand.count,success from playerNamebrand where playerNamebrand.index=%s order by playerNamebrand.count desc limit %s,%s;"  %(index,offset,number)
            else:
                sql = "select playerID, playerNamebrand.index, playerNamebrand.count,success from playerNamebrand where playerNamebrand.index=%s order by playerNamebrand.success desc limit %s,%s;"  %(index,offset,number)

            
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['playerID'] = row[0]+self.player_id_offset
                result_one['index'] = row[1]
                result_one['count'] = row[2]
                result_one['success'] = row[3]


                #print result_one
                result.append(result_one)

            if conn is not None:
                conn.close(); 
            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result


    def db_get_ranking_number(self, index, playerID, sort_type='exp'):
        '''
            get the ranklist.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            if sort_type == 'exp':
                sql = "select id,playerID,number from (select id, playerID, playerNamebrand.index, count, (@number:=@number+1) as number from playerNamebrand,(select (@number:=0)) b where playerNamebrand.index=%s order by count desc) c where playerID=%s;"  %(index,playerID-self.player_id_offset)
            else:
                sql = "select id,playerID,number from (select id, playerID, playerNamebrand.index, count, (@number:=@number+1) as number from playerNamebrand,(select (@number:=0)) b where playerNamebrand.index=%s order by success desc) c where playerID=%s;"  %(index,playerID-self.player_id_offset)
            
            
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['id'] = row[0]+self.player_id_offset
                result_one['playerID'] = row[1]
                result_one['number'] = int(row[2])


                #print result_one
                result.append(result_one)

            if conn is not None:
                conn.close(); 
            
            return "success","ok",result;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result


    def db_get_ranking_members_number(self, index):
        '''
            get the ranklist members number
        '''
        try:
            result = []
            count = 0
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);


            # insert project
            sql = "select count(id) from playerNamebrand where playerNamebrand.index=%s;"  %(index)
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                count = row[0]

            if conn is not None:
                conn.close(); 
            
            return "success","ok",count;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),count



    def db_get_number_of_inviters(self, playerid):
        '''
            get the number of inviter.
        '''
        try:
            number = 0
            conn = None;
            ret, db = self.__connect_to_db();
            ret,conn = self.__create_connection(db);

            sql = "select count(inviter) from player2 where inviter=%s;"  %(int(playerid)-self.player_id_offset)
            
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                number = row[0]

            if conn is not None:
                conn.close(); 
            
            return "success","ok",number;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error",str(ex),result

