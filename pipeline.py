import subprocess
from datetime import timedelta
from prefect import task, Flow, Task
from prefect.schedules import IntervalSchedule


def run_script(command):
    """
    :params command: Subprocess command
    """
    subprocess.run(command)


@task(name='Product Scraper')
def collect():
    """
    Start main scraper.
    """
    cmd = 'py 01_data_collection_spiders\\main_scraper.py'
    return run_script(cmd)


@task()
def generate():
    """
    Generate Links for Review and Shop Scraper.
    """
    cmd = 'py 03_link_generator/generator_pipe.py'
    return subprocess.run(cmd)


@task(name='Review and Shop Scraper')
def collect_shop_review():
    """
    Start second scraper for Review and Shop.
    """
    cmd = 'py 01_data_collection_spiders/shop_profile_and_review_scraper.py'
    return subprocess.run(cmd)


@task()
def clean():
    """
    Run Data Cleaning Script.
    """
    cmd = 'py 02_data_cleaning/shopee_data_cleaner.py'
    return subprocess.run(cmd)


@task()
def store():
    """
    Store data to sqlite3 database.
    """
    cmd = 'py -m ./05_sqlite3/update_session.py'
    return subprocess.run(cmd)


schedule = IntervalSchedule(interval=timedelta(days=7))


def prefect_flow():
    """
    Starts Prefect Flow Pipeline
    """
    with Flow(name='shopee_etl_pipeline', schedule=schedule) as flow:
        task_generate = generate()
        task_shop_reviews = collect_shop_review()
        task_clean = clean()
        task_store = store()

        flow.set_dependencies(
            upstream_tasks=[collect()],
            task=task_generate,)

        flow.set_dependencies(
            upstream_tasks=[task_generate],
            task=task_shop_reviews)

        flow.set_dependencies(
            upstream_tasks=[task_shop_reviews],
            task=task_clean,)

        flow.set_dependencies(
            upstream_tasks=[task_clean],
            task=task_store)


    return flow


if __name__ == '__main__':
    flow = prefect_flow()
    flow.run()
