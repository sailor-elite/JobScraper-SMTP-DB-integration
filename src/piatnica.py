import requests
from bs4 import BeautifulSoup

class JobPost:
    def __init__(self, name, date, location):
        self.name = name
        self.date = date
        self.location = location

    def __str__(self):
        return f"{self.name} | {self.date} | {self.location}"

class PiatnicaJobScrapper:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.job_posts = []

    def fetch_data(self):
        response = requests.get(self.url)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def parse_jobs(self):
        elements = self.soup.find_all(class_='post-single-header')
        for element in elements:
            jobname = element.find(class_='post-single-title')
            name_text = jobname.get_text(strip=True) if jobname else "Brak nazwy"

            jobdate = element.find(class_='post-date')
            date_text = jobdate.get_text(strip=True) if jobdate else "Brak daty"

            joblocation = element.find(class_='post-place')
            location_text = joblocation.get_text(strip=True) if joblocation else "Brak lokalizacji"

            job_post = JobPost(name_text, date_text, location_text)
            self.job_posts.append(job_post)

    def display_jobs(self):
        for job in self.job_posts:
            job = print(job)
        return job

