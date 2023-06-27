from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import undetected_chromedriver as uc

class Flight:
    def __init__(self, ep, pp, bp, fp, origin, destination):
        self.ep = ep
        self.pp = pp
        self.bp = bp
        self.fp = fp
        self.origin = origin
        self.destination = destination

def flightToStr(f):
    return str(f.ep) + " -- " + str(f.pp) + " -- " + str(f.bp) + " -- " + str(f.fp) + " -- Duration: " + str(f.duration)

options = uc.ChromeOptions()
options.add_argument('--headless')
driver = uc.Chrome(options=options)
driver.get("https://www.aa.com/booking/find-flights?maxAwardSegmentAllowed=4")


def searchInit(origin, destination, departure, arrival):
    redeemButton = driver.find_element(By.CSS_SELECTOR, ".customComponent:nth-child(1) > label:nth-child(3) > .control")
    redeemButton.click()

    if arrival == 0:
        oneWay = driver.find_element(By.CSS_SELECTOR, "#ui-id-4 > span:nth-child(2)")
        oneWay.click()

    originField = driver.find_element(By.ID, "segments0.origin")
    originField.send_keys("\b\b\b")
    originField.send_keys(origin)

    destField = driver.find_element(By.ID, "segments0.destination")
    destField.send_keys("\b\b\b")
    destField.send_keys(destination)

    departField = driver.find_element(By.ID, "segments0.travelDate")
    departField.send_keys(departure)

    if arrival != 0:
        returnField = driver.find_element(By.ID, "segments1.travelDate")
        returnField.send_keys(arrival)

    submit = driver.find_element(By.ID, "flightSearchSubmitBtn")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submit.click()
    WebDriverWait(driver, 35).until(EC.presence_of_element_located((By.ID, "flight-direction-text")))
    print(getCabinTypes())

    flights = []
    i = 0
    while i < int(getFlightCount()):
        flights.append(flightToStr(getFlight(i, getCabinTypes())))
        i += 1
    return flights


def searchCont(departure):
    newSearch = driver.find_element(By.ID, "new-search-desktop")
    newSearch.click()

    departField = driver.find_element(By.ID, "segments0.travelDate")
    departField.send_keys("\b\b\b\b\b\b\b\b\b\b")
    departField.send_keys(departure)
    submit = driver.find_element(By.ID, "flightSearchSubmitBtn")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submit.click()

    WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "flight-direction-text")))

    flights = []
    i = 0
    while i < int(getFlightCount()):
        flights.append(flightToStr(getFlight(i, getCabinTypes())))
        i += 1
    return flights


def getPrice(flightNum, product): #Pulls the miles and copay for the flight number and the class of service (product)
    try:
        miles = driver.find_element(By.XPATH, "//button[@id='flight" + str(flightNum) + "-product" + str(
            product) + "']/app-choose-flights-price-desktop/span").text
        copay = driver.find_element(By.XPATH, "//button[@id='flight" + str(flightNum) + "-product" + str(
            product) + "']/app-choose-flights-price-desktop/div").text
        return miles + " " + copay
    except NoSuchElementException:
        return "Not Available"


def getFlight(flightNum, cabins):
    fli = Flight
    i = 0
    while i < len(cabins):
        if cabins[i] == "Main Cabin":
            fli.ep = getPrice(flightNum, i)
        if cabins[i] == "Premium Economy":
            fli.pp = getPrice(flightNum, i)
        if cabins[i] == "Business":
            fli.bp = getPrice(flightNum, i)
        if cabins[i] == "First":
            fli.fp = getPrice(flightNum, i)
        i += 1

    if "Main Cabin" not in cabins:
        fli.ep = -1
    if "Premium Economy" not in cabins:
        fli.pp = -1
    if "Business" not in cabins:
        fli.bp = -1
    if "First" not in cabins:
        fli.fp = -1

    fli.origin = driver.find_element(By.CSS_SELECTOR, "#flight-details-" + str(flightNum) + " .origin > .city-code").text
    fli.destination = driver.find_element(By.CSS_SELECTOR, "#flight-details-" + str(flightNum) + " .destination > .city-code").text
    fli.duration = driver.find_element(By.CSS_SELECTOR, "#flight-details-" + str(flightNum) + " .duration").text

    return fli


def getFlightCount(): #To be only called when on the choose flights section
    num = ""
    result = driver.find_element(By.CLASS_NAME, "result-count").text
    for i in result:
        if i.isdigit():
            num = num + i
    return num


def getCabinTypes():
    try:
        coach = driver.find_element(By.CSS_SELECTOR, ".coach").text
    except NoSuchElementException:
        coach = 0

    try:
        premium = driver.find_element(By.CSS_SELECTOR, ".premium_economy").text
    except NoSuchElementException:
        premium = 0

    try:
        business = driver.find_element(By.CSS_SELECTOR, ".business").text
    except NoSuchElementException:
        business = 0

    try:
        first = driver.find_element(By.CSS_SELECTOR, ".first").text
    except NoSuchElementException:
        first = 0

    classes = [coach, premium, business, first]
    for i in classes:
        if i == 0:
            classes.remove(i)
    return classes


def convertDate(date): #Converts the date to the correct format
    year = date.year
    month = date.month
    day = date.day
    total = str(month) + "/" + str(day) + "/" + str(year)
    return total


start_date = datetime.date(2023, 8, 21)
end_date = datetime.date(2023, 8, 23)
delta = datetime.timedelta(days=1)
print(convertDate(start_date) + " --> " + str(searchInit("NYC", "DEL", convertDate(start_date), 0)))
while start_date < end_date:
    start_date += delta
    print(convertDate(start_date) + " --> " + str(searchCont(convertDate(start_date))))

driver.quit()