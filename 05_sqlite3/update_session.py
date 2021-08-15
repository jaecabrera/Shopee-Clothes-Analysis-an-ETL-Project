import pandas as pd
import os
from datetime import datetime, timedelta
from pandas.core.common import flatten
from sqlalchemy import create_engine


def create_pk(dataframe: pd.DataFrame(), date_today, pk_series: str, data_id: str) -> pd.DataFrame:
    """
    Creates date_collected and primary key id for the
        dataframe.
    :param dataframe: Dataframe chosen to create primary key.
    :param date_today: date to represent the date of collection.
    :param pk_series: primary key column name.
    :param data_id: name of the id in column e.g. 'product_itemid', 'shopid', etc.
    :returns: DataFrame with date + id as primary key for SQL DB.
    """

    dataframe['date_collected'] = date_today
    dataframe[pk_series] = dataframe['date_collected'].astype('string') + dataframe[data_id].astype('string')
    dataframe[pk_series] = dataframe[pk_series].str.replace('-', '')
    columns = [*dataframe.columns]
    base_columns = columns[:-2]
    add_columns = [pk_series, 'date_collected']

    for items in base_columns:
        add_columns.append(items)

    dataframe = dataframe[add_columns]

    return dataframe


# create connection to database
engine = create_engine('sqlite:///shopee.db', echo=True)
fp = '../04_clean_files'

# time factor
yesterday = datetime.today() - timedelta(days=1)
today = yesterday.strftime('%Y-%m-%d')

# get today's files
today_files = [[items for items in file if items.startswith(str(today))] for _, _, file in os.walk(fp)]

# create list of dataframe of today's files.
frames_compiled = []
for items in [*flatten(today_files)]:
    read_df = pd.read_csv(fp + '/' + items)
    frames_compiled.append(read_df)

product = create_pk(
    # Product DataFrame
    frames_compiled[0],
    date_today=today,
    pk_series='pk_product',
    data_id='product_itemid'
)

review = create_pk(
    # Review DataFrame
    frames_compiled[1],
    date_today=today,
    pk_series='pk_review',
    data_id='cmtid'
)

shop = create_pk(
    # Shop DataFrame
    frames_compiled[2],
    date_today=today,
    pk_series='pk_shop',
    data_id='shopid'
)

# Insert Data to SQLite DB
# Shop Data
shop.to_sql('Shop', con=engine, index=0, if_exists='append')

# Product Data
product.to_sql('Product', con=engine, index=0, if_exists='append')

# Review Data
review.to_sql('Review', con=engine, index=0, if_exists='append')
