# =============================================================================
# 
# RUN THIS CODE USING THE FOLLOWING LINE ON CMD
# scrapy crawl articlelinks -o links.csv
# 
# Approximate crawling time is 8-20 seconds.
# =============================================================================
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import getpass
import scrapy

# =============================================================================
# ENVIRONMENTAL SETTINGS
# Chrome Driver used here. Please change the driver path with yours.
# =============================================================================
url = 'https://www.sciencedirect.com/'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome('C:\\Users\\ozgrp\\Desktop\\UW\\Webscraping\\7\\chromedriver_win32\\chromedriver.exe',options = chrome_options)
driver.get(url)

# Continuous search type checking on the console until the user provides the answer in the given form.
search_type = input('Would you like to log in or continue your query on guest mode? Note: \n Some content may not be available due to account specific restrictions. \n (Y/N)')
while True:   
    if not(search_type == "Y" or search_type == "N"):
        search_type = input("Please provide your answer as 'Y' for yes or 'N' for no.")
    else:
        break

# If user wants to perform the search in logged in mode then following code will perform the log in.
if search_type=="Y":     
    time.sleep(2)
    driver.find_element_by_id('gh-signin-btn').click()
    time.sleep(2)
    username = driver.find_element_by_id('reg-userid')
    my_email = input('Please provide your email:')
    username.send_keys(my_email)
    time.sleep(2)
    password = driver.find_element_by_id('reg-password')
    my_pass = getpass.getpass('Please provide your password:')
    password.send_keys(my_pass)
    driver.find_element_by_class_name('login-submit').click()
    time.sleep(2)

# In both modes of search the following block is executed. 
search = driver.find_element_by_id('qs-searchbox-input')
my_key = input('Please provide your search keyword:')
search.send_keys(my_key)
time.sleep(2)
search.send_keys(Keys.RETURN)
time.sleep(2)
driver.current_url

# If user prefers to perform the search without logging in then a modal will be displayed that blocks the search. It should be closed automatically.
if search_type=="N":
    driver.find_element_by_class_name("modal-close-button").click()

# Following 3 lines clicks to load 100 articles in one page.   
time.sleep(2)
driver.find_element_by_xpath("//span[text()='100']").click()
lasturl = driver.current_url


# Scrapy item description that is to be yielded and exported on csv.
class Link(scrapy.Item):
    link = scrapy.Field()

# Corresponding spider object description to gather 100 links of the search.
class ArticleLinks(scrapy.Spider):
    name = 'articlelinks'
    allowed_domains = ['www.sciencedirect.com']
    start_urls = [lasturl]

    # Headers attribute allows our scraper to pretend it is a real user.
    def start_requests(self):
        headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
        for url in self.start_urls:
            yield scrapy.Request(url, headers=headers, callback=self.parse)
   
    # In this callback function we gather all of the links and yield.
    def parse(self, response):
        selection = response.xpath("(//h2//a)//@href")
        for s in selection:
            l = Link()
            l['link'] = 'https://www.sciencedirect.com/' + s.get()
            yield l