import sqlite3
from datetime import date


class JobOffersEmail:
    def __init__(self, db_path="jobs.db"):
        self.db_path = db_path

    def get_today_offers(self):

        today = date.today().isoformat()
        query = """
        SELECT name, date, location, job
        FROM projects
        WHERE date = ?;
        """
        with sqlite3.connect(self.db_path) as conn:
            return conn.execute(query, (today,)).fetchall()

    def generate_subject(self):

        today = date.today().strftime("%Y-%m-%d")
        return f"Job Offers {today}"

    def generate_body(self):

        offers = self.get_today_offers()
        if not offers:
            return "No job offers found for today."

        body = "Today's Job Offers:\n\n"
        for offer in offers:
            name, job_date, location, company = offer
            body += f"Job: {name}\nDate: {job_date}\nLocation: {location}\nCompany: {company}\n\n"

        return body
