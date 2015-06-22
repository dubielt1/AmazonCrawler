import scrapy
import re
from amazon.items import AmazonItem

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.sgml import SgmlLinkExtractor


from scrapy import optional_features
# uncommented fixes my issue
#optional_features.remove('boto')


class amazonSpider(CrawlSpider): #CrawlSpider
	name = "amazon"
	allowed_domains = []

	base_url = "http://amazon"

	
	country = raw_input("please enter the country-code domain name (e.g. '.com', '.fr', '.co.uk'): ")
	base_url = base_url + country + "/"
	

	if country != ".com":
		rules = (Rule (LinkExtractor(allow=(), restrict_xpaths=("//a[contains(@href,'ref=cm_cr_pr_btm_link_next')]")), callback='parse_foreign', follow=True, ),)

	else:
		rules = (Rule (LinkExtractor(allow=(), restrict_xpaths=(".//*[@id='cm_cr-pagination_bar']/ul/li[last()]/a")), callback='parse_item', follow=True, ),)
		
		

	global ASIN
	ASIN = raw_input("Enter an ASIN please: ")



	product_page = base_url + "dp/" + ASIN + "/"
	review_page = base_url + "product-reviews/" + ASIN + "/"

	start_urls = []
	start_urls.append(review_page)
	

	#another function for parsing foreign coutries with seperate rules and callback

	def parse_foreign(self, response):
		items = []

		item = AmazonItem()

		title_path = "//a[contains(@href, " + "'/dp/" + ASIN + "/ref=cm_cr_pr_product_top'" +")]/text()"

		item['title'] = response.xpath(title_path).extract()

		temp = response.xpath(".//*[@class='reviewText']/text()").extract()

		temp = ''.join(temp)

		item['reviews'] = temp

		items.append(item)

		return items

	def parse_item(self, response):
		items = []

		item = AmazonItem()

		item['title'] = response.xpath(".//*[@id='cm_cr-product_info']/div/div[2]/div/div/div[2]/div[1]/span/a/text()").extract()

		temp = response.xpath(".//*//span[contains(@class, 'review-text')]/text()").extract()

		temp = ''.join(temp) #Makes into a string

		item['reviews'] = temp

		items.append(item)

		return items
