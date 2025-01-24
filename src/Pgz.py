import requests


class JobPost:
    def __init__(self, title, date_posted, location):
        self.title = title
        self.date_posted = date_posted
        self.location = location

    def __str__(self):
        return f"Position: {self.title}\nDate: {self.date_posted}\nLocation: {self.location}\n"


class PGZJobScraper:
    def __init__(self):
        self.api_url = "https://pcw-api.softgarden.de/widget-api/job-list/jobAds/"
        self.headers = {
            "Content-Type": "application/json",
            "Origin": "https://kariera.grupapgz.pl",
            "Referer": "https://kariera.grupapgz.pl/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
        }
        self.payload = {
            "userId": "b87400e0-b37d-4ba9-85ea-346bd54a094b",
            "projectId": "ec53ad54-7b23-47d4-b33b-f2244a27a759",
            "pageId": "dfa8c272-7e43-441e-bc43-ab4c95ada584",
            "locale": "pl",
            "isActiveCustomJobPages": False,
            "isUseLayoutsOfSubsidiaries": False,
            "filterStatus": {
                "careerLevel": False,
                "category": True,
                "partnership": True,
                "region": True,
                "location": True
            },
            "listState": {
                "search": "",
                "location": {},
                "filters": {},
                "filterPredictions": {}
            },
            "jobListTitleNew": "Nowa",
            "isForCurrentLocale": False,
            "isStandalone": False
        }

    def fetch_jobs(self, page_number=1, jobs_per_page=1024):

        self.payload.update({
            "pageNumber": page_number,
            "numberOfJobsOnPage": jobs_per_page
        })

        try:
            response = requests.post(self.api_url, headers=self.headers, json=self.payload)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"error with getting date: {e}")
            return None

    def parse_jobs(self, data):

        jobs = data.get("data", {}).get("jobs", [])

        job_posts = []
        for job in jobs:
            title = job.get("title", "no title")
            date_posted = job.get("date", "no date")
            location = job.get("location", "no location")
            job_posts.append(JobPost(title, date_posted, location))
        return job_posts

    def scrape_all_jobs(self):

        all_jobs = []
        page_number = 1

        while True:
            print(f"Downloading site number {page_number}...")
            data = self.fetch_jobs(page_number=page_number)

            if not data:
                print("No further data or error.")
                break

            job_posts = self.parse_jobs(data)
            if not job_posts:
                print("No further job offers.")
                break

            all_jobs.extend(job_posts)
            page_number += 1

        return all_jobs


