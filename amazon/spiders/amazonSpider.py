import scrapy
import re
from amazon.items import AmazonItem

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrapy import optional_features
# uncommented fixes my issue
#optional_features.remove('boto')


class amazonSpider(scrapy.Spider): #CrawlSpider
	name = "amazon"
	allowed_domains = ["amazon.com"]

	base_url = "http://amazon.com/"

	ASIN = raw_input("Enter an ASIN please: ")

	product_page = base_url + "dp/" + ASIN + "/"
	review_page = base_url + "product-reviews/" + ASIN + "/"

	start_urls = []#['http://www.amazon.com/AUSDOM%C2%AE-Lightweght-Over-Ear-headset-leather/dp/B00SB6SPA2/ref=sr_1_18?&s=electronics&ie=UTF8&qid=1434750275&sr=1-18&keywords=headphones']
	#urls = raw_input("enter a url: ")
	#start_urls.append(urls)
	#start_urls.append(product_page)
	start_urls.append(review_page)
	



	def parse(self, response): #if CrawlSpider, change name (can't override parse())
		items = []

		item = AmazonItem()

		#item['title'] = response.xpath(".//*[@id='productTitle']/text()").extract()
		item['title'] = response.xpath(".//*[@id='cm_cr-product_info']/div/div[2]/div/div/div[2]/div[1]/span/a/text()").extract()

		temp = response.xpath(".//*[@class='a-section a-spacing-small page-content page-min-width']//span[@class='a-size-base' or contains(@class, 'review-text')]/text()").extract()

		temp = ''.join(temp) #Makes into a string

		item['reviews'] = temp#re.sub(r'Comment', "\n\n", temp) #works when not in a list (e.g. items[])
		#product = AmazonItem()
		#product['title'] = response.xpath(".//*[@id='productTitle']").extract()

		items.append(item)

		print items
