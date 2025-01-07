import requests
from bs4 import BeautifulSoup


class JobPost:
    def __init__(self, position, date, location, region):
        self.position = position
        self.date = date
        self.location = location
        self.region = region

    def __str__(self):
        return f"STANOWISKO: {self.position}\nDATA: {self.date}\nMIEJSCOWOSC: {self.location}\nWOJEWODZTWO: {self.region}\n"


class OrlenJobScraper:
    def __init__(self, url):
        self.url = url
        self.job_posts = []

    def fetch_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Problem z pobraniem danych: {e}")
            return None

    def parse_jobs(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all("td")

        job_data = []
        for tag in tags:
            text = tag.get_text(strip=True)
            if "ORLEN Petrobaltic" in text:
                continue
            job_data.append(text)

            if len(job_data) == 4:  
                position, date, location, region = job_data
                job_post = JobPost(position, date, location, region)
                self.job_posts.append(job_post)
                job_data = []

    def display_jobs(self):
        for job in self.job_posts:
            job = print(job)
        return job
