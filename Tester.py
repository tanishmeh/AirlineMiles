from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

origin = "EWR"
destination = "DEL"
depart_date = "12/30/2024"

driver = webdriver.Chrome()
driver.get("https://www.united.com/en/us/book-flight/united-one-way")

# Wait for page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "bookFlightOriginInput")))

# Enter origin
origin_field = driver.find_element(By.NAME, "bookFlightOriginInput")
origin_field.clear()
origin_field.send_keys(origin)

# Enter destination
dest_field = driver.find_element(By.NAME, "bookFlightDestinationInput")
dest_field.clear()
dest_field.send_keys(destination)

# Select depart date
depart_date_field = driver.find_element(By.ID, "DepartDate")
depart_date_field.clear()
depart_date_field.send_keys(depart_date)

# Select one-way trip
oneway_button = driver.find_element(By.ID, "oneway")
oneway_button.click()

# Select miles
miles_button = driver.find_element(By.ID, "award")
miles_button.click()

# Submit form
submit_btn = driver.find_element(By.XPATH, "//button[contains(@data-testid,'submit-button')]")
submit_btn.click()

# Wait for results to load
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.flight-module.segment.offer-listing")))

# Get flights
flights = driver.find_elements(By.CSS_SELECTOR, "li.flight-module.segment.offer-listing")

# Extract flight data
results = {}
results[depart_date] = {}

for i, flight in enumerate(flights):
    flight_details = {}

    origin = flight.find_element(By.CSS_SELECTOR, "span.airport-name").text
    dest = flight.find_element(By.CSS_SELECTOR, "span.airport-name2").text

    depart_time = flight.find_element(By.CSS_SELECTOR, "span.departure-time").text
    arrive_time = flight.find_element(By.CSS_SELECTOR, "span.arrival-time").text

    travel_time = flight.find_element(By.CSS_SELECTOR, "span.flight-duration").text

    economy = flight.find_element(By.CSS_SELECTOR, "span.price-text").text

    flight_details["origin"] = origin
    flight_details["destination"] = dest
    flight_details["departTime"] = depart_time
    flight_details["arriveTime"] = arrive_time
    flight_details["travelTime"] = travel_time
    flight_details["Economy"] = economy

    flight_id = "flight" + str(i)
    results[depart_date][flight_id] = flight_details

print(json.dumps(results, indent=4))

driver.quit()
