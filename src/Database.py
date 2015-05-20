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

    def db_search_guild(self, number):
        '''
            Search the guild, and return the guild list.
        '''
        try:
            result = []
            conn = None;
            ret, db = self.__connect_to_db();

            ret,conn = self.__create_connection(db);


            
            sql = "select guild2.id,guild2.name,guild2.head,level,guild2.limit,guild2.number,createrOpenID from guild2 where status!='delete';" 
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['guild_id'] = row[0]
                result_one['guild_name'] = row[1]

                result_one['level'] = row[3]
                result_one['people_limits'] = row[4]
                result_one['people_number'] = row[5]
                result_one['createrOpenID'] = row[6]

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
            
            sql = "select id,name,head,level,createTime,createrID,createrOpenID,exp,gold,gem,prop,province,city,county,longitude,latitude,guild2.limit,guild2.number from guild2 where guild2.id=%s;" \
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
                result_one['createrID'] = row[5]
                result_one['createrOpenID'] = row[6]
                result_one['exp'] = row[7]
                result_one['gold'] = row[8]
                result_one['gem'] = row[9]
                result_one['prop'] = row[10]
                result_one['province'] = row[11]
                result_one['city'] = row[12]
                result_one['county'] = row[13]
                result_one['longitude'] = row[14]
                result_one['latitude'] = row[15]
                result_one['people_limits'] = row[16]
                result_one['people_number'] = row[17]
              
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

            if  params.has_key('headID'):
                update_cmd = "%s headID=%s," %(update_cmd, params['headID'])

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
            sql = "select id, account, guildID from player where player.account='%s';"  %(openid)
            #Factory.logger.debug("[sql]%s" %(sql));
            print "sql: %s." %(sql)
            conn.execute(sql);

            dataset = conn.fetchall();

            for row in dataset:
                result_one = {}
                result_one['id'] = row[0]
                result_one['account'] = row[1]
                result_one['guildID'] = row[2]

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
            sql = 'UPDATE player SET '
            update_cmd = ''
            conn = None

            # check the must param
            if not params.has_key('player_openid'):
                return "error", "no must param: player_openid."


            if  params.has_key('guild_id'):
                update_cmd = "%s guildId=%s," %(update_cmd, params['guild_id'])


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

    def db_update_player_info_by_guildId(self, params,guild_id):
        '''
            Update player info by params
        '''  
        conn = None 
        try:
            sql = 'UPDATE player SET '
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
                update_cmd = "%s exp=%s," %(update_cmd, params['exp'])

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