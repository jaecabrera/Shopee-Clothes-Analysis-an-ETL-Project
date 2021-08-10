# Shopee ETL Project 
Final Dataset Output Link:  https://www.kaggle.com/jaepin/shopeeph-koreantop-clothing

## About

The project's aim is to collect data from the E-commerce platform Shopee and create
an insightful dashboard for competetive analysis. This project helps to gain insights
on 5 business problems. 

- What is the **pricing strategy** of the clothing retailing segment?
- What are **product qualities** and **service qualities** to watch out for. 
- How much online demand is there for a niche product category?
- What are some of the barriers to entry?
- How competetitive is e-retailing platform?


## Data Collection

For this project we'll be dealing with flat files `.json` & `.csv`. Shopee has a dynamic webpage that
uses json files for their system. 

1. `data_collection_spiders\mainscraper.py`
  is a `scrapy basic spider` that scrapes general product information.
  such as product id, price, rating as well as other features (product variation etc.).
  The output file will are saved at `/shopee_etl_project/extract_exports` as a flat `.csv`
  
2. The product data from step 1 only has a few information on the product. 
![image](https://user-images.githubusercontent.com/84308320/128824644-5b61a564-8255-461b-b19c-8477f433210d.png)


