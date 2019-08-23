from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Chrome("C:/Python27/chromedriver")
driver.get("https://test.connectedservices.emerson.com/MPFM/ServiceManager")


log_in = driver.find_element_by_name('loginfmt')
log_in.send_keys('hiep.nguyen@emerson.com')
#driver.find_element_by_id('idSIButton9').click()


try:

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    driver.find_element_by_id('idSIButton9').click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'idSIButton9')))
    driver.find_element_by_id('idSIButton9').click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'cId-q6x5nZ5o')))
    driver.find_element_by_id('cId-q6x5nZ5o').click()

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.ID, 'aId-4')))
    driver.find_element_by_id('aId-4').click()



except:
    print "Everything happens for a reason"



'''

___________
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "idSIButton9"))
    )
    driver.find_element_by_id('idSIButton9').click()
except:
    print "Oh no 2"
    driver.quit()


try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "cId-q6x5nZ5o"))
    )
    driver.find_element_by_id('cId-q6x5nZ5o').click()
except:
    print "Oh no 3"
    driver.quit()
'''







'''
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome("C:/Python27/chromedriver")

driver.get("https://www.goodreads.com/user/sign_in")
driver.set_page_load_timeout(30)

email = driver.find_element_by_xpath('//*[@id="user_email"]')
print email
'''
'''
email = driver.find_element_by_xpath('//*[@id="user_email"]')
password = driver.find_element_by_xpath('//*[@id="user_password"]')
submit = driver.find_element_by_xpath('//*[@id="emailForm"]/form/fieldset/div[5]/input')

email.send_keys(username)
password.send_keys(pas)
submit.click()

'''