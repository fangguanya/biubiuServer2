import os
import json
import MySQLdb
from datetime import datetime
import time

from Config import Config

class Database:

    def __connect_to_db(self):
        try:
            print "mysqlHost:%s, mysqlUser:%s, mysqlPassword:%s, mysqlDatabase:%s" %(Config.mysqlHost, 
                Config.mysqlUser, Config.mysqlPassword, Config.mysqlDatabase)
            db = MySQLdb.connect(host=Config.mysqlHost,user=Config.mysqlUser, 
                passwd=Config.mysqlPassword, db=Config.mysqlDatabase )

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
        try:
            # default params
            createrID = 0
            name = ''
            head = ''

            # check the params


            createrID = params['player']
            name = params['name']
            head = params['logo']

            conn = None;
            ret, db = self.__connect_to_db();
            print "__connect_to_db %s" %(ret)
            ret,conn = self.__create_connection(db);
            print "__create_connection %s" %(ret)

            # insert project
            sql = "insert into guild2(createrID, name, head, createTime, guild2.limit) values ('%s','%s','%s','%s','%s');" \
                %self.__escape_tuple(createrID,name,head,datetime.now(),"25");
            #Factory.logger.debug("[sql]%s" %(sql));
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
            
            return "success","ok",guild_id;

        except Exception,ex:
            if conn is not None:
                conn.close();

            return "error","not do",None
    
