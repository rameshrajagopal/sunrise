#!/usr/bin/env python

import multiprocessing
import os.path
import time
import datetime
from sherlock import Sherlock

import sys
sys.path.append("/home/indix/Work/api-box/sunrise/api/parser")

class ApiProcesses:

    def check_proc(self, process):
        if process is "sherlock" or "marina":
            file_path="/home/indix/Work/api-box/"+process+"/register_done"

            timeout=10
            startTime = datetime.datetime.now()
            endTime = startTime + datetime.timedelta(seconds=timeout)

            while datetime.datetime.now() < endTime:
                if not os.path.exists(file_path):
                    time.sleep(5)
                else:
                    break
            if os.path.isfile(file_path):
                print("%s master and slave processes started" % process)
            else:
                print ("Timed out waiting for the file: %s" % file_path)

if __name__ == '__main__':

    sherlock_obj = Sherlock()
    sherlock_obj.start_master("sherlock")
    jobs = []
    for i in range(2):
        processes = multiprocessing.Process(target=sherlock_obj.start_slave, args=(i,"sherlock",))
    jobs.append(processes)
    processes.start()

    api_procs = ApiProcesses()
    api_procs.check_proc("sherlock")