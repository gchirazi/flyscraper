from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Google Sheets setup
SPREADSHEET_URL = "https://docs.google.com/spreadsheets/d/1uSeNUeyOg3L92ZRCqHlWVgPficsQev4U3o7AcmJ8nNg/edit#gid=0"
CREDENTIALS_FILE = "quiet-maxim-453111-d1-d53861804702.json"

# Selenium setup
def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Price extraction Ryanair
def get_ryanair_price_back(driver):
    url = "https://www.ryanair.com/gb/en/trip/flights/select?adults=2&dateOut=2025-04-22&originIata=BVA&destinationIata=OTP"
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 15)
        price_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "flight-card-summary__full-price")))
        price = price_element.text.strip().replace("€", "").replace(",", ".")
        return float(price)
    except Exception as e:
        print(f"Eroare Ryanair: {e}")
        return None

def get_ryanair_price_go(driver):
    url = "https://www.ryanair.com/gb/en/trip/flights/select?adults=2&teens=0&children=0&infants=0&dateOut=2025-04-17&dateIn=&isConnectedFlight=false&discount=0&promoCode=&isReturn=false&originIata=OTP&destinationIata=BVA&tpAdults=2&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2025-04-17&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=OTP&tpDestinationIata=BVA"
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 15)
        price_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "flight-card-summary__full-price")))
        price = price_element.text.strip().replace("€", "").replace(",", ".")
        return float(price)
    except Exception as e:
        print(f"Eroare Ryanair: {e}")
        return None


# Funcțion for Google Sheets
def update_google_sheet(ryanair_price_back, ryanair_price_go):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(SPREADSHEET_URL).sheet1
    
    sheet.append_row([time.strftime("%Y-%m-%d %H:%M"), ryanair_price_back, ryanair_price_go, (ryanair_price_back + ryanair_price_go) * 4.98])

# Run the script
if __name__ == "__main__":
    driver = setup_driver()
    ryanair_price_back = get_ryanair_price_back(driver)
    ryanair_price_go = get_ryanair_price_go(driver)
    driver.quit()
    update_google_sheet(ryanair_price_back, ryanair_price_go)
