#!/usr/ali/bin/python
# coding:utf-8

class RequestAct(object):
    def __init__(self):
        self.object_name = "REQUEST"
        self.__object_dic = {}

    def initialize(self):
        self.__object_dic = {
            # request nothing (just wait for the user to say something)
            "nothing" : "...",

            # ask if the user wants to make another query
            "next_query" : "You can say, when is the next bus, when is the previous bus, start a new query, or goodbye.",

            # request the departure place
            "origin_place" : "Where are you leaving from?",

            # request the arrival place
            "destination_place" : ["Where are you going?", "Where would you like to go?"]
        }


    def hasObject(self, obj):
        return self.__object_dic.has_key(obj)

    def getObject(self, obj):
        return self.__object_dic[obj]

    def getAllObjs(self):
        return self.__object_dic.keys()

