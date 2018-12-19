#!/usr/ali/bin/python
# coding:utf-8

class InformAct(object):
    def __init__(self):
        self.object_name = "INFROM"
        self.__object_dic = {}

    def initialize(self):
        self.__object_dic = {
            # welcome to the system
            "welcome" : "Welcome to MyBus.",

            # quitting
            "goodbye" : "Thank you for using MyBus. Goodbye.",

            # looking up database (to announce a delay)
             "looking_up_database_first" : "Just a minute. Let me check that for you.",
             "looking_up_database_subsequent" : "Just a second.",

            # inform the user we're starting a new query
            "starting_new_query" : "Okay let's start from the beginning.",

            # query result
            "result" : self.showResult,

            # query results
            "results": self.showResults,

            # error
            "error" : self.showError,

            # vad_error
            "vad_error" : ["I'm sorry. I didn't understand you.  Please repeat yourself.", "I'm sorry, I do not understand what you said"]
        }


    def hasObject(self, obj):
        return self.__object_dic.has_key(obj)

    def getObject(self, obj):
        return self.__object_dic[obj]

    def getAllObjs(self):
        return self.__object_dic.keys()

    def showResult(self, frame_hash):
        return "There is a < result.route %s> leaving < origin_place %s> at < result.departure_time %s>. It will arrive at <destination_place %s> at <result.arrival_time %s>." % (
        frame_hash["result"]["route"], frame_hash["origin_place"], frame_hash["result"]["departure_time"], frame_hash["destination_place"], frame_hash["result"]["arrival_time"])

    def showResults(self, frame_hash):
        return "There is a < result.0.route %s> leaving < origin_place %s> at < result.0.departure_time %s>. It will arrive at <destination_place %s> at <result.0.arrival_time %s>." % (
        frame_hash["result"][0]["route"], frame_hash["origin_place"], frame_hash["result"][0]["departure_time"], frame_hash["destination_place"], frame_hash["result"][0]["arrival_time"])

    def showError(self, err):
        pass

