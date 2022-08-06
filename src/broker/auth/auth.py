# -*- coding: utf-8 -*-

""" Basic access and management for pyhomebroker APIs """

__all__ = ['Auth']
__version__ = '0.0.1'
__author__ = 'fgr-17'


import os


class Auth:
    """ pyhomebroker auth data """

    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, filename):
        cls.auth_file = filename
        if cls.read_file() != 0:
            cls.input_account_data()

        # @classmethod
        # def from_dict(cls)


# self.bin_path = "../bin"
#         self.auth_file = f'{self.bin_path}/Authfile'

        # try:
        #     os.mkdir(self.bin_path)
        # except OSError:
        #     # print(error)
        #     pass

        

    # def __init__(self, dni, user, password, comitente):

    #     self.dni = dni
    #     self.usr = user
    #     self.pwd = password
    #     self.acc = comitente
    #     self.save_file()

    def input_account_data(self):
        """ user enters data manually """
        print("___ Ingreso cuenta ___")
        self.dni = input("DNI:")
        self.usr = input("User:")
        self.pwd = input("Pass:")
        self.acc = input("Cuenta comitente:")
        self.save_file()

    def print(self):
        """ show auth info """
        print(f'DNI: {self.dni}')
        print(f'usuario: {self.usr}')
        print(f'password: {self.pwd}')
        print(f'cuenta: {self.acc}')

    def save_file(self):
        """ save file with auth info """
        with open(self.auth_file, "w", encoding="utf8") as file_desc:
            file_desc.write(f'{self.dni},{self.usr},{self.pwd},{self.acc}')
            file_desc.close()

    def read_file(self):
        """ Read auth file """
        try:
            with open(self.auth_file, "r", encoding="utf8") as file_desc:
                self.dni, self.usr, self.pwd,\
                    self.acc = file_desc.read().split(',')
                return 0

        except IOError:
            return 2
