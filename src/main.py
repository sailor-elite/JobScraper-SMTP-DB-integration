from piatnica import PiatnicaJobScrapper
from Zurad import ZuradJobScraper
from Pgz import PGZJobScraper
from OrlenPetrobaltic import OrlenJobScraper
from db_handler import DataHandler
from db_init import Database

data_handler = DataHandler('jobs.db')
def Database_init():
    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    date text NOT NULL,
                                    job text NOT NULL
                                ); """
    db = Database('jobs.db')
    db.conn = db.create_connection(db.db_file)
    db.create_table(sql_create_projects_table)
    db.conn.close()





def Piatnica():
    url = "https://piatnica.com.pl/biznes/praca/"
    scraper = PiatnicaJobScrapper(url)
    scraper.fetch_data()
    jobs = scraper.parse_jobs()
    scraper.display_jobs()
    for job in jobs:
        job_data = (job.name, job.date, job.location)
        data_handler.insert_data(job_data)


def PGZ():
    scraper = PGZJobScraper()
    jobs = scraper.scrape_all_jobs()

    if jobs:
        print("Oferty pracy PGZ:")
        for job in jobs:
            job_data = (job.title, job.date_posted, job.location)
            data_handler.insert_data(job_data)

    else:
        print("Brak ofert pracy z PGZ.")


def Zurad():
    url = "https://zurad.com.pl/ogloszenia-o-prace/"
    scraper = ZuradJobScraper(url)

    scraper.fetch_data()

    scraper.parse_update_dates()
    scraper.parse_job_positions()
    date = scraper.update_dates
    for job in scraper.job_positions:
        job_data = (job.position, str(date[0]), 'Zurad')
        data_handler.insert_data(job_data)


def Orlen():
    url = (
        "https://skk.erecruiter.pl/GetHtml.ashx?"
        "cfg=76b98f485df044c9a6e71c52f6cb8632&grid=rows&pn=1&jt=&wp=&af_100=51"
        "&sc=skk_col_publish_date&sd=desc&jsoncallback=jsonp1735214136921&_=1735214546091"
    )
    scraper = OrlenJobScraper(url)
    html_data = scraper.fetch_data()

    if html_data:
        scraper.parse_jobs(html_data)
        jobs = scraper.job_posts
        for job in jobs:
            job_data = (job.position, job.date, job.location)
            data_handler.insert_data(job_data)


if __name__ == "__main__":

    Database_init()

    try:
        print('\n' + "ZURAD: " + '\n')
        Zurad()
    except Exception as e:
        print(f"errror in ZURAD: {e}")

    try:
        print("PIATNICA: " + '\n')
        Piatnica()
    except Exception as e:
        print(f"error in PIATNICA: {e}")
    try:
        print('\n' + "PGZ: " + '\n')
        PGZ()
    except Exception as e:
        print(f"error in PGZ: {e}")

    try:
        print('\n' + "ORLEN PETROBALTIC: " + '\n')
        Orlen()
    except Exception as e:
        print(f"error in ORLEN PETROBALTIC: {e}")
