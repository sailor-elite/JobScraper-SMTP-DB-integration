import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class JobPost:
    def __init__(self, position, location, company):
        self.position = position
        self.location = location
        self.company = company

    def __str__(self):
        return f"STANOWISKO: {self.position}\nMIEJSCOWOŚĆ: {self.location}\nFIRMA: {self.company}\n"


class PGZJobScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.job_posts = []

    def FetchData(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Problem z pobraniem danych: {e}")
            return None

    def ParseAndOutput(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        tags = soup.find_all("td")

        job_data = []
        for index, tag in enumerate(tags):
            job_data.append(tag.get_text(strip=True))
            if (index + 1) % 3 == 0:
                position, location, company = job_data
                job_post = JobPost(position, location, company)
                self.job_posts.append(job_post)
                print(job_post)
                job_data = []

    def LastPageNumber(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(self.base_url)
        try:
            element = driver.find_element(By.CLASS_NAME, "skk_pager_last")
            page_number = int(element.text.strip())
        except Exception as e:
            print(f"Błąd podczas odczytu numeru ostatniej strony: {e}")
            page_number = 1
        driver.quit()
        return page_number

    def ScrapeAllJobs(self):
        last_page = self.LastPageNumber()

        for page_number in range(1, last_page + 1):
            print(f"STRONA: {page_number}\n")
            url = (
                f"https://skk.erecruiter.pl/GetHtml.ashx?"
                f"cfg=055531097fe04079a190d2f210485080&grid=rows&pn={page_number}&jt=&wp=&kw="
                f"&sc=skk_col_publish_date&sd=desc&jsoncallback=jQuery3500673159553047447_1735646463673"
            )
            html_data = self.FetchData(url)
            if html_data:
                self.ParseAndOutput(html_data)


