# -*- coding: utf-8 -*-
""" Basic access and management for pyhomebroker APIs """

__version__ = '0.0.1'
__author__ = 'fgr-17'


class Auth:
    """ pyhomebroker auth data """
    def __init__(self, id_num, usr, pwd, acc):
        self.__id_num = id_num
        self.__usr = usr
        self.__pwd = pwd
        self.__acc = acc
        self.__filename = ""

    @classmethod
    def from_file(cls, filename):
        """ Creates auth data from file """
        ret = cls.read_file(filename)
        if isinstance(ret, dict) is True:
            return cls(ret['id_num'], ret['usr'], ret['pwd'], ret['acc'])
        return None

    @classmethod
    def from_stdin(cls):
        """ user enters data manually """
        print("___ Ingreso cuenta ___")
        id_num = input("ID:")
        usr = input("User:")
        pwd = input("Pass:")
        acc = input("Account:")
        filename = input("Save file to:")
        tmp = cls(id_num, usr, pwd, acc)
        tmp.set_filename(filename)
        tmp.save_file()
        return tmp

    def set_filename(self, filename):
        """ set filename to save data """
        self.__filename = filename

    def get(self):
        """ get all data as a dict """
        keys = ["id_num", "usr", "pwd", "acc"]
        values = [self.__id_num, self.__usr, self.__pwd, self.__acc]
        return dict(zip(keys, values))

    def get_id_num(self):
        """ get id number """
        return self.__id_num

    def get_usr(self):
        """ get user """
        return self.__usr

    def get_pwd(self):
        """ get password """
        return self.__pwd

    def get_acc(self):
        """ get account """
        return self.__acc

    def print(self):
        """ show auth info """
        print(f'ID: {self.__id_num}')
        print(f'user: {self.__usr}')
        print(f'password: {self.__pwd}')
        print(f'account: {self.__acc}')

    def save_file(self):
        """ save file with auth info """
        with open(self.__filename, "w", encoding="utf8") as file_desc:
            file_desc.write(f'{self.__id_num},{self.__usr},{self.__pwd},{self.__acc}')
            file_desc.close()

    @staticmethod
    def read_file(filename):
        """ Read auth file """
        try:
            with open(filename, "r", encoding="utf8") as file_desc:
                keys = ["id_num", "usr", "pwd", "acc"]
                values = file_desc.read().split(',')
                return dict(zip(keys, values))
        except IOError:
            return 2
