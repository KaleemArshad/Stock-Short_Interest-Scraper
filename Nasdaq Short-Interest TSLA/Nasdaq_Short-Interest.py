from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep


capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

opts = Options()
opts.add_argument('--ignore-certificate-errors')
opts.add_argument('--ignore-ssl-errors')
# opts.add_argument("--headless")

driver = webdriver.Chrome(
    desired_capabilities=capa, options=opts, executable_path='C:/WebDrivers/chromedriver.exe')

try:
    print()
    print('Scraping Process is Started')

    url = 'https://www.nasdaq.com/market-activity/stocks/tsla/short-interest'

    wait = WebDriverWait(driver, 10)

    print()
    print('Loading Url Please Wait...')

    driver.get(url)
    driver.maximize_window()
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '.short-interest__table-body')))
    sleep(3)
    driver.execute_script("window.scrollBy(0, 900)", "")
    # driver.execute_script("window.stop();")

    print()
    print('Waiting for Content to Load Properly')

    sleep(3)

    src = driver.page_source
    soup = bs(src, 'lxml')

    list_1 = []
    list_2 = []
    list_3 = []
    list_4 = []

    print()
    print('Content is Loaded, Scraping Required Detail')
    print('Wait Please...')

    SETTLEMENT_DATE = soup.find_all('th', class_='short-interest__cell')
    for date in SETTLEMENT_DATE:
        text0 = date.text
        list_1.append(text0)

    SHORT_INTEREST = soup.find_all(
        'td', class_='short-interest__cell--interest')
    for interest in SHORT_INTEREST:
        text1 = interest.text
        list_2.append(text1)

    AVG_DAILY_SHARE_VOLUME = soup.find_all(
        'td', class_='short-interest__cell--avgDailyShareVolume')
    for avg in AVG_DAILY_SHARE_VOLUME:
        text2 = avg.text
        list_3.append(text2)

    DAYS_TO_COVER = soup.find_all(
        'td', class_='short-interest__cell--daysToCover')
    for days in DAYS_TO_COVER:
        text3 = days.text
        list_4.append(text3)

    print()
    print('Scraping Done, Saving the Data')

    data = {
        'SETTLEMENT_DATE': list_1,
        'SHORT_INTEREST': list_2,
        'AVG_DAILY_SHARE_VOLUME': list_3,
        'DAYS_TO_COVER': list_4
    }

    df = pd.DataFrame(data)
    df.to_csv('Tesla_Short-Interest.csv', index=False)

finally:
    driver.quit()
    print()
    print('All Done Successfully, You can Check Your Scraped Data')
