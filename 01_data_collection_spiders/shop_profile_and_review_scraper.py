import scrapy
import json
import pathlib
import pandas as pd
from datetime import datetime
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging

# Time Reference
TODAY = datetime.now().strftime("%Y-%m-%d")

# Links/Response data
input_data = pd.read_csv(f'../generated_links/{TODAY}_links(BASE).csv')
url_start_list = input_data.shop_profile_links.to_list()
scrapy_shopee_links = {
    'START_URL_SPIDERS': ['https://shopee.ph'],
    'PROFILE': input_data.shop_profile_links.to_list(),
    'REVIEW': input_data.shop_review_links.to_list()}

# Scraper Settings
spider_settings = {
    'ROBOTSTXT_OBEY': False,
    'DOWNLOAD_DELAY': 3,
    'CONCURRENT_REQUESTS_PER_DOMAIN': 16,
    'AUTOTHROTTLE_ENABLED': 'True',
    'AUTOTHROTTLE_START_DELAY': 30,
    'AUTOTHROTTLE_MAX_DELAY': 60,
    'AUTOTHROTTLE_TARGET_CONCURRENCY': 2.0,

    # CACHE
    'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',

    # USER-AGENT
    'DOWNLOADER_MIDDLEWARES': {
        # ...
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        # ...
    },
}


# Review Spider
class ReviewsSpider(scrapy.Spider):
    name = 'reviews_spider'
    custom_settings = spider_settings
    start_urls = scrapy_shopee_links.\
        get('START_URL_SPIDERS')

    def parse(self, response):
        review_api_url = scrapy_shopee_links.get('REVIEW')
        for items in review_api_url:
            yield scrapy.Request(
                url=items,
                callback=self.parse_review)

    def parse_review(self, response):
        raw_json = response.body
        d = json.loads(raw_json)

        for entry in d['data']['ratings']:
            yield {
                'comments_compilation': entry
            }


# Shop Spider
class ShopSpider(scrapy.Spider):
    name = 'shop_spider'
    custom_settings = spider_settings
    start_urls = scrapy_shopee_links.\
        get('START_URL_SPIDERS')

    def parse(self, response):
        shop_api_url = scrapy_shopee_links.get('PROFILE')
        for items in shop_api_url:
            yield scrapy.Request(
                url=items,
                callback=self.parse_shop)

    def parse_shop(self, response):
        raw_json = response.body
        d = json.loads(raw_json)

        yield {
            'shop_data': d['data']
        }


# Review Process
review = CrawlerRunner(
    settings={
        'FEEDS': {pathlib.PureWindowsPath(f'../extracted_files/{TODAY}s_review(DIRTY).json'): {'format': 'json'}}}
)

# Shop Profile Process
shop = CrawlerRunner(
    settings={
        'FEEDS': {pathlib.PureWindowsPath(f'../extracted_files/{TODAY}s_shop(DIRTY).json'): {'format': 'json'}}}
)

# scraper log
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


@defer.inlineCallbacks
def crawl():
    yield review.crawl(ReviewsSpider)
    yield shop.crawl(ShopSpider)
    reactor.stop()

crawl()
reactor.run()
