# -*- coding: utf-8 -*-

"""
    Basic access and management for pyhomebroker APIs
"""

__all__ = ['auth', 'homebroker']
__version__ = '0.0.1'
__author__ = 'fgr-17'

from ast import arg
from pyhomebroker import HomeBroker


class HbAuth:
    """
        pyhomebroker auth data
    """

    auth_file = "./bin/Authfile"

    def __init__(self, *args):
        if self.read_file() is not None:
            self.input_account_data()

    # def __init__(self, dni, usr, pwd, acc):
    #     self.dni = dni
    #     self.usr = usr
    #     self.pwd = pwd
    #     self.acc = acc

    def input_account_data(self):
        print("___ Ingreso cuenta ___")
        self.dni = input("DNI:")
        self.usr = input("User:")
        self.pwd = input("Pass:")
        self.acc = input("Cuenta comitente:")
        self.save_file()

    def print(self):
        print("DNI:{}".format(self.dni))
        print("usuario:{}".format(self.usr))
        print("password:{}".format(self.pwd))
        print("cuenta:{}".format(self.acc))

    def save_file(self):
        fd = open(self.auth_file, "w")
        if(fd != FileNotFoundError):
            fd.write("{},{},{},{}".format(self.dni, self.usr,
                                          self.pwd, self.acc))
            fd.close()

    def read_file(self):
        try:
            fd = open(self.auth_file, "r")
            if(fd != FileNotFoundError):
                self.dni, self.usr, self.pwd, self.acc = fd.read().split(',')
            else:
                return 1
        except IOError:
            return 2


class HbInterface:
    """
        pyhomebroker interface manager
    """

    def __init__(self):
        self.auth = HbAuth()

    def print_auth_data(self):
        self.auth.print()


class Broker(HbInterface):

    def __init__(self, code):
        super().__init__()
        self.code = code

    def login(self):
        self.hb = HomeBroker(self.code)
        self.hb.auth.login(self.auth.dni, self.auth.usr,
                           self.auth.pwd, raise_exception=True)
        self.hb.online.connect()
