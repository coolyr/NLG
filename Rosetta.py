#!/usr/ali/bin/python
# coding:utf-8

import sys
import random
import re
import Inform
import Request

reload(sys)
sys.setdefaultencoding('utf-8')

class Rosetta(object):
    def __init__(self):
        self.class_name = "Rosetta"
        self.act = {}

    def initialize(self):
        #创建对象
        inform = Inform.InformAct()
        request = Request.RequestAct()
        #初始化
        inform.initialize()
        request.initialize()
        #添加到动作Hash
        self.act["inform"] = inform
        self.act["request"] = request

    '''
    start
    {
        act inform
        object  result
        origin_place    wudaokou
        destination_place   huilongguan
        result  {
            departure_time  1418
            arrival_time    1920
            route   bus
        }
    }
    end
    '''

    def Reinitialize(self):
        pass

    def processFrames(self, framesStr):
        print "framesStr =>", framesStr

        #<1> 切分,清空[\n\s\t\r]等
        tokens = framesStr.split()#默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等。
        # print "tokens => ", tokens
        # print "len = ", len(tokens)

        #<2> 判断start和end
        start = tokens.pop(0)
        end = tokens.pop()
        # print "len = ", len(tokens)

        if "start" != start or "end" != end:
            print "frame list should start with 'start' and end with 'end'"
            return -1

        #<3>解析{}
        i = 0
        sentences = ""
        while(i < len(tokens)):
            if tokens[i] != "{":
                print "ERROR: frame should begin with a '{'"
                return -1

            match = 1
            j = i + 1
            while(match != 0):
                if "{" == tokens[j]:
                    match += 1
                if "}" == tokens[j]:
                    match -= 1
                j += 1
            hash_frame = {}
            ret = self.parseFrame(tokens[i:j], hash_frame)
            if ret != 0:
                print "parseFrame Error!"
                return -1
            print "####### hash_frame =", hash_frame
            sentences += self.generate(hash_frame)
            i = j
        print "sentences => ", sentences
        print "##################################################################"
        return sentences


    def parseFrame(self, tokens, hash_frame):
        # print "parseFrame ==> ", tokens
        start = tokens.pop(0)
        end = tokens.pop()
        if "{" != start or "}" != end:
            print "frame should start with '{' and end with '}'"
            return -1
        ret, index = self.parseKV(hash_frame, tokens, 0)
        if ret != 0:
            print "parseKV Error!"
            return -1
        return 0


    # 递归函数：进入该函数必须保证key = slot，同时函数要跳过"}"字符
    def parseKV(self, hash_frame, tokens, index=0):
        # print "parseKV ==> tokens[",index,"] =", tokens[index], "\t\ttokens =", tokens
        slot = tokens[index]
        # print "slot = ", slot
        index +=1
        flag = True
        try:
            while(index < len(tokens)):
                if "{" == tokens[index]:
                    hash_frame[slot] = {}
                    ret, index = self.parseKV(hash_frame[slot], tokens, index + 1)
                    if ret != 0:
                        return (-1, index)
                elif "}" == tokens[index]:
                    index += 1
                    return (0, index)
                elif re.search(":\d", tokens[index]):
                    searchObj = re.search("\d", tokens[index])
                    hash_frame[slot] = {}
                    index += 1
                    for i in range(int(searchObj.group(0))):
                        hash_frame[slot][i] = {}
                        start = tokens[index]
                        if "{" != start:
                            print "Array should begin with a '{'";
                            return (-1, index)
                        ret, index = self.parseKV(hash_frame[slot][i], tokens, index + 1)
                        if ret != 0:
                            return (-1, index)
                elif flag:
                    value = tokens[index]
                    hash_frame[slot] = value
                    index += 1
                    flag = False
                else:
                    slot = tokens[index]
                    index += 1
                    flag = True
        except BaseException, e:
            print e.message
            return (-1, index)
        return (0, index)


    def generate(self, hash_frame):
        # <1>获取回答 frame 已经是Hash类型
        ret, replay = self.getBestReply(hash_frame)
        # <2>判断是否合法
        # <3>过滤器
        # <4>保存concept到历史记录
        # <5>加上“Header、Footer”
        return replay


    def getBestReply(self, hash_frame):
        act = hash_frame["act"]
        object = hash_frame["object"]
        print "act=%s, object=%s" % (act,object)
        ret, reply = self.getActObject(act, object)
        if ret != 0:
            print "not matched best replay"
            return (-1, "")
        if hasattr(reply, '__call__'):
            reply = reply(hash_frame)
        elif isinstance(reply, str):
            pass
        elif isinstance(reply, list):
            reply = random.sample(reply, 1)[0]
        else:
            print "unknow type"
        return (0, reply)


    def getActObject(self, act, object):
        if not self.act.has_key(act):
            print "unknow act=%s" % act
            return (-1, "")
        if self.act[act].hasObject(object):
            return (0, self.act[act].getObject(object))
        else:
            for obj in self.act[act].getAllObjs():
                if object in obj:
                    print "Matched on key: %s" % obj
                    return (0, self.act[act].getObject(obj))
        return (-1, "")


    # now push concepts into history
    def pushConceptsInHistory(self):
        pass

    # this filter is applied at the end on the utterance. It contains various regexp replaces which do abbreviations mostly
    def finalFilter(self, reply):
        # prolong_break = " {break time=\"800ms\"/} "
        # reply = re.sub(" \.\.\.\. ", prolong_break, reply)
        #
        # long_break = " {break time=\"600ms\"/} "
        # reply = re.sub(" \.\.\. ", long_break, reply)
        #
        # short_break = " {break time=\"400ms\"/} "
        # reply = re.sub(" \.\. ", short_break, reply)
        return reply


    def getHeader(self):
        # return '{?xml version=\"1.0\" encoding=\"ISO-8859-1\"?}{speak version=\"1.0\" xmlns=\"http://www.w3.org/2001/10/synthesis\"xml:lang=\"en-US\"}';
        return ""

    def getFooter(self):
        # return "{/speak}";
        # return q{{/SABLE}};
        return ""


if __name__ == '__main__':
    nlg = Rosetta()
    nlg.initialize()

    o_1 = "start\n{\nact\tinform\nobject\tgoodby\n_repeat_counter\t4\n}\nend\n"
    o_2 = "start\n{\nact\tinform\nobject\tresult\norigin_place\twudaokou\ndestination_place\thuilongguan\nresult\t{\ndeparture_time\t1418\narrival_time\t1920\nroute\tbus\n}\n}\nend\n"
    o_3 = "start\n{\nact\tinform\nobject\tgoodbye\n_repeat_counter\t4\n}\n{\nact\tinform\nobject\tvad_error\n_repeat_counter\t1\n}\nend\n"
    o_4 = "start\n{\nact\tinform\nobject\tresults\norigin_place\twudaokou\ndestination_place\thuilongguan\nresult\t:3\n{\ndeparture_time\t1618\narrival_time\t2120\nroute\tsubway\n}\n{\ndeparture_time\t1418\narrival_time\t1920\nroute\tbus\n}\n{\ndeparture_time\t1618\narrival_time\t2120\nroute\tsubway\n}\n}\nend\n"

    nlg.processFrames(o_1)
    print
    nlg.processFrames(o_2)
    print
    nlg.processFrames(o_3)
    print
    nlg.processFrames(o_4)

