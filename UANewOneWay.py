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
driver.get("https://www.united.com/en/us/book-flight/united-one-way")

def searchInit(origin, destination, departure):
    miles = driver.find_element(By.XPATH, "//label[contains(.,'Miles')]")
    miles.click()

    ori = driver.find_element(By.ID, "originInput5")
    ori.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
    ori.send_keys(origin)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button/div").click()

    des = driver.find_element(By.ID, "destinationInput6")
    des.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
    des.send_keys(destination)
    time.sleep(1)
    driver.find_element(By.XPATH, "//button/div").click()

    dep = driver.find_element(By.ID, "DepartDate")
    dep.send_keys("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b")
    dep.send_keys(departure)
    dep.send_keys("\t")

    time.sleep(1)

    find = driver.find_element(By.XPATH, "//span[contains(.,'Find flights')]")
    find.click()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "closeBtn")))
    time.sleep(3)
    close = driver.find_element(By.ID, "closeBtn")
    close.click()

    time.sleep(10)

def searchContinue(origin, destination, departure):



searchInit("EWR", "DEL", "03/20/24")

