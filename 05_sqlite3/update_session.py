import pandas as pd
import os
from datetime import datetime
from pandas.core.common import flatten
from sqlalchemy import create_engine

engine = create_engine('sqlite:///shopee.db')
fp = '../04_clean_files'
today = datetime.today().strftime('%Y-%m-%d')
today_files = [[items for items in file if items.startswith(str(today))] for _, _, file in os.walk(fp)]

frames_compiled = []
for items in [*flatten(today_files)]:
    read_df = pd.read_csv(fp + '/' + items)
    frames_compiled.append(read_df)

# Product Data
frames_compiled[0].to_sql('Product', con=engine)

# Review Data
frames_compiled[1].to_sql('Review', con=engine)

# Shop Data
frames_compiled[2].to_sql('Shop', con=engine)
