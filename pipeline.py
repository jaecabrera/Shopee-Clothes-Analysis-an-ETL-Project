import subprocess
import time


def collect():
    subprocess.run('python3 ./01_data_collection_spiders/main_scraper.py', shell=True)

    def generate():
        subprocess.run('python3 ./03_link_generator/generator_pipe.py')

    generate()
    subprocess.run('python3 ./01_data_collection_spiders/shop_profile_and_review_scraper.py', shell=True)


def clean():
    subprocess.run('python3 ./02_data_cleaning/shopee_data_cleaner.py')


def store():
    subprocess.run('python3 ./05_sqlite3/update_session.py')


if __name__ == '__main__':
    collect()
    clean()
    store()
