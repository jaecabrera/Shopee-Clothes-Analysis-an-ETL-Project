import pandas as pd
import numpy as np
import warnings
from time import ctime
from ast import literal_eval
from datetime import date
from load.load_helper import LoadHelper
from review_cleaner.clean_r import ReviewCleaner

warnings.filterwarnings(action='ignore')
today = date.today()

in_dir = '../extracted_files'
save_dir = '../04_clean_files'

# create object: LoadHelper
df = LoadHelper(
    filepath=in_dir,
    date='None')

# create list of those files
files = [items for items in df.data_directory()]

# Product Data Cleaning ---------------------------------------
for item in files:

    if item.startswith(df.time()) & item.endswith('.csv'):
        if 'product' in item:
            product_df = pd.read_csv(f'{df.filepath}\\{item}')

data = product_df


# Product Cleaning
# from product_brands with 0, None, 'nan' -> No Brand
def clean_product_brand(df):
    pb = df.product_brand

    # change series data type to string
    pb = pb.astype('string')

    # replace nan entries with 'No Brand'
    pb.fillna('No Brand', inplace=True)

    # second pass for no brands
    pb.replace({
        '0': 'No Brand',
        'None': 'No Brand',
        'nan': 'No Brand'
    }, inplace=True)

    df.product_brand = pb

    return df


print("Cleaning Product Brand....")
data = clean_product_brand(data)

# Product Prices
data.product_price = [
    *map(lambda string: string[:-5], data.product_price. \
         astype('string'))]

data.product_price_min = [
    *map(lambda string: string[:-5], data.product_price_min. \
         astype('string'))]

data.product_price_max = [
    *map(lambda string: string[:-5], data.product_price_max. \
         astype('string'))]

print("Cleaning Product Prices....")


# Boolean Values
def transform_bool(df):
    original = df.copy(deep=True)
    bool_df = df.select_dtypes('bool')
    bool_df = bool_df.astype('int')

    original.drop(
        columns=original.select_dtypes('bool').columns.tolist())

    return original.append(bool_df)


data_bool = data.select_dtypes('bool').astype('int')
data.drop(columns=list(data.select_dtypes('bool')), inplace=True)
data_clean = data.join(data_bool, how='right')
data_clean = data_clean.set_index('product_itemid')

data = data_clean
print("Cleaning Boolean Values....")

# product total rating
data['product_total_rating'] = data.product_total_rating. \
    apply(lambda num: round(num, 2))

# fill nans in product_text_variation
data.product_text_variation.fillna(
    "{'name': 'None', 'options': [], 'images': None, 'properties': [], 'type': 0}",
    inplace=True)

# round off rating
data['product_total_rating'] = data.product_total_rating.apply(
    lambda rates: round(rates, 2))
print("Cleaning Product Ratings....")

# Product Variation
# drop product image variation
data.drop(columns='product_image_variation', inplace=True)

# convert nested dictionary in text variation to list
variation_list = []
for items in data.product_text_variation:
    variation_list.append(items)

# function to count variations
product_vars = []

for i in range(0, len(data)):
    try:
        product_vars. \
            append(len(literal_eval(variation_list[i]. \
                                    lstrip('[').rstrip(']'))['options']))

    except TypeError:
        product_vars. \
            append(len(literal_eval(variation_list[i]. \
                                    lstrip('[').rstrip(']'))[0]['options']))

# insert series into dataframe
data['product_variation_count'] = product_vars

# drop product text variations
data.drop(columns='product_text_variation', inplace=True)

# output file
print('File Exported')
data.to_csv(save_dir + '/' + f'{df.time()}-product_data.csv')

# Review Data Cleaning ---------------------------------------

for item in files:

    if item.startswith(df.time()) & item.endswith('review(DIRTY).json'):
        review_filepath = f'{df.filepath}\\{item}'
        review_df = pd.read_json(review_filepath)

# Process - Review Data, DATAFRAME: review_df)
rcleaner = ReviewCleaner()
clean_data = rcleaner.create_frame(review_df)
clean_data = rcleaner.create_tag_series(clean_data)
clean_data_with_tags = rcleaner.count_rate_tags(review_df, clean_data)

# remove \n's in comment strings
clean_data['comment'] = clean_data['comment'].str.replace('\n', ' ')

# drop tags column with dictionary
clean_data = clean_data.drop(columns='tags')

# set cmtid as dataframe index
clean_data = clean_data.set_index('cmtid')

# Output - Review Data, DATAFRAME: clean_data
clean_data.to_csv(save_dir + '/' + f'{df.time()}-review_data.csv')

# Shop Data Cleaning ---------------------------------------

for item in files:
    if item.startswith(df.time()) & item.endswith('shop(DIRTY).json'):
        shop_df = pd.read_json(f'{df.filepath}\\{item}')

# copy shop dataframe to var data
data = shop_df.copy(deep=True)

# drop na shops
data.dropna(inplace=True)

# get json data as list
json_list = []
for json_object in data.shop_data[:]:
    json_list.append(json_object)

# normalize data into 1 dataframe
shop_normalize_data = pd.json_normalize(json_list)
shop_normalize_data.head()

# get needed features
shop_data = shop_normalize_data[[
    'shopid',
    'ctime',
    'name',
    'item_count',
    'follower_count',
    'response_rate',
    'response_time',
    'shop_location',
    'is_shopee_verified',
    'is_official_shop',
    'rating_bad',
    'rating_good',
    'rating_normal',
    'rating_star',
]]

# get empty shop location with empty string
null_shop_data = shop_data.query("shop_location == ''").copy(deep=True)

# replace empty string with null values
null_shop_data.shop_location = np.nan

# get indexes of these null values
null_shop_location_indexes = np.asarray(null_shop_data.index)

# match and replace values in shop data
shop_data.iloc[null_shop_location_indexes] = null_shop_data

# convert boolean to (0,1) int values
shop_data[['is_shopee_verified', 'is_official_shop']] = shop_data[
    ['is_shopee_verified', 'is_official_shop']].astype('int')

# convert ctime column to time string
time_data = shop_data['ctime'].apply(lambda time: ctime(time))

# convert string to datetime object
time_data = pd.to_datetime(time_data)
shop_data['ctime'] = time_data

# check possible missing values for response_time
no_response_time = shop_data['response_time'].isna().sum()
null_ratio_no_response_time = no_response_time / len(shop_data)

# add dict for info
shop_data_info = {
    'shape': shop_data.shape,
    'response_time_missing': no_response_time,
    'shape_to_null_ratio': null_ratio_no_response_time,
}

# add user warning
if null_ratio_no_response_time >= 0.15:
    warnings.warn("Response Time: NULL values exceed 15% ")
    print(f'{shop_data_info}')

# response time null values
shop_data_nulls = list(shop_data[shop_data.response_time.isna()].index)
shop_data = shop_data.drop(shop_data_nulls)

# convert ctime response rate to string
shop_data['response_time'] = shop_data['response_time']. \
    apply(lambda time: ctime(time))

# get the timestamp using string selector
shop_data['response_time'] = shop_data['response_time']. \
    apply(lambda time_string: time_string[10:-5])

# round rating star to two decimal places
shop_data['rating_star'] = shop_data.rating_star. \
    apply(lambda rating: round(rating, 2))

# split data
shop_data['join_month'] = shop_data['ctime'].dt.month_name()
shop_data['join_day'] = shop_data['ctime'].dt.day
shop_data['join_year'] = shop_data['ctime'].dt.year
shop_data = shop_data.drop(columns='ctime')

# re-arrange shop_data columns
shop_data = shop_data[
    [
        'shopid',
        'name',
        'join_month',
        'join_day',
        'join_year',
        'item_count',
        'follower_count',
        'response_time',
        'response_rate',
        'shop_location',
        'rating_bad',
        'rating_good',
        'rating_normal',
        'rating_star',
        'is_shopee_verified',
        'is_official_shop',
    ]
]

# shopid as dataframe index
shop_data = shop_data.set_index('shopid')

# output file
shop_data.to_csv(save_dir + '/' + f'{df.time()}-shop_data.csv')
