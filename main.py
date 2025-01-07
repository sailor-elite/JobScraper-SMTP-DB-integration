from piatnica import PiatnicaJobScrapper
from Zurad import ZuradJobScraper
from Pgz import PGZJobScraper
from OrlenPetrobaltic import OrlenJobScraper

def Piatnica():
    url = "https://piatnica.com.pl/biznes/praca/"
    scraper = PiatnicaJobScrapper(url)
    scraper.fetch_data()
    scraper.parse_jobs()
    scraper.display_jobs()

def PGZ():
    scraper = PGZJobScraper("https://grupapgz.pl/kariera/")
    scraper.ScrapeAllJobs()

def Zurad():
    url = "https://zurad.com.pl/ogloszenia-o-prace/"
    scraper = ZuradJobScraper(url)
    scraper.fetch_data()
    scraper.parse_update_dates()
    scraper.parse_job_positions()
    scraper.display_updates()
    scraper.display_job_positions()

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
        scraper.display_jobs() 

print("PIATNICA: " + '\n')
Piatnica()
print('\n' + "ZURAD: " + '\n')
Zurad()
print('\n' + "ORLEN PETROBALTIC: " + '\n')
Orlen()
print('\n' + "PGZ: " + '\n')
PGZ()
