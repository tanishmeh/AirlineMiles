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
driver.get("https://www.aircanada.com/ca/en/aco/home.html")

def searchInit(origin, destination, departure):
    miles = driver.find_element(By.ID, "bkmgFlights_searchTypeToggle")
    miles.click()

    oneWay = driver.find_element(By.ID, "bkmgFlights_tripTypeSelector_O")
    oneWay.click()

    ori = driver.find_element(By.ID, "bkmgFlights_origin_trip_1")
    ori.send_keys(origin)

    des = driver.find_element(By.ID, "bkmgFlights_destination_trip_1")
    des.send_keys(destination)

    date = driver.find_element(By.ID, "bkmgFlights_travelDates_1")
    date.send_keys(departure)

    time.sleep(50)

def main():
    searchInit("NYC", "DEL", "12/12/23")