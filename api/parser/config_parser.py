#!/usr/bin/env python
import ConfigParser

class Parser:

    def __init__(self):
        self.api_config = ConfigParser.ConfigParser().read("../config/api.ini")

    def apiConfigMap(section):
        dict = {}
        options = api_config.options(section)
        print options
        for option in options:
            try:
                dict[option] = api_config.get(section, option)
                if dict[option] == -1:
                    print("Skip: %s" % option)
            except:
                print("Exception thrown %s!" % option)
                dict[option] = None
        return dict

if __name__ == '__main__':
    num = 1
    system="sherlock"
    slave=system+"_slave_"+str(num+1)
    t = Parser
    print t.api_config
    print(t.apiConfigMap(slave)['slaveport'])