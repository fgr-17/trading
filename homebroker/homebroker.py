# -*- coding: utf-8 -*-
from ast import arg

class hb_auth:
    """pyhomebroker auth data"""

    auth_file="./bin/Authfile"

    def __init__(self, *args):
        if(self.read_file() != None):
            self.input_account_data()

    # def __init__(self, dni, usr, pwd, acc):
    #     self.dni = dni
    #     self.usr = usr
    #     self.pwd = pwd
    #     self.acc = acc

    def input_account_data(self):
        print("___ Ingreso cuenta ___")
        self.dni = input("DNI:")
        self.usr = input("Usuario:")
        self.pwd = input("Password:")
        self.acc = input("Nro. cuenta comitente:")
        self.save_file()

    def print(self):
        print("DNI:{}".format(self.dni))
        print("usuario:{}".format(self.usr))
        print("password:{}".format(self.pwd))
        print("cuenta:{}".format(self.acc))

    def save_file(self):
        fd = open(self.auth_file, "w")
        if(fd != FileNotFoundError):
            fd.write("{},{},{},{}".format(self.dni, self.usr, self.pwd, self.acc))
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

class homebroker:
    """pyhomebroker interface manager"""

    def __init__(self):
        self.auth = hb_auth()        
            
    def print_auth_data(self):
        self.auth.print()
