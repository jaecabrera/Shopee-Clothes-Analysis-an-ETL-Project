import pandas as pd
from GeneratorHelp import ShopeeScrape
from load.load_helper import LoadHelper
from dataclasses import dataclass

# create load helper object
df = LoadHelper(filepath='extracted_files', date=None)
files = [items for items in df.data_directory()]

# date today
today = df.time()

# save filepath
save_fp = 'generated_links'

# find needed file
for item in files:
    if item.startswith(df.time()) & item.endswith('product(DIRTY).csv'):
        data = pd.read_csv(f'{df.filepath}\\{item}')

# Create ShopeeScrape Object
shs = ShopeeScrape(
    product_link='https://shopee.ph/',
    review_link='https://shopee.ph/api/v2/item/',
    image_link='https://cf.shopee.ph/file/',
    shop_link='https://shopee.ph/api/v4/product/get_shop_info?shopid=',
)


@dataclass
class GenScript:

    def __init__(self):
        self.shop_profile_links = shs.get_shop_profile_link(
            shop=data.product_shopid)

        self.review_links = shs.get_review(
            shop=data.product_shopid,
            product=data.product_itemid)

        self.image_links = shs.get_image(
            image_code=data.product_image_variation)

        self.product_link = shs.get_product(
            name=data.product_name,
            shop=data.product_shopid,
            product=data.product_itemid)

    def export(self, time_collect, save_filepath, filename):
        """
        :param time_collect: date of collection
        :param save_filepath: link generator target save directory
        :param filename: .csv filename
        """
        dataframe = pd.DataFrame()
        dataframe['product_itemid'] = data.product_itemid
        dataframe['product_shopid'] = data.product_shopid
        dataframe['product_links'] = self.product_link
        dataframe['shop_review_links'] = self.review_links
        dataframe['image_links'] = self.image_links
        dataframe['shop_profile_links'] = self.shop_profile_links
        save_to = save_filepath + '/' + time_collect + filename
        data_export = dataframe.to_csv(save_to, index=0)

        return data_export


if __name__ == '__main__':
    GenScript().export(
        time_collect=today,
        save_filepath=save_fp,
        filename='_links(BASE).csv')
