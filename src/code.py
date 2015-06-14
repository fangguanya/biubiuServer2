#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Code:
    '''
        the return code for api.
        if code = 0, means ok;
        else means error
    '''

    ERROR_CODE_OK                   = 0        # OK

    ERROR_CODE_EXCEPTION            = 1000     # error for code exception
    ERROR_CODE_LICENSE              = 1001     # error for license

    ERROR_CODE_NEED_MUST_PARAMS     = 1100     # error for neet must params
    ERROR_CODE_CREATE_TOKEN         = 1101     # error for create token
    ERROR_CODE_FAILURE_TOKEN        = 1102     # error for failure token
    ERROR_CODE_PARAMS_ERROR         = 1103     # error for params

    # about database
    ERROR_CODE_DATABASE             = 1200     # error for database 
    ERROR_CODE_DATABASE_NO_PLAYER   = 1201     # error for database no player info get


    # about player
    ERROR_CODE_PLAYER_HAS_IN_GUILD       = 2000     # error for player has in guild 


    

