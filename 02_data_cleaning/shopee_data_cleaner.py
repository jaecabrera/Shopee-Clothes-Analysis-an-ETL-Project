import pandas as pd
import warnings
from ast import literal_eval
from datetime import date
from load.load_helper import LoadHelper
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

# find the updated files for this date
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

data.head()

# output file
print('File Exported')
data.to_csv(save_dir + '/' + f'{df.time()}-product_data.csv')
