# - Modules
import pandas as pd

# Default Clean Output Filepath
OUTPUT_FILEPATH = "E:\\cj-files\\Shopee ETL\\Global Output\\"

# load data
df = DataFarmer(
    filepath=r'E:\cj-files\Shopee ETL\Global Input',
    date='None')

# print available files with file extension .csv, .json
for items in df.data_directory():
    print(items)

# create list of those files
files = [items for items in df.data_directory()]

# find the updated files for this date
for item in files:
    if item.startswith(df.time()) & item.endswith('.json'):

        if 'review' in item:
            review_df = pd.read_json(df.filepath + '\\' + item)

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
clean_data.to_csv(OUTPUT_FILEPATH + f'{df.time()}-review_data.csv')
