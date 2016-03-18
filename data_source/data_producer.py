#!/usr/bin/env python

import sys
import random

class Variant(object):
    MIN_SALE_PRICE = 10000
    MAX_SALE_PRICE = 1000 * 1000
    MAX_PID_VALUE = 1024 * 1024 * 1024
    MAX_AVAIL_VALUE = 1024 * 1024

    def __init__(self):
        self.pid = random.randint(1, Variant.MAX_PID_VALUE)
        self.min_sale_price = random.randint(1, Variant.MIN_SALE_PRICE)
        self.max_sale_price = random.randint(self.min_sale_price, Variant.MAX_SALE_PRICE)
        self.avail = random.randint(1, Variant.MAX_AVAIL_VALUE)
        self.on_promotion = random.randint(0, 1)

    def __str__(self):
        return str(self.pid) + " " + str(self.min_sale_price) + " " +\
               str(self.max_sale_price) + " " + str(self.avail) + " " + \
               str(self.on_promotion) +"\n"


class StoreProduct(object):
    def __init__(self, store_id, title, variants):
        self.store_id = store_id
        self.variants = variants
        self.title = title

    def __str__(self):
        return str(self.store_id) + " " + str(len(self.variants)) + " " + self.title  +"\n"

class Product(object):
    def __init__(self, brand_id, cid, geo, num_store_prods, store_products):
        self.mpid = id(self)
        self.brand_id = brand_id
        self.cid = cid
        self.geo = geo
        self.num_store_products = num_store_prods
        self.store_products = store_products

    def __str__(self):
        return str(self.mpid)+" "+str(self.brand_id) + " " + str(self.cid) + " " + str(self.geo) +\
               " " + str(len(self.store_products)) + "\n"

    def getMpid(self):
        return self.mpid

class DataProducer(object):
    MAX_BRAND_ID   = 1024 * 1024
    MAX_CATEGORY_ID = 1024 * 1024
    MAX_STORES_PER_PRODUCT = 10
    MAX_VARIANTS_PER_PRODUCT = 10

    def __init__(self, data_file, output_path, max_shards):
        self.data_file = data_file
        self.products = []
        self.token_map = {}
        self.product_map = {}
        self.output_path = output_path
        self.num_shards = 0
        self.shard_map_data = []
        self.max_shards = max_shards;
        self.mpid_map = {}

    def parse(self):
        with open(self.data_file, 'r') as f:
            for line in f:
                data = line.strip();
                self.products.append(data)
                for e in data.split():
                    if self.token_map.has_key(e):
                        self.token_map[e] += 1
                    else:
                        self.token_map[e] = 1
        per_shard = len(self.products) // self.max_shards
        self.shard_map_data = [self.products[i:i+per_shard] for i in xrange(0, len(self.products), per_shard)]
        self.num_shards = len(self.shard_map_data)


    def print_records(self):
        print "Products"
        print self.products
        print "token  cnt"
        for k,v in self.token_map.items():
            print k, v
        for k, v in self.mpid_map.items():
            print k, v

    def generate_product(self, f, num_stores = 2, num_variants = 2):
        mpid = 1
        brand_id = 100
        cid = 1000
        geo = 840
        f.write(self.output_path + "/ " + str(self.num_shards) + "\n")
        f.write(str(len(self.products)) + "\n")
        for p in self.products:
            variants = []
            for v in xrange(num_variants):
                variants.append(Variant())

            num_store_products = []
            for pas in xrange(num_stores):
                num_store_products.append(StoreProduct(pas, p, variants))

            prod = Product(brand_id, cid, geo, len(num_store_products), num_store_products)
            f.write(str(prod))
            print prod,
            for pas in num_store_products:
                f.write(str(pas))
                print "\t" + str(pas) ,
                for v in variants:
                    f.write(str(v))
                    print "\t\t" + str(v) ,

    def generate_shard_data(self, f, shard_id, shard_products, num_stores = 2, num_variants = 2):
        brand_id = random.randint(1, DataProducer.MAX_BRAND_ID)
        cid = random.randint(1, DataProducer.MAX_CATEGORY_ID)
        geo = 840
        f.write(str(len(shard_products)) + "\n")
        #go through all products and write into the file
        for p in shard_products:
            variants = []
            for v in xrange(num_variants):
                variants.append(Variant())

            num_store_products = []
            for pas in xrange(num_stores):
                num_store_products.append(StoreProduct(pas, p, variants))

            prod = Product(brand_id, cid, geo, len(num_store_products), num_store_products)
            self.mpid_map[prod.getMpid()] = prod
            f.write(str(prod))
            print prod,
            for pas in num_store_products:
                f.write(str(pas))
                print "\t" + str(pas) ,
                for v in variants:
                    f.write(str(v))
                    print "\t\t" + str(v) ,

    def write_header(self, f):
        f.write(self.output_path + "/ " + str(self.num_shards) + "\n");

    def generate_product_file(self, product_file):
        f = open(product_file, 'w')
        #write header
        self.write_header(f);
        for (shard_id, shard_products) in enumerate(self.shard_map_data):
            num_stores = random.randint(1, DataProducer.MAX_STORES_PER_PRODUCT)
            num_variants = random.randint(1, DataProducer.MAX_VARIANTS_PER_PRODUCT)
            self.generate_shard_data(f, shard_id, shard_products, num_stores, num_variants)
        #close the file
        f.close()

#main
if __name__ == '__main__':
    if len(sys.argv) != 4:
        print "Usage is wrong"
        print sys.argv[0] + " filename o/p_dir_name o/p_file"
        sys.exit(-1)
    data_producer = DataProducer(sys.argv[1], sys.argv[2], 2)
    data_producer.parse()
    data_producer.generate_product_file(sys.argv[3])
    data_producer.print_records()
