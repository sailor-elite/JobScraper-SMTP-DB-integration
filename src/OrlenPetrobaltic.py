import requests
from bs4 import BeautifulSoup


class JobPost:
    def __init__(self, position, date, location, region):
        self.position = position
        self.date = date
        self.location = location
        self.region = region

    def __str__(self):
        return f"Position: {self.position}\nDate: {self.date}\nLocation: {self.location}\nVoivodeship: {self.region}\n"


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
            print(f"Error with getting data: {e}")
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
        if not self.job_posts:
            print("No offers to show.")
        else:
            for job in self.job_posts:
                print(job)


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
        return scraper.job_posts
