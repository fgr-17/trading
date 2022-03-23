#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
class homebroker_auth:
    """pyhomebroker auth data"""

    auth_file="Authfile"

    def __init__(self, dni, usr, pwd, acc):
        self.dni = dni
        self.usr = usr
        self.pwd = pwd
        self.acc = acc

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
        fd = open(self.auth_file, "r")
        if(fd != FileNotFoundError):
            self.dni, self.usr, self.pwd, self.acc = fd.read().split()
            self.print()



class homebroker:
    """pyhomebroker interface manager"""

    def __init__(self):
        print("___ Ingreso cuenta ___")
        dni = input("DNI:")
        usr = input("Usuario:")
        pwd = input("Password:")
        acc = input("Nro. cuenta comitente:")
        self.auth = homebroker_auth(dni, usr, pwd, acc)
        self.auth.save_file()


    def print_auth_data(self):
        self.auth.read_file()


hb = homebroker()
hb.print_auth_data()