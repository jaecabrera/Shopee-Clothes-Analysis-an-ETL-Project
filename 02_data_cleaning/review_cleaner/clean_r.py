from dataclasses import dataclass
import pandas as pd
import numpy as np


@dataclass
class ReviewCleaner:

    @staticmethod
    def create_frame(data):
        entries = len(data['comments_compilation'])
        empty_dataframe = pd.DataFrame()
        empty_dataframe['itemid'] = [data['comments_compilation'].values[i]['itemid'] for i in range(0, entries)]
        empty_dataframe['shopid'] = [data['comments_compilation'].values[i]['shopid'] for i in range(0, entries)]
        empty_dataframe['cmtid'] = [data['comments_compilation'].values[i]['cmtid'] for i in range(0, entries)]
        empty_dataframe['author_username'] = [data['comments_compilation'].values[i]['author_username'] for i in
                                              range(0, entries)]
        empty_dataframe['comment'] = [data['comments_compilation'].values[i]['comment'] for i in range(0, entries)]
        empty_dataframe['rating_star'] = [data['comments_compilation'].values[i]['rating_star'] for i in
                                          range(0, entries)]
        empty_dataframe['tags'] = [data['comments_compilation'].values[i]['tags'] for i in range(0, entries)]

        return empty_dataframe

    @staticmethod
    def create_tag_series(dataframe):

        positive_tag_list = [
            'no_tag',
            'pos_good_quality',
            'pos_excellent_quality',
            'pos_very_accomodating',
            'pos_well_packaged',
            'pos_item_shipped_immediately',
            'pos_will_order_again']

        negative_tag_list = [
            'neg_defective',
            'neg_did_not_receive_item',
            'neg_damaged_packaging',
            'neg_will_not_order_again',
            'neg_rude_seller',
            'neg_item_shipped_late',
            'neg_item_different_from_picture',
        ]

        for positive_items in positive_tag_list:
            dataframe[positive_items] = np.zeros(len(dataframe), dtype='int')

        for negative_items in negative_tag_list:
            dataframe[negative_items] = np.zeros(len(dataframe), dtype='int')

        return dataframe

    @staticmethod
    def count_rate_tags(original_data, clean_data):

        for i in range(0, len(clean_data)):
            try:
                for items in original_data.comments_compilation[i]['tags']:

                    # positive sentiments
                    if str.lower(items.get('tag_description')) == 'excellent quality ':
                        clean_data.iloc[i, clean_data.columns.get_loc('pos_excellent_quality')] = 1

                    if str.lower(items.get('tag_description')) == 'very accommodating seller ':
                        clean_data.iloc[i, clean_data.columns.get_loc('pos_very_accomodating')] = 1

                    if str.lower(items.get('tag_description')) == 'well-packaged':
                        clean_data.iloc[i, clean_data.columns.get_loc('pos_well_packaged')] = 1

                    if str.lower(items.get('tag_description')) == 'item shipped immediately ':
                        clean_data.iloc[i, clean_data.columns.get_loc('pos_item_shipped_immediately')] = 1

                    if str.lower(items.get('tag_description')) == 'will order again ':
                        clean_data.iloc[i, clean_data.columns.get_loc('pos_will_order_again')] = 1

                    # negative sentiments

                    if str.lower(items.get('tag_description')) == 'damaged / defective item':
                        clean_data.iloc[i, clean_data.columns.get_loc('neg_defective')] = 1

                    if str.lower(items.get('tag_description')) == 'did not receive item':
                        clean_data.iloc[i, clean_data.columns.get_loc('neg_did_not_receive_item')] = 1

                    if str.lower(items.get('tag_description')) == 'damaged packaging':
                        clean_data.iloc[i, clean_data.columns.get_loc('neg_damaged_packaging')] = 1

                    if str.lower(items.get('tag_description')) == 'will not order again':
                        clean_data.iloc[i, clean_data.columns.get_loc('neg_will_not_order_again')] = 1

                    if str.lower(items.get('tag_description')) == 'rude seller ':
                        clean_data.iloc[i, clean_data.columns.get_loc('neg_rude_seller')] = 1

                    if str.lower(items.get('tag_description')) == 'item shipped very late ':
                        clean_data.iloc[i, clean_data.columns.get_loc('neg_item_shipped_late')] = 1

                    if str.lower(items.get('tag_description')) == 'item different from picture ':
                        clean_data.iloc[i, clean_data.columns.get_loc('neg_item_shipped_late')] = 1

            except TypeError:

                clean_data.iloc[i, clean_data.columns.get_loc('no_tag')] = 1

                continue
