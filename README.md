# Ryanair Price Scraper

This project is an **automated scraper** that collects flight ticket prices from the **Ryanair** website (round trip) and saves them in a **Google Sheet** for monitoring.

## Features
- Automatically extracts flight ticket prices from **Ryanair** (both outbound and return flights)
- Saves data in a **Google Spreadsheet**  
- Runs automatically without manual interaction (using `cron` or `Task Scheduler`)  
- Uses **Selenium WebDriver** for web scraping  
- Secure authentication with **Google Sheets API** via Google Cloud  

---

## Technologies Used
- **Python** - main programming language  
- **Selenium** - for web scraping  
- **gspread** - for interacting with Google Sheets  
- **Google Cloud Platform** - for API authentication  
- **WebDriver Manager** - for handling Chrome drivers  

---

## Installation and Setup

### 1. Install Dependencies
Make sure you have **Python 3.10+** installed, then run:  
```bash
pip install selenium webdriver-manager gspread oauth2client selenium-stealth
```

### 2. Set Up Google Cloud API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)  
2. Create a **new project**  
3. Enable **Google Sheets API**  
4. Create a **Service Account** and download the JSON key file  
5. Share your Google Sheet with the email found in the JSON file  

### 3. Configure Chrome WebDriver
The script uses `webdriver-manager`, but ensure you have **Google Chrome installed**.

---

## Usage

### 1. Configure the File
Update `CREDENTIALS_FILE` with the path to your downloaded JSON file:  
```python
CREDENTIALS_FILE = "\path\to\service-account.json"
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/example/edit#gid=0"
```
Ensure `SPREADSHEET_URL` is correctly set.

### 2. Run the Script
To manually execute the script, run:
```bash
python bilete.py
```
This will:  
- Open Chrome in headless mode  
- Access the Ryanair website and extract flight prices  
- Save the data into Google Sheets  

### 3. Automate the Script (Schedule Execution)

#### Linux/Mac - Using `cron`
Add this to crontab (`crontab -e`):
```bash
0 * * * * /usr/bin/python3 /path/to/bilete.py
```
This will run the script **every hour**.

#### Windows - Using Task Scheduler
1. Open **Task Scheduler**  
2. Create a **new task** → Add `python bilete.py` as an action  
3. Set it to run **every hour**  

---

## Project Structure
```
flyscraper/
│── bilete.py            # Main script
│── service_account.json  # Google Sheets API key (DO NOT SHARE!)
│── README.md             # Documentation
```

---

## Technical Explanation
- **Selenium WebDriver** → Controls Chrome and interacts with the Ryanair website  
- **Web Scraping** → Finds HTML elements containing flight prices  
- **Google Sheets API** → Enables automatic data writing into Google Sheets  
- **Automation** → Scheduled execution using `cron` or Task Scheduler  

---

## Example Data Saved in Google Sheets

| Date & Time       | Ryanair Outbound (€) | Ryanair Return (€) | Total (RON) |
|-------------------|---------------------|---------------------|-------------|
| 2025-03-17 12:00 | 39.99                | 49.99               | 445.02      |
| 2025-03-17 13:00 | 42.50                | 50.00               | 456.45      |

The total amount is calculated directly in the script:
```python
sheet.append_row([time.strftime("%Y-%m-%d %H:%M"), ryanair_price, wizzair_price, (ryanair_price + wizzair_price) * 4.98])
```
