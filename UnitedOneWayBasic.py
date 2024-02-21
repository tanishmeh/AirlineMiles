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

    # WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "a-results-show-all"))) #This currently does not work, limited to 20 results
    # try:
    #     expand = driver.find_element(By.ID, "a-results-show-all").click()
    # except NoSuchElementException:
    #     expand = 0
    return getFlights()


def searchCont(departure):
    dep = driver.find_element(By.ID, "DepartDate")
    dep.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
    dep.send_keys(departure)
    driver.find_element(By.CSS_SELECTOR, ".edit-search-submit").click()

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".simplemodal-close")))
    closeMP = driver.find_element(By.CSS_SELECTOR, ".simplemodal-close")
    closeMP.click()
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lof-origin")))

    return getFlights()


def getFlights():
    flightList = {}

    flights = driver.find_element(By.ID, "flight-result-list-revised")
    elements = flights.find_elements(By.XPATH, ".//li[contains(@class, 'flight-block flight-block-fares')]")

    index = 0
    for i in elements:
        flightList["flight" + str(index)] = getFlightInfo(i.text)
        index += 1

    return flightList


def getFlightInfo(flight):
    flightInfo = {}
    temp = flight.split("\n")
    print(str(temp))
    flightInfo["Departure Time"] = temp[3]
    flightInfo["Departure Airport"] = temp[4]
    flightInfo["Arrival Time"] = temp[7]
    flightInfo["Arrival Airport"] = temp[8]
    flightInfo["Stops"] = temp[10]
    flightInfo["Duration"] = temp[11]

    flightInfo["Economy"] = ""
    flightInfo["Premium Economy"] = ""
    flightInfo["Business"] = ""

    index = 0
    for i in temp:
        if i == "miles":
            copay = temp[index + 1]
            miles = temp[index - 1]
            if temp[index + 2] == "fare for Economy":
                flightInfo["Economy"] = miles + " miles + " + copay[1:]
            elif temp[index + 2] == "fare for Premium Economy":
                flightInfo["Premium Economy"] = miles + " miles + " + copay[1:]
            elif (temp[index + 2] == "fare for Business/First (lowest)" or temp[index + 2] == "fare for Business (lowest)"):
                flightInfo["Business"] = miles + " miles + " + copay[1:]
            elif (temp[index + 2] == "fare for Business/First" or temp[index + 2] == "fare for Business"):
                if flightInfo["Business"] == "":
                    flightInfo["Business"] = miles + " miles + " + copay[1:]
        index += 1
    return flightInfo


# def getCabinTypes():
#     try:
#         coach = driver.find_element(By.XPATH, "//a[@id='column-MIN-ECONOMY-SURP-OR-DISP']/div").text
#     except NoSuchElementException:
#         coach = 0
#
#     try:
#         premium = driver.find_element(By.XPATH, "//a[@id='column-ECO-PREMIUM-DISP']/div").text
#     except NoSuchElementException:
#         premium = 0
#
#     try:
#         business = driver.find_element(By.XPATH, "//a[@id='column-MIN-BUSINESS-SURP-OR-DISP']/div").text
#     except NoSuchElementException:
#         business = 0
#
#     classes = [coach, premium, business]
#     for i in classes:
#         if i == 0:
#             classes.remove(i)
#     return classes

def convertDate(date):  # Converts the date to the correct format
    year = date.year
    month = date.month
    day = date.day
    total = str(month) + "/" + str(day) + "/" + str(year)
    return total


file = open("UAOneWay.json", "w")

results = {}

start_date = datetime.date(2024, 11, 15)
end_date = datetime.date(2024, 11, 16)
delta = datetime.timedelta(days=1)
results[convertDate(start_date)] = searchInit("EWR", "DEL", convertDate(start_date))
while start_date < end_date:
    start_date += delta
    results[convertDate(start_date)] = searchCont(convertDate(start_date))

file.write(json.dumps(results, indent=4))
file.close()

driver.quit()
