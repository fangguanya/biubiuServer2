
import os
import socket
import subprocess


class Utility:
    ''' class utility '''
    base62_alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base64_alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-/'
    base56_alphabet = '23456789abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'


    def __init__(self):
        # save the os name for utest to mock it.
        self.os_name = os.name;


    def get_host_name(self):
        '''
        [public] get the hostname of current machine.
        '''
        return socket.gethostname();
    
    def get_ip_list(self):
        '''
        [public] get the ip list of current machine.
        sometimes it always return "127.0.0.1".
        '''
        #hostname, aliaslist, ipaddrlist
        try:
            host = socket.gethostbyname_ex(self.get_host_name());
            
            if len(host) < 3:
                raise Exception("failed to get ip list: %s" %(host));
            
            return host[2];
        except:
            return [];


    def do_command(self, cmd):
        '''
            do_command will use subprocess to do command, and then return the command return info.
        '''
        try:
            child = subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
            (out_data,out_err) = child.communicate() 

            return 'success',out_data
        except Exception,ex:
            return 'error',str(ex)


    def base62_encode(self, number, alphabet=base62_alphabet):
        '''
            Default: encode a number in base 62. user can define alphabet for base x.
            'num': The number to encode
            'alphabet': The alphabet to use for encoding
        '''
        try:

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
            return 'success',''.join(arr)

        except Exception,ex:
            return 'error',str(ex)

    def base62_decode(self, nstr, alphabet=base62_alphabet):
        '''
            Decode a Base X encoded string into the number
        '''
        try:

            base = len(alphabet)
            strlen = len(nstr)
            num = 0

            idx = 0
            for char in nstr:
                power = (strlen - (idx + 1))
                num += alphabet.index(char) * (base ** power)
                idx += 1

            return "success",num


        except Exception,ex:
            return 'error',str(ex)

    def base56_encode(self, number, alphabet=base56_alphabet):
        '''
            Default: encode a number in base 56. user can define alphabet for base x.
            'num': The number to encode
            'alphabet': The alphabet to use for encoding
        '''
        try:

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
            return 'success',''.join(arr)

        except Exception,ex:
            return 'error',str(ex)
