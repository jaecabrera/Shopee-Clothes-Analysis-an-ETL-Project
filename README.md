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

Shopee has a dynamic webpage that uses json files for their system. 
For this project we'll be dealing with flat files `.json` & `.csv`. 

1. `data_collection_spiders\mainscraper.py`
  is a **scrapy basic spider** that scrapes general product information.
  such as product id, price, rating as well as other features (product variation etc.).
  The output file will are saved at `/shopee_etl_project/extract_exports` as a flat `.csv`
  
2. Generate response links from application `data_collection_spiders/linkgenerator/responsegen/shopee_linkgen_app.zip`.
  Select the extracted product file from step one and click on export links. Consequentially, it
  will then export a flat `.csv` file onto `generated links` folder. The links are use for our next scraper
  to get more information on the shop and review data.
  
![image](https://user-images.githubusercontent.com/84308320/128824644-5b61a564-8255-461b-b19c-8477f433210d.png)

3. Run the scraper for shop and review data using `data_collection_spiders/shop_profile_and_review_scraper.py`, it may
   take a little while compared to the previous scraper because of the number of reviews (50 newest reviews) per product.
   The scraper will output 2 `.csv` files to extracted files.
   
## Data Cleaning

1. The only step that we have to do is to run the 2 script located at `data_cleaning/shopee_data_cleaner.py`
   This script will output clean and trasformed data in `extract_exports` folder. And are tagged with (CLEAN).
   

