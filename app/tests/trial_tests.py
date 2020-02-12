import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

dir = os.path.dirname(os.path.abspath(__file__))
chrome_driver_path = dir + "\chromedriver.exe"

driver = webdriver.Chrome(executable_path = chrome_driver_path)
driver.implicitly_wait(10)
driver.maximize_window()


driver.get("http://localhost:5000/auth/login")

username_field = driver.find_element_by_id("username")
username_field.send_keys("vignesh")

password_field = driver.find_element_by_id("password")
password_field.send_keys("Vignesh123")

submit_button = driver.find_element_by_id("submit")
submit_button.click()


