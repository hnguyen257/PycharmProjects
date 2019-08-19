import csv
import time
from bs4 import BeautifulSoup, ResultSet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


count = 0
tracking = 3301 # set to current book_id, and the scraper will continue from there
with open('books.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    url = 'https://www.amazon.com/s?k='
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)

    for row in csv_reader:
        if count < tracking:
            count += 1
            continue
        isbn = str(row['isbn'])
        while(len(isbn) < 10):
            isbn = '0' + isbn
        print('The isbn is: ' + isbn)

        url2 = url + isbn + '&ref=nb_sb_noss'

        print url2
        driver.get(url2)
        time.sleep(2)
        page = driver.page_source

        soup = BeautifulSoup(page, 'html.parser')

        links = soup.find('a', attrs={'class': 'a-link-normal a-text-normal'})
        if links is None:
            #print soup
            driver.get(url2)
            time.sleep(10)
            page = driver.page_source
            soup = BeautifulSoup(page, 'html.parser')
            links = soup.find('a', attrs={'class': 'a-link-normal a-text-normal'})
            if links is None:
                tracking += 1
                continue

        a = str(links.get('href'))

        url4 = 'https://www.amazon.com' + a

        print url4

        driver.get(url4)
        time.sleep(1)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

        #print soup


        avgRating = soup.find('span', attrs={'class': 'a-icon-alt'})
        if avgRating is None:
            #print soup
            continue
        avgRating = str(avgRating.text.strip().encode("utf-8"))
        avgRating = avgRating.split()[0]


        reviewAuthor = soup.findAll('span', attrs={'class': 'a-profile-name'})
        review = soup.findAll('div', attrs={'class': 'a-expander-content reviewText review-text-content '
                                                     'a-expander-partial-collapse-content'})

        book_id = row['book_id']
        isbnList = isbn
        titles = row['title']
        authorList = row['authors']
        print(avgRating)
        avgRatingList = avgRating



        if(len(reviewAuthor) > 0):
            comAuthor1 = reviewAuthor[0].text.strip().encode("utf-8")
            comContent1 = review[0].text.strip().encode("utf-8")
            if (len(reviewAuthor) > 1):
                comAuthor2 = reviewAuthor[1].text.strip().encode("utf-8")
                comContent2 = review[1].text.strip().encode("utf-8")
                if (len(reviewAuthor) > 2):
                    comAuthor3 = reviewAuthor[2].text.strip().encode("utf-8")
                    comContent3 = review[2].text.strip().encode("utf-8")

        if(len(reviewAuthor) < 3):
            comAuthor3 = 'none'
            comContent3 = 'none'
            if (len(reviewAuthor) < 2):
                comAuthor2 = 'none'
                comContent2 = 'none'
                if (len(reviewAuthor) < 1):
                    comAuthor1 = 'none'
                    comContent1 = 'none'

        with open('AmazonResult33.csv', mode='ab') as testing_file:
            testing_writer = csv.writer(testing_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            # testing_writer.writerow(['book_id', 'titles', 'isbn', 'author', 'review source', 'average rating', 'review author', 'review content'])
            testing_writer.writerow(
                [book_id, titles, isbnList, authorList, 'Amazon', avgRatingList, comAuthor1, comContent1])
            testing_writer.writerow(
                [book_id, titles, isbnList, authorList, 'Amazon', avgRatingList, comAuthor2, comContent2])
            testing_writer.writerow(
                [book_id, titles, isbnList, authorList, 'Amazon', avgRatingList, comAuthor3, comContent3])
        testing_file.close()