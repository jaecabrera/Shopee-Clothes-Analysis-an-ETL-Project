import scrapy
import json
import re
import time
import pathlib
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

save_path = '../extracted_files/%(time)s_product(DIRTY).csv'
project_settings = dict(
    # BEGIN: scrapy spider settings
    BOT_NAME='clothes',
    SPIDER_MODULES=['clothes.spiders'],
    NEWSPIDER_MODULE='clothes.spiders',
    ROBOTSTXT_OBEY=False,
    DOWNLOAD_DELAY=3,
    CONCURRENT_REQUESTS_PER_DOMAIN=16,

    # SPEED
    AUTOTHROTTLE_ENABLED=True,
    AUTOTHROTTLE_START_DELAY=30,
    AUTOTHROTTLE_MAX_DELAY=60,
    AUTOTHROTTLE_TARGET_CONCURRENCY=2.0,

    # CACHE
    DUPEFILTER_CLASS='scrapy_splash.SplashAwareDupeFilter',
    HTTPCACHE_STORAGE='scrapy_splash.SplashAwareFSCacheStorage',

    # PROXY
    PROXY_POOL_ENABLED=True,
    PROXY_POOL_TRY_WITH_HOST=True,

    # MIDDLEWARES
    DOWNLOADER_MIDDLEWARES={
        # ...
        # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
        # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
        # ...
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
        # ...
    },
    # RANDOM_UA_PER_PROXY=True,

    FEEDS={pathlib.PureWindowsPath(save_path): {'format': 'csv'}}
)

code = {
    'short_sleeves': '6800',
    'top': '827',
    'long_sleeves': '6807',
    'crop_top': '7238'}
code_list = [v for k, v in code.items()]

url_requests = {
    'address_cat_id': 'https://shopee.ph/api/v4/search/search_items?by=relevancy&categoryids=',
    'address_key_word': '&keyword=korean%20top&',
    'address_sort': 'limit=100&newest=10&order=desc&',
    'address_scenario': 'page_type=search&scenario=PAGE_GLOBAL_SEARCH&skip_autocorrect=1&version=2'}

url_request_appended = url_requests. \
                           get('address_key_word') + url_requests. \
                           get('address_sort') + url_requests. \
                           get('address_scenario')


# scrapy spider
class ClothesSpider(scrapy.Spider):
    name = 'clothes'
    start_urls = ['https://shopee.ph/']
    custom_settings = project_settings

    def start_requests(self):

        url_list = []
        for items in code_list:
            url_list.append(
                url_requests.get('address_cat_id') + items
                + url_request_appended)

        for urls in url_list:
            yield scrapy.Request(url=urls, callback=self.parse_json)

    def parse_json(self, response):
        json_body = response.body
        data = json.loads(json_body)

        for entry in data['items']:
            if re.findall(code.get('short_sleeves'), str(response.url)) == [code.get('short_sleeves')]:
                category_labeler = 'Short Sleeves'
            if re.findall(code.get('top'), str(response.url)) == [code.get('top')]:
                category_labeler = 'Top'
            if re.findall(code.get('long_sleeves'), str(response.url)) == [code.get('long_sleeves')]:
                category_labeler = 'Long Sleeves'
            if re.findall(code.get('crop_top'), str(response.url)) == [code.get('crop_top')]:
                category_labeler = 'Crop Top'

            scrape = entry['item_basic']
            yield {
                'product_itemid': scrape['itemid'],
                'product_shopid': scrape['shopid'],
                'product_category': category_labeler,
                'product_name': scrape['name'],
                'product_price': scrape['price_before_discount'],
                'product_price_min': scrape['price_min'],
                'product_price_max': scrape['price_max'],
                'product_discount': scrape['raw_discount'],
                'product_brand': scrape['brand'],
                'product_like_count': scrape['liked_count'],
                'product_comment_count': scrape['cmt_count'],
                'product_views': scrape['view_count'],
                'prod_rate_star_0': scrape['item_rating']['rating_count'][5],
                'prod_rate_star_1': scrape['item_rating']['rating_count'][4],
                'prod_rate_star_2': scrape['item_rating']['rating_count'][3],
                'prod_rate_star_3': scrape['item_rating']['rating_count'][2],
                'prod_rate_star_4': scrape['item_rating']['rating_count'][1],
                'prod_rate_star_5': scrape['item_rating']['rating_count'][0],
                'product_total_rating': scrape['item_rating']['rating_star'],
                'stock': scrape['stock'],
                'units_sold': scrape['historical_sold'],
                'status': scrape['status'],
                'shop_location': scrape['shop_location'],
                'shop_is_on_flash_sale': scrape['is_on_flash_sale'],
                'shop_is_preferred_plus_seller': scrape['is_preferred_plus_seller'],
                'feature_lowest_price_guarantee': scrape['has_lowest_price_guarantee'],
                'feature_can_use_bundle_deal': scrape['can_use_bundle_deal'],
                'feature_can_use_cod': scrape['can_use_cod'],
                'feature_can_use_wholesale': scrape['can_use_wholesale'],
                'feature_show_free_shipping': scrape['show_free_shipping'],
                'product_image_variation': scrape['images'],
                'product_text_variation': scrape['tier_variations'],
            }


@defer.inlineCallbacks
def run():
    main_crawl = CrawlerRunner()
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    yield main_crawl.crawl(ClothesSpider)
    reactor.stop()


if __name__ == '__main__':
    run()
    reactor.run()
    time.sleep(0.10)
