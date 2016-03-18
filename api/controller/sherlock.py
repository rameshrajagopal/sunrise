#!/usr/bin/env python

import shlex
import subprocess
import sys
sys.path.append("/home/indix/Work/api-box/sunrise/api/parser")
from parser import Parser

class Sherlock:
    def start_master(self, system):

        master = system+"_master"

        command = "nohup "+Parser.apiConfigMap(master)['executable']+" " \
                  "--port= "+Parser.apiConfigMap(master)['port']+" "+ \
                  "--slaves= "+Parser.apiConfigMap(master)['slaves_path']+" "+ \
                  "--shards= "+Parser.apiConfigMap(master)['shards_path']+" "+ \
                  "--replicas="+Parser.apiConfigMap(master)['replicas']+" "+ \
                  "--log_dir="+Parser.apiConfigMap(master)['log_path']+" "+ \
                  "--queryTimeoutMillis="+Parser.apiConfigMap(master)['queryTimeoutMillis']+ " 2>&1 &"

        print command
        master_args = shlex.split(command)
        print master_args
        subprocess.Popen(master_args)

    def start_slave(self, system, num):

        slave = system+"_slave"
        slave_id = system+"_slave_"+str(num+1)

        command = "nohup "+Parser.apiConfigMap(slave)['executable']+" " \
                  "--slaveaddress="+Parser.apiConfigMap(slave)['slaveaddress']+ " " \
                  "--slaveport="+Parser.apiConfigMap(slave_id)['slaveport']+" " \
                  "--masteraddress="+Parser.apiConfigMap(slave)['masteraddress']+" " \
                  "--masterport="+Parser.apiConfigMap(slave)['masterport']+" " \
                  "--httpPathToShards="+Parser.apiConfigMap(slave)['httpPathToShards']+" " \
                  "--fsPathToShards="+Parser.apiConfigMap(slave_id)['fsPathToShards']+" " \
                  "--backupPathToShards="+Parser.apiConfigMap(slave_id)['']+" " \
                  "--log_dir="+Parser.apiConfigMap(slave_id)['log_dir']+" " \
                  "--kafkaBrokerList="+Parser.apiConfigMap(slave)['kafkaBrokerList']+" " \
                  "--exportMessageSize="+Parser.apiConfigMap(slave)['exportMessageSize']+" " \
                  "--useOnDiskTokenIndex="+Parser.apiConfigMap(slave)['useOnDiskTokenIndex']+" " \
                  "--useS3Cmd="+Parser.apiConfigMap(slave)['useS3Cmd']+" " \
                  "--accessKey="+Parser.apiConfigMap(slave)['accessKey']+" " \
                  "--secretKey="+Parser.apiConfigMap(slave)['secretKey']+" 2>&1 &"

        print command
        slave_args = shlex.split(command)
        print slave_args
        subprocess.Popen(slave_args)