# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
from pprint import pprint

from scrapy import *
from collections import defaultdict


class AmazonPipeline(object):

#    def __init__(self):
	

    def count(self, words, n):

        countD = defaultdict(int)

        for i in range(len(words)-n+1):
            key = tuple(words[i:i+n])
            countD[key] = countD[key] + 1


	raw = open("raw.txt", "a")
	raw.write(str(countD))

        pprint (countD) #Could be removed, data written to file
	


    def close_spider(self, spider):
	fr = open('review_data.txt', 'r')
	all_reviews = fr.read()
	fr.close()

	#wouldn't hurt to remove 'Comment'
	all_reviews = all_reviews.replace(",", " ")
	all_reviews = all_reviews.replace(".", " ")
	all_reviews = all_reviews.replace("-", " ")
	all_reviews = all_reviews.replace("!", " ")
	all_reviews = all_reviews.replace("?", " ")
	all_reviews = all_reviews.replace("@", " ")
	all_reviews = all_reviews.replace("/", " ")
	all_reviews = all_reviews.replace(":", " ")
	all_reviews = all_reviews.replace(";", " ")
	all_reviews = all_reviews.replace("'", " ")
	all_reviews = all_reviews.replace('"', " ")
	all_reviews = all_reviews.replace("(", " ")
	all_reviews = all_reviews.replace(")", " ")
	all_reviews = all_reviews.replace("+", " ")
	all_reviews = all_reviews.replace("=", " ")

        words = all_reviews.split()


        self.count(words, 1)
        self.count(words, 2)
        self.count(words, 3)
        self.count(words, 4)	

    def process_item(self, item, spider):
	
	f = open('review_data.txt', 'a')	

	f.write(item['reviews'])
	f.write(" ")	
	
	f.close()

        return item
