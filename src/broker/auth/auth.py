# -*- coding: utf-8 -*-

""" Basic access and management for pyhomebroker APIs """

__all__ = ['Auth']
__version__ = '0.0.1'
__author__ = 'fgr-17'

import os
from operator import itemgetter

class Auth:
    """ pyhomebroker auth data """

    def __init__(self, id_num, usr, pwd, acc):
        self.id_num = id_num
        self.usr = usr
        self.pwd = pwd
        self.acc = acc

        self.print()


    @classmethod
    def from_file(cls, filename):
        """ Creates auth data from file """
        print(os.getcwd())
        print(filename)
        ret = cls.read_file(filename) 

        print(ret)
        if(isinstance(ret, dict)):
            return(cls(ret['id_num'], ret['usr'], ret['pwd'], ret['acc']))
        else:
            return None


        # cls.input_account_data(cls)

# self.bin_path = "../bin"
#         self.auth_file = f'{self.bin_path}/Authfile'

        # try:
        #     os.mkdir(self.bin_path)
        # except OSError:
        #     # print(error)
        #     pass

    def input_account_data(self):
        """ user enters data manually """
        print("___ Ingreso cuenta ___")
        self.id_num = input("ID:")
        self.usr = input("User:")
        self.pwd = input("Pass:")
        self.acc = input("Account:")
        self.save_file()

    def print(self):
        """ show auth info """
        print(f'ID: {self.id_num}')
        print(f'user: {self.usr}')
        print(f'password: {self.pwd}')
        print(f'account: {self.acc}')

    @staticmethod
    def save_file(auth_data, filename):
        """ save file with auth info """
        with open(filename, "w", encoding="utf8") as file_desc:
            file_desc.write(f'{auth_data.id_num},{auth_data.usr},{auth_data.pwd},{auth_data.acc}')
            file_desc.close()

    @staticmethod
    def read_file(filename):
        print(f'filename: {filename}')
        """ Read auth file """
        try:
            with open(filename, "r", encoding="utf8") as file_desc:
                keys = ["id_num", "usr", "pwd", "acc"]
                values = file_desc.read().split(',')
                return dict(zip(keys, values))

        except IOError:
            return 2
