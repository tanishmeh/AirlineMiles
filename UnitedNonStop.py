import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import datetime
import undetected_chromedriver as uc
import json

# driver = uc.Chrome(headless=True)
driver = uc.Chrome()
driver.get("https://www.united.com/ual/en/us/flight-search/book-a-flight")

def searchInit(origin, destination, departure):
    miles = driver.find_element(By.CSS_SELECTOR, ".form-group:nth-child(2) > .radio:nth-child(6)")
    miles.click()

    oneWay = driver.find_element(By.XPATH, "//label[contains(.,'One-way')]")
    oneWay.click()

    ori = driver.find_element(By.ID, "Trips_0__Origin")
    ori.send_keys(origin)
    dest = driver.find_element(By.ID, "Trips_0__Destination")
    dest.send_keys(destination)
    dep = driver.find_element(By.ID, "Trips_0__DepartDate")
    dep.send_keys(departure)
    submit = driver.find_element(By.ID, "btn-search")
    submit.click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".simplemodal-close")))
    closeMP = driver.find_element(By.CSS_SELECTOR, ".simplemodal-close")
    closeMP.click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lof-origin")))
    print(getCabinTypes())

    # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "a-results-show-all"))) #This currently does not work, limited to 20 results
    # try:
    #     expand = driver.find_element(By.ID, "a-results-show-all").click()
    # except NoSuchElementException:
    #     expand = 0

    print(getFlightHashes())
    print(getFlight("ECO-PREMIUM-DISP_", "359-82-UA"))
    time.sleep(25)

def getFlightHashes():
    hashes = []

    flights = driver.find_element(By.ID, "flight-result-list-revised")
    elements = flights.find_elements(By.XPATH, ".//li[contains(@class, 'flight-block flight-block-fares')]")

    for i in elements:
        hashes.append(i.get_attribute("data-flight-hash"))

    return hashes

def getFlight(cabinCode, hash):
    flight = {}
    econ = driver.find_element(By.XPATH, "//div[@id='sr_product_" + cabinCode + hash + "']/div/div").text
    econCo = driver.find_element(By.XPATH, "//div[@id='sr_product_" + cabinCode + hash + "']/div/div[2]").text
    if (econ == "Saver Award"):
        econ = driver.find_element(By.XPATH, "//div[@id='sr_product_" + cabinCode + hash + "']/div/div[2]").text
        econCo = driver.find_element(By.XPATH, "//div[@id='sr_product_" + cabinCode + hash + "']/div/div[3]").text

    return econ + econCo
# def getPrices(hashes):


def getCabinTypes():
    try:
        coach = driver.find_element(By.XPATH, "//a[@id='column-MIN-ECONOMY-SURP-OR-DISP']/div").text
    except NoSuchElementException:
        coach = 0

    try:
        premium = driver.find_element(By.XPATH, "//a[@id='column-ECO-PREMIUM-DISP']/div").text
    except NoSuchElementException:
        premium = 0

    try:
        business = driver.find_element(By.XPATH, "//a[@id='column-MIN-BUSINESS-SURP-OR-DISP']/div").text
    except NoSuchElementException:
        business = 0

    classes = [coach, premium, business]
    for i in classes:
        if i == 0:
            classes.remove(i)
    return classes

searchInit("NYC", "DEL", "12/25/2023")