from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Flight:
    def __init__(self, ep, pp, bp, fp, dep, arr, stops, duration):
        self.ep = ep
        self.pp = pp
        self.bp = bp
        self.fp = fp
        self.dep = dep
        self.arr = arr
        self.stops = stops
        self.duration = duration

PATH = "/Users/tanishmehta/Desktop/Projects/AirlineMiles/chromedriver"
driver = webdriver.Chrome()
driver.get("https://www.aa.com/booking/find-flights?maxAwardSegmentAllowed=4")
# print(driver.title)

# driver.find_element(By.CSS_SELECTOR, ".mat-end-date").click()
# driver.find_element(By.CSS_SELECTOR, ".cdk-overlay-backdrop").click()

def searchInit(origin, destination, departure, arrival):
    redeemButton = driver.find_element(By.CSS_SELECTOR, ".customComponent:nth-child(1) > label:nth-child(3) > .control")
    redeemButton.click()

    originField = driver.find_element(By.ID, "segments0.origin")
    originField.send_keys("\b\b\b")
    originField.send_keys(origin)

    destField = driver.find_element(By.ID, "segments0.destination")
    destField.send_keys("\b\b\b")
    destField.send_keys(destination)

    departField = driver.find_element(By.ID, "segments0.travelDate")
    departField.send_keys(departure)

    returnField = driver.find_element(By.ID, "segments1.travelDate")
    returnField.send_keys(arrival)

    submit = driver.find_element(By.ID, "flightSearchSubmitBtn")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    submit.click()
    time.sleep(32)

    for i in range(0, 3):
        try:
            CSSSel = "#flight-details-" + str(i)
            dep = driver.find_element(By.CSS_SELECTOR, CSSSel + " .origin > .flt-times").text
            print(dep)
        except RuntimeError:
            break

        for k in range(0, 3):
            try:
                XPAT = "//button[@id='flight" + str(i) + "-product" + str(k) + "']/app-choose-flights-price-desktop"
                miles = driver.find_element(By.XPATH, XPAT + "/span").text
                print(miles)
                copay = driver.find_element(By.XPATH, XPAT + "/div").text
                print(copay)
            except RuntimeError:
                break




# tem = driver.find_element(By.ID, "flight0-product0")
# miles = driver.find_element(By.XPATH, "//button[@id='flight0-product0']/app-choose-flights-price-desktop/span").text
# copay = driver.find_element(By.XPATH, "//button[@id='flight0-product0']/app-choose-flights-price-desktop/div").text
# print(miles)
# print(copay)

searchInit("NYC", "DEL", "12/30/2023", "01/07/2024")

# dep = driver.find_element(By.CSS_SELECTOR, "#flight-details-0 .origin > .flt-times").text
# print(dep)

# for i in range(0, 50):
#     for k in range(0, 3):
#         pos = "flight" + str(i) + "-product" + str(k)
#         tem = driver.find_element(By.ID, pos)
#         print(tem)

# def changeDate(startDate, endDate):
#     date = driver.find_element(By.CSS_SELECTOR, ".mat-end-date")
#     date.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b") #Erases previous contents for both the start and end dates
#     sdate = driver.find_element(By.CSS_SELECTOR, ".mat-start-date") #Start Date
#     sdate.send_keys(startDate)
#     edate = driver.find_element(By.CSS_SELECTOR, ".mat-end-date") #End Date
#     edate.send_keys(endDate)
#
# def getFare(startDate, endDate):
#     changeDate(startDate, endDate)
#     driver.find_element(By.CSS_SELECTOR, ".search-button .mat-icon").click()
#
#     time.sleep(40)
#     driver.find_element((By.NAME, "css=.mat-header-row > .cdk-column-carrier_AA")).click()
#
#
#
# getFare("11/22/2023", "11/27/2023")



# elem = driver.find_element(By.ID, "mat-chip-list-input-0")
# elem.clear()
# elem.send_keys("nyc")
# elem.send_keys(Keys.RETURN)
# elem2 = driver.find_element(By.ID, "mat-chip-list-input-1")
# elem2.send_keys("delhi")
#
# time.sleep(3)
# elem2.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
