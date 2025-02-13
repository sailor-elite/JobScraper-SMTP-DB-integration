# JobScraper-SMTP-DB-integration

## Project Description
JobScraper-SMTP-DB-integration is a script that automates the process of fetching job offers, sending them via Gmail, and storing them in a database.

## Requirements
- Python 3.x
- Libraries listed in `requirements.txt`
- SMTP account for sending emails

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repository/JobScraper-SMTP-DB-integration.git
   cd JobScraper-SMTP-DB-integration
   ```
2. Install the required libraries:
   ```sh
   pip install -r requirements.txt
   ```
3. Configure environment variables or `.env` file by setting:
   ```env
   EMAIL_SENDER=your_email@example.com
   EMAIL_PASSWORD=your_email_password
   EMAIL_RECEIVER='["email_receiver", "email_receiver", "email_receiver", "etc" ]'
   ```

## Running the Script
To run the script, use the command:
```sh
python main.py
```

## Project Structure
```
JobScraper-SMTP-DB-integration/
│── src/
│   │── db_handler.py        # Module for handling database operations
│   │── db_init.py           # Database initialization script
│   │── JobOffersEmail.py    # Handles email notifications for job offers
│   │── jobs.db              # SQLite database storing job offers
│   │── main.py              # Main script entry point
│   │── OrlenPetrobaltic.py  # Scraper for Orlen Petrobaltic job offers
│   │── Pgz.py               # Scraper for PGZ job offers
│   │── piatnica.py          # Scraper for Piatnica job offers
│   │── SMTP_Handler.py      # Module for handling SMTP email operations
│   │── Zurad.py             # Scraper for Zurad job offers
│── requirements.txt         # List of required libraries
│── README.md                # Project documentation
```


