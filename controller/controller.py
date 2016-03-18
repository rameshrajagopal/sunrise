#!/usr/bin/env python

import sys
import signal
import time
import os

def signal_handler(signal, frame):
    print "Exiting"
    sys.exit(-1)

global CWD_DIR, DATA_SOURCE_PATH, DATA_SHARD_INDEXER_PATH, INTERMEDIATE_FILE, CWD_ELF_PATH
CWD_DIR = "/home/indix/ind9/hackathon/sunrise"
DATA_SOURCE_PATH = CWD_DIR + "/data_source/"
CWD_ELF_PATH = CWD_DIR + "/elfs"
DATA_GENERATOR_ELF = "product_generator"
DATA_SHARD_INDEXER = "shard_indexer.out"
INTERMEDIATE_FILE = CWD_DIR + "/output_files/sherlock.txt"

sys.path.append(DATA_SOURCE_PATH)
sys.path.append("/home/indix/ind9/hackathon/sunrise/elfs")

from simple_http_server import HttpServer
from data_producer import DataProducer
import threading
from subprocess import call

class Controller(object):

    def __init__(self, port, products_file, shard_file_path):
        self.prod_file = products_file
        self.shard_file_path = shard_file_path
        self.port = port
        self.http_server = HttpServer(port, shard_file_path)
        self.http_thread = threading.Thread(target=Controller.httpServer, args = (self,))
        self.num_shards = 2
        self.indexer_type = "sherlock"
        self.data_producer = DataProducer(self.prod_file, self.shard_file_path,
                self.num_shards)

    def httpServer(self):
        try:
            self.http_server.start()
        except e:
            print e
            sys.exit(-1)

    def setup(self):
        self.data_producer.parse()
        self.data_producer.generate_product_file(INTERMEDIATE_FILE)
        print DATA_GENERATOR_ELF, INTERMEDIATE_FILE
        try:
            status = call([DATA_GENERATOR_ELF, INTERMEDIATE_FILE])
#            os.system(DATA_GENERATOR_ELF + " " + INTERMEDIATE_FILE)
            print "Generating shard indexes" 
        except OSError as e:
            print "Execution failed:", e
        for shard_id in xrange(self.num_shards):
            matched_prod_file = CWD_DIR + "/output_files/" + str(shard_id) + "/matched_products.data"
            print matched_prod_file
#            os.system(DATA_SHARD_INDEXER + " " + self.indexer_type + " " + str(shard_id) +
 #                   " " + matched_prod_file)
            call([DATA_SHARD_INDEXER, self.indexer_type, str(shard_id),
                    matched_prod_file])
            tgz_file = CWD_DIR + "/output_files/" + str(shard_id) + "/sherlock/" + str(shard_id) + ".tar.gz"
            print tgz_file, self.shard_file_path
            call(["mv", tgz_file, self.shard_file_path])
        time.sleep(2)
        
    def start(self):
        self.http_thread.start()
        print "Server started"

    def join(self):
        self.http_thread.join()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    if len(sys.argv) != 4:
        print "Usage is wrong"
        print sys.argv[0] + " products_file shard_file_path"
        sys.exit(-1)
    controller = Controller(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    controller.setup()
    controller.start()
 #   controller.join()
         
