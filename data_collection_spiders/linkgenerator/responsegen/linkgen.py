from dataclasses import dataclass
from itertools import zip_longest
import re
import pandas as pd


@dataclass
class ShopeeScrape:
    """
    This class helps generate links by concatenating IDs from our scraped data.
    """
    # https://shopee.ph/(!product-name)-i.(!shopid).(!productid)
    # https://shopee.ph/api/v2/item/
    # https://cf.shopee.ph/file/
    # https://shopee.ph/api/v4/product/get_shop_info?
    product_link: str
    review_link: str
    image_link: str
    shop_link: str

    def get_product(self, name, shop, product):
        """Generates shopee product links"""
        name = name.str.replace(' ', '-')
        shop = shop.astype('string')
        product = product.astype('string')

        ids = shop + '.' + product
        name_encode = name.str.encode('ascii', 'ignore')
        name_decode = name_encode.str.decode('ascii')
        name_decode = [*map(lambda x: re.sub(r'[^\w]', '', x), name_decode)]

        # pair
        urls = [
            self.product_link + name + '-i.' + id for id, name in zip_longest(ids, name_decode)
        ]

        return urls

    def get_image(self, image_code):
        """Generates image links for reference"""
        image_variations = pd.DataFrame()
        image_variations['code'] = image_code
        variation_expand = image_variations['code'].str.split(',', expand=True)
        variation_expand = variation_expand[0]
        variation_expand = variation_expand.apply(lambda i: self.image_link + i)

        return variation_expand

    def get_review(self, shop, product):
        """ Generates shopee product links """
        shop = shop.astype('string')
        product = product.astype('string')
        base1 = 'get_ratings?filter=0&flag=1&itemid='
        base2 = '&limit=50&offset=0&shopid='
        base3 = '&type=0'

        # pair
        return [
            self.review_link + base1 + prod + base2 + shp + base3 for prod, shp in zip_longest(product, shop)
        ]

    def get_shop_profile_link(self, shop):
        """ Generates Shopee shop profile Links """
        shop = shop.apply(lambda i: self.shop_link + str(i))
        return shop
