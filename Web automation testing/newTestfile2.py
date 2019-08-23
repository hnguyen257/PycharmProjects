from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome("C:/Python27/chromedriver")
driver.get("https://test.connectedservices.emerson.com/MPFM/ServiceManager")

elem = driver.find_element_by_name('loginfmt')
elem.send_keys('hiep.nguyen@emerson.com')

try:
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    driver.find_element_by_id('idSIButton9').click()
except:
    pass

try:
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    driver.find_element_by_id('idSIButton9').click()
except:
    pass

try:
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'cId-q6x5nZ5o')))
    driver.find_element_by_id('cId-q6x5nZ5o').click()
except:
    pass

try:
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'aId-4')))
    driver.find_element_by_id('aId-4').click()
except:
    pass
