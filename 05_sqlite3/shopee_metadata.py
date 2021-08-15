# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import (Column, String, Integer, Float, SmallInteger, ForeignKey, Date)

engine = create_engine('sqlite:///shopee.db')
Base = declarative_base()


class Shop(Base):
    __tablename__ = 'shop'

    pk_shop = Column(String(20), primary_key=True, unique=True)
    date_collected = Column(Date(), nullable=False)
    shopid = Column(String(50), nullable=False)
    name = Column(String(255))
    join_month = Column(String(10))
    join_day = Column(Integer())
    join_year = Column(Integer())
    item_count = Column(Integer())
    follower_count = Column(Integer())
    response_time = Column(String(10))
    response_rate = Column(Integer())
    shop_location = Column(String(100), nullable=True)
    rating_bad = Column(SmallInteger())
    rating_good = Column(SmallInteger())
    rating_normal = Column(SmallInteger())
    rating_star = Column(SmallInteger())
    is_shopee_verified = Column(SmallInteger())
    is_official_shop = Column(SmallInteger())

    product_relationship = relationship("Product")
    review_relationship = relationship("Review")


class Product(Base):
    __tablename__ = 'product'

    pk_product = Column(String(), primary_key=True)
    date_collected = Column(Date(), nullable=False)
    product_itemid = Column(String())
    product_shopid = Column(String(), ForeignKey('shop.shopid'))
    product_category = Column(String(10))
    product_name = Column(String(255))
    product_price = Column(Float(), nullable=True)
    product_price_min = Column(Float())
    product_price_max = Column(Float())
    product_discount = Column(Integer())
    product_brand = Column(String(255))
    product_like_count = Column(Integer())
    product_comment_count = Column(Integer())
    product_views = Column(Integer())
    prod_rate_star_0 = Column(Integer())
    prod_rate_star_1 = Column(Integer())
    prod_rate_star_2 = Column(Integer())
    prod_rate_star_3 = Column(Integer())
    prod_rate_star_4 = Column(Integer())
    prod_rate_star_5 = Column(SmallInteger())
    product_total_rating = Column(Float())
    stock = Column(Integer())
    units_sold = Column(Integer())
    status = Column(SmallInteger())
    shop_location = Column(String(255))
    shop_is_on_flash_sale = Column(SmallInteger())
    shop_is_preferred_plus_seller = Column(SmallInteger())
    feature_lowest_price_guarantee = Column(SmallInteger())
    feature_can_use_bundle_deal = Column(SmallInteger())
    feature_can_use_cod = Column(SmallInteger())
    feature_can_use_wholesale = Column(SmallInteger())
    feature_show_free_shipping = Column(SmallInteger())
    product_variation_count = Column(SmallInteger())

    product_review_relationship = relationship("Review")


class Review(Base):
    __tablename__ = 'review'

    pk_review = Column(String(), primary_key=True, unique=True)
    date_collected = Column(Date(), nullable=False)
    cmtid = Column(String(20), nullable=False)
    itemid = Column(String(), ForeignKey('product.product_itemid'))
    shopid = Column(String(), ForeignKey('shop.shopid'))
    author_username = Column(String())
    comment = Column(String())
    rating_star = Column(SmallInteger())
    no_tag = Column(SmallInteger())
    pos_good_quality = Column(SmallInteger())
    pos_excellent_quality = Column(SmallInteger())
    pos_very_accomodating = Column(SmallInteger())
    pos_well_packaged = Column(SmallInteger())
    pos_item_shipped_immediately = Column(SmallInteger())
    pos_will_order_again = Column(SmallInteger())
    neg_defective = Column(SmallInteger())
    neg_did_not_receive_item = Column(SmallInteger())
    neg_damaged_packaging = Column(SmallInteger())
    neg_will_not_order_again = Column(SmallInteger())
    neg_rude_seller = Column(SmallInteger())
    neg_item_shipped_late = Column(SmallInteger())
    neg_item_different_from_picture = Column(SmallInteger())
