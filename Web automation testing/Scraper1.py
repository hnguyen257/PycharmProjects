from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#import pandas as pd

driver = webdriver.Chrome()

def sign_in(username, pas):
    driver.get("https://www.goodreads.com/user/sign_in")
    driver.set_page_load_timeout(30)

    email = driver.find_element_by_xpath('//*[@id="user_email"]')
    password = driver.find_element_by_xpath('//*[@id="user_password"]')
    submit = driver.find_element_by_xpath('//*[@id="emailForm"]/form/fieldset/div[5]/input')

    email.send_keys(username)
    password.send_keys(pas)
    submit.click()

def clean(s):
    return s.encode("utf-8")

df_completed = pd.read_csv("./bookdata.csv", header = 0 , index_col= 0)
books_completed = df_completed['title'].tolist()

df = pd.read_csv("./books.csv", header = 0)

df = df.drop(df[df.title.isin(books_completed)].index, axis=0)
df = df.drop(columns=['book_id','authors','goodreads_book_id','best_book_id','work_id','books_count','original_title','language_code','small_image_url'], axis=1)

books = df['title'].tolist()

#print("books:",books)

sign_in('wesclock777@gmail.com', 'apples')

descriptions = []
buy = []
det = []
authors = []

count = 0

for book in books:
    if count == 1000:
        break
    if book in books_completed:
        continue

    book = book.split("(")[0].decode('utf-8')
    try:
        driver.get('https://www.goodreads.com/')
    except:
        driver.execute_script("window.stop();")
    search = driver.find_element_by_xpath("/html/body/div[3]/div/header/div[1]/div/div[2]/form/input")
    search.click()
    search.send_keys(book)
    try:
        search.send_keys(Keys.RETURN)
    except:
        pass
    try:
        try:
            first_res = driver.find_element_by_xpath( \
                "/html/body/div[2]/div[3]/div[1]/div[2]/div[2]/table/tbody/tr[1]/td[2]/a")
            first_res.click()
        except:
            driver.execute_script("window.stop();")

        try:
            more = driver.find_element_by_xpath('//*[@id="description"]/a')
            more.click()
        except:
            driver.execute_script("window.stop();")
            pass

        try:
            more_details = driver.find_element_by_xpath('//*[@id="bookDataBoxShow"]')
            more_details.click()
        except:
            pass

        auth = driver.find_element_by_xpath('//*[@id="bookAuthors"]/span[2]/div[1]/a/span')

        try:
            des = driver.find_element_by_xpath('//*[@id="description"]')
            descriptions.append(clean(des.get_attribute("innerText")))
        except:
            descriptions.append("")

        pgs = driver.find_element_by_xpath('//*[@id="details"]/div[1]')
        buybtn = driver.find_element_by_xpath('//*[@id="buyButton"]')

        buy.append(clean(buybtn.get_attribute('href')))
        det.append(clean(pgs.get_attribute('innerText')))
        authors.append(clean(auth.get_attribute('innerHTML')))
        count+=1
        print(book, count)
    except Exception, err:
        print(err)
        print("Going to Save")
        break

df = df.head(count)

driver.quit()
df['author'] = authors
df['details'] = det
df['description'] = descriptions
df['purchase'] = buy

df.to_csv('./bookdata.csv', encoding='utf-8', mode='a', header=False)

print("saved")

print len(df)