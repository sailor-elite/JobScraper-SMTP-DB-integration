from datetime import datetime

import requests
from bs4 import BeautifulSoup
import locale
locale.setlocale(locale.LC_TIME, 'pl_PL.UTF-8')


months_map = {
        "stycznia": "-01-", "lutego": "-02-", "marca": "-03-", "kwietnia": "-04-",
        "maja": "-05-", "czerwca": "-06-", "lipca": "-07-", "sierpnia": "-08-",
        "września": "-09-", "października": "-10-", "listopada": "-11-", "grudnia": "-12-"
    }

class OLX_Scrapper:
    def __init__(self):
        self.URL = "https://www.olx.pl/praca/lomza/"

    def fetch_jobs(self):

        try:
            max_number = 0
            response = requests.get(self.URL)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            numbers = soup.find_all("a", class_="css-b6tdh7")
            for number in numbers:
                raw_numbers = int(number.get_text(strip=True))

                if raw_numbers > max_number:
                    max_number = raw_numbers

            jobs = []

            for i in range(0,max_number):
                new_URL = self.URL + f"?page={i}"
                job_response = requests.get(new_URL)
                job_response.raise_for_status()
                soup = BeautifulSoup(job_response.text, "html.parser")
                job_names = soup.find_all("a", class_="css-13gxtrp")
                job_employees = soup.find_all("p", class_="css-1rpfcm7")
                job_dates = soup.find_all("p", class_="css-996jis")
                print(new_URL)
                for name, place, date in zip(job_names,job_employees, job_dates):
                    job_title = name.get_text(strip=True)
                    job_location = place.get_text(strip=True)

                    job_date = date.get_text(strip=True)
                    if "Dzisiaj" in job_date:
                        job_date = job_date.replace(job_date, datetime.today().strftime("%d.%m.%Y"))
                    elif "Odświeżono dnia" in job_date:
                        job_date = job_date.replace("Odświeżono dnia", "")
                    elif "Dzisiaj" not in job_date:
                        for month_name, month_num in months_map.items():
                            print(job_date, " ", month_name)
                            if month_name in job_date:
                                job_date = job_date.replace(month_name, month_num).replace(" ","")
                                job_date = datetime.strptime(job_date, "%d-%m-%Y").strftime("%d.%m.%Y")
                                break
                    jobs.append({"name": job_title, "date": job_date, "location": job_location, "source": "OLX"})
                return jobs

        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None
