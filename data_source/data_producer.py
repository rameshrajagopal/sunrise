#!/usr/bin/env python

import sys

class Variant(object):
    def __init__(self):
        self.pid = 1
        self.min_sale_price = 1000
        self.max_sale_price = 2000
        self.avail = 10247
        self.on_promotion = 1

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
    def __init__(self, mpid, brand_id, cid, geo, num_store_prods, store_products):
        self.mpid = mpid
        self.brand_id = brand_id
        self.cid = cid
        self.geo = geo
        self.num_store_products = num_store_prods
        self.store_products = store_products

    def __str__(self):
        return str(self.mpid)+" "+str(self.brand_id) + " " + str(self.cid) + " " + str(self.geo) +\
               " " + str(len(self.store_products)) + "\n" 

class DataProducer(object):
    def __init__(self, data_file):
        self.data_file = data_file
        self.products = []
        self.token_map = {}
        self.product_map = {}

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

    def print_records(self):
        print "Products"
        print self.products
        print "token  cnt" 
        for k,v in self.token_map.items():
            print k, v

    def generate_product(self, product_file, num_stores = 2, num_variants = 2):
        mpid = 1
        brand_id = 100
        cid = 1000
        geo = 840
        f = open(product_file, 'w')
        for p in self.products:
            variants = []
            for v in xrange(num_variants):
                variants.append(Variant())
            
            num_store_products = []
            for pas in xrange(num_stores):
                num_store_products.append(StoreProduct(pas, p, variants))

            prod = Product(mpid, brand_id, cid, geo, len(num_store_products), num_store_products)
            f.write(str(prod))
            print prod,
            for pas in num_store_products:
                f.write(str(pas))
                print "\t" + str(pas) ,
                for v in variants:
                    f.write(str(v))
                    print "\t\t" + str(v) ,
        f.close()
#main                
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage is wrong"
        print sys.argv[0] + " filename" 
        sys.exit(-1)
    data_producer = DataProducer(sys.argv[1])
    data_producer.parse()
    data_producer.print_records()
    data_producer.generate_product("/tmp/sherlokc_input.txt")
