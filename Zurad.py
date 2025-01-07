import requests
from bs4 import BeautifulSoup

class JobUpdate:
    def __init__(self, update_date):
        self.update_date = update_date

    def __str__(self):
        return f"{self.update_date}"

class JobPosition:
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return f"{self.position}"

class ZuradJobScraper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.update_dates = []
        self.job_positions = []

    def fetch_data(self):
        response = requests.get(self.url)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def parse_update_dates(self):
        update_dates = self.soup.find_all(class_="pas3")
        for update_date in update_dates:
            main_elements = update_date.find_all(class_="col-md-12")
            for element in main_elements:
                if element.get('class') == ['col-md-12']:
                    h3_elements = element.find_all("h3")
                    for h3 in h3_elements:
                        date_text = h3.get_text(strip=True)
                        self.update_dates.append(JobUpdate(date_text))

    def parse_job_positions(self):
        job_positions = self.soup.find_all(class_='box-oferta')
        for job in job_positions:
            position_text = job.get_text(strip=True)
            self.job_positions.append(JobPosition(position_text))

    def display_updates(self):
        for update in self.update_dates:
            update = print(update)
        return update

    def display_job_positions(self):
        for job in self.job_positions:
            job = print(job)
        return job

