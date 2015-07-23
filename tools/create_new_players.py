
import sys
sys.path.append("..")


import json
import time
import random
import os


from src.Database import Database
class Cplayer:

    base_alphabet = '23456789abcdefghijkmnpqrstuvwxyz'

    def __init__(self):
        self.database = Database()

    def add_one_name_and_value(self,inlist, name, value):
        one_in = {}
        one_in['name']  = name
        one_in['value'] = value
        inlist.append(one_in)

    
    def base62_encode(self, number, alphabet=base_alphabet):


        # the number must 'int'
        if not isinstance( number, int):
            return "error","number must int."

        if  number == 0:
            return 'success', '0'

        arr = []
        base = len(alphabet)
        while number:
            rem = number % base
            number = number // base
            arr.append(alphabet[rem])
        
        arr.reverse()

        return ''.join(arr)

    def GetFileList(self, FindPath):

        FileList=[]
        FileNames=os.listdir(FindPath)

        if (len(FileNames)>0):
            for fn in FileNames: 
                fullfilename="/images/player/head/%s" %fn
                FileList.append(fullfilename)
        return FileList

    def main(self):

        try:


            heads = self.GetFileList('/root/biubiuServer2/images/player/head')

            file = open("new_players.txt")

            cnt = 840
            while 1:
                name = file.readline()
                if not name:
                    break
                name=name.strip('\n')
                cnt += 1
                #print name + "cnt:%s" %cnt
                

                # get params
                player_params_list = []
                self.add_one_name_and_value(player_params_list, 'id', cnt)
                self.add_one_name_and_value(player_params_list, 'name', name)

                now = time.time()
                now *= 1000000000
                now = int(now) + cnt
                account =  self.base62_encode(now, self.base_alphabet)           
                self.add_one_name_and_value(player_params_list, 'account', account)
                self.add_one_name_and_value(player_params_list, 'accountID', cnt)
                self.add_one_name_and_value(player_params_list, 'gold', random.randint(200, 20000))
                self.add_one_name_and_value(player_params_list, 'level', 1)
                self.add_one_name_and_value(player_params_list, 'exp', random.randint(200, 20000))



                self.add_one_name_and_value(player_params_list, 'headurl', heads[random.randint(0, len(heads)-1)])

                print json.dumps(player_params_list)

                # create account
                account_params_list = []
                self.add_one_name_and_value(account_params_list, 'id', cnt)
                self.add_one_name_and_value(account_params_list, 'name', account)
                self.database.db_do_insert_commond('account',account_params_list)

                # create player
                self.database.db_do_insert_commond('player',player_params_list)
                self.database.db_do_insert_commond('player2',player_params_list)
                
                #break;
                time.sleep(0.1)
        except Exception,ex:
            print "ERROR:%s" %(ex)


app = Cplayer()
app.main()