from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import datetime
import undetected_chromedriver as uc
import json


class Flight:
    def __init__(self, origin, destination, departTime, arriveTime, travelTime, eco = None, pre = None, bus = None, fir = None):
        self.origin = origin
        self.destination = destination
        self.departTime = departTime
        self.arriveTime = arriveTime
        self.travelTime = travelTime
        self.eco = eco
        self.pre = pre
        self.bus = bus
        self.fir = fir

    def to_dict(self):
        return {
            "origin": self.origin,
            "destination": self.destination,
            "departTime": self.departTime,
            "arriveTime": self.arriveTime,
            "travelTime": self.travelTime,
            "Economy": self.eco,
            "Premium": self.pre,
            "Business": self.bus,
            "First": self.fir
        }

# driver = uc.Chrome(headless=True)
driver = uc.Chrome()
driver.get("https://www.aa.com/booking/find-flights?maxAwardSegmentAllowed=4")


def searchInit(origin, destination, departure, arrival, nearbyAirports):  # Initiates the search from the first screen
    redeemButton = driver.find_element(By.CSS_SELECTOR, ".customComponent:nth-child(1) > label:nth-child(3) > .control")
    redeemButton.click()

    if arrival == 0:
        oneWay = driver.find_element(By.CSS_SELECTOR, "#ui-id-4 > span:nth-child(2)")
        oneWay.click()

    # if arrival != 0:
    #     returnField = driver.find_element(By.ID, "segments1.travelDate")
    #     returnField.send_keys(arrival)

    # Adds Nearby Airport Functionality for American Airlines
    if nearbyAirports:
        nearbyButton1 = driver.find_element(By.CSS_SELECTOR, ".depart .control")
        nearbyButton2 = driver.find_element(By.CSS_SELECTOR, ".span-phone6:nth-child(2) .control")
        nearbyButton1.click()
        nearbyButton2.click()

    originField = driver.find_element(By.ID, "segments0.origin")
    originField.send_keys("\b\b\b")
    originField.send_keys(origin)

    destField = driver.find_element(By.ID, "segments0.destination")
    destField.send_keys("\b\b\b")
    destField.send_keys(destination)

    departField = driver.find_element(By.ID, "segments0.travelDate")
    departField.send_keys(departure)

    submit = driver.find_element(By.ID, "flightSearchSubmitBtn")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submit.click()
    print("SearchInit completed!")
    WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "flight-direction-text")))
    print(getCabinTypes())

    return getAllFlights()


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

    return getAllFlights()


# Gets all the flights for the specific day it is on
def getAllFlights():
    flights = {}
    i = 0
    cabins = getCabinTypes()
    while i < int(getFlightCount()):
        flights["flight" + str(i)] = getFlight(i, cabins)
        i += 1
    return flights  # Returns a dictionary of all flights for the specified day


# Pulls the miles and copay for the flight number and the class of service (product)
def getPrice(flightNum, product):
    try:
        miles = driver.find_element(By.XPATH, "//button[@id='flight" + str(flightNum) + "-product" + str(
            product) + "']/app-choose-flights-price-desktop/span").text
        copay = driver.find_element(By.XPATH, "//button[@id='flight" + str(flightNum) + "-product" + str(
            product) + "']/app-choose-flights-price-desktop/div").text
        return miles + " " + copay
    except NoSuchElementException:
        return "Not Available"


def getFlight(flightNum, cabins):
    element = driver.find_element(By.CSS_SELECTOR, "#flight-details-" + str(flightNum))

    duration = element.find_element(By.CSS_SELECTOR, " .duration").text
    origin = element.find_element(By.CSS_SELECTOR, " .origin > .city-code").text
    destination = element.find_element(By.CSS_SELECTOR, " .destination > .city-code").text
    departure = element.find_element(By.CSS_SELECTOR, " .origin > .flt-times").text
    arrival = element.find_element(By.CSS_SELECTOR, " .destination > .flt-times").text

    flight = Flight(origin, destination, departure, arrival, duration)

    for i in range(len(cabins)):
        if cabins[i] == "Main Cabin":
            flight.eco = getPrice(flightNum, i)
        if cabins[i] == "Premium Economy":
            flight.pre = getPrice(flightNum, i)
        if cabins[i] == "Business":
            flight.bus = getPrice(flightNum, i)
        if cabins[i] == "First":
            flight.fir = getPrice(flightNum, i)

    return flight


# To be only called when on the choose flights section
def getFlightCount():
    num = ""
    result = driver.find_element(By.CLASS_NAME, "result-count").text
    for i in result: #extracts the integer from the string
        if i.isdigit():
            num = num + i
    return num


def getCabinTypes():
    classes = ["Main Cabin", "Premium Economy", "Business", "First"]
    try:
        coach = driver.find_element(By.CSS_SELECTOR, ".coach").text
    except NoSuchElementException:
        classes.remove("Main Cabin")

    try:
        premium = driver.find_element(By.CSS_SELECTOR, ".premium_economy").text
    except NoSuchElementException:
        classes.remove("Premium Economy")

    try:
        business = driver.find_element(By.CSS_SELECTOR, ".business").text
    except NoSuchElementException:
        classes.remove("Business")

    try:
        first = driver.find_element(By.CSS_SELECTOR, ".first").text
    except NoSuchElementException:
        classes.remove("First")

    return classes


def convertDate(date):  # Converts the date to the correct format
    year = date.year
    month = date.month
    day = date.day
    total = str(month) + "/" + str(day) + "/" + str(year)
    return total


file = open("AANonstop.json", "w")
results = {}  # This will be the final dictionary containing the dates and the flights for that day

date = datetime.date(2024, 12, 9)
end_date = datetime.date(2024, 12, 9)
delta = datetime.timedelta(days=1)
results[convertDate(date)] = searchInit("JFK", "DEL", convertDate(date), 0, True)
while date < end_date:
    date += delta
    results[convertDate(date)] = searchCont(convertDate(date))

serializable_results = {}
for date, flights in results.items():
    serializable_flights = {}
    for flight_key, flight_obj in flights.items():
        serializable_flights[flight_key] = flight_obj.to_dict()  # Convert Flight object to a dictionary
    serializable_results[date] = serializable_flights

jsonResult = json.dumps(serializable_results, indent=4)

file.write(jsonResult)
file.close()

driver.quit()