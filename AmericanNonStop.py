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
driver.get("https://www.aa.com/booking/find-flights?maxAwardSegmentAllowed=4")


def searchInit(origin, destination, departure, arrival): #Initiates the search from the first screen
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

    # if arrival != 0:
    #     returnField = driver.find_element(By.ID, "segments1.travelDate")
    #     returnField.send_keys(arrival)

    submit = driver.find_element(By.ID, "flightSearchSubmitBtn")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submit.click()
    print("SearchInit completed!")
    WebDriverWait(driver, 45).until(EC.presence_of_element_located((By.ID, "flight-direction-text")))
    print(getCabinTypes())

    flights = {}
    i = 0
    while i < int(getFlightCount()):
        flights["flight" + str(i)] = getFlight(i, getCabinTypes())
        i += 1
    return flights #Returns a dictionary of all flights for the specified day


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

    flights = {}
    i = 0
    while i < int(getFlightCount()):
        flights["flight" + str(i)] = getFlight(i, getCabinTypes())
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
    fli = {}
    i = 0
    #
    # if "Main Cabin" not in cabins:
    #     fli["Economy"] = -1
    # if "Premium Economy" not in cabins:
    #     fli["Premium Economy"] = -1
    # if "Business" not in cabins:
    #     fli["Business"] = -1
    # if "First" not in cabins:
    #     fli["First"] = -1

    while i < len(cabins):
        if cabins[i] == "Main Cabin":
            fli["Economy"] = getPrice(flightNum, i)
        if cabins[i] == "Premium Economy":
            fli["Premium Economy"] = getPrice(flightNum, i)
        if cabins[i] == "Business":
            fli["Business"] = getPrice(flightNum, i)
        if cabins[i] == "First":
            fli["First"] = getPrice(flightNum, i)
        i += 1



    # fli["Origin"] = driver.find_element(By.CSS_SELECTOR, "#flight-details-" + str(flightNum) + " .origin > .city-code").text
    # fli["Destination"] = driver.find_element(By.CSS_SELECTOR, "#flight-details-" + str(flightNum) + " .destination > .city-code").text
    fli["Duration"] = driver.find_element(By.CSS_SELECTOR, "#flight-details-" + str(flightNum) + " .duration").text

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

file = open("AANonstop.json", "w")
results = {} #This will be the final dictionary containing the dates and the flights for that day

start_date = datetime.date(2023, 12, 9)
end_date = datetime.date(2023, 12, 9)
delta = datetime.timedelta(days=1)
results[convertDate(start_date)] = searchInit("JFK", "DEL", convertDate(start_date), 0)
while start_date < end_date:
    start_date += delta
    results[convertDate(start_date)] = searchCont(convertDate(start_date))

file.write(json.dumps(results, indent=4))
file.close()

driver.quit()