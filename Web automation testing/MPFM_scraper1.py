



from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("C:/Python27/chromedriver")
driver.get("http://www.python.org")

print driver.title
driver.save_screenshot('foo.png')
#print driver.page_source
elem = driver.application_cache
print elem








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