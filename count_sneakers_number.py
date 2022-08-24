from bs4 import BeautifulSoup
from selenium import webdriver
import pickle

import config
import web_crawler
# import getpass
# import os
#
# USER_NAME = getpass.getuser()
#
#
# def add_to_startup(file_path=""):
#     if file_path == "":
#         file_path = os.path.dirname(os.path.realpath(__file__))
#     bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
#     with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
#         bat_file.write(r'start "" "%s"' % file_path)
#
#
# add_to_startup()

driver = webdriver.Chrome(executable_path=config.chrome_driver_path)
driver.get('https://www.lamoda.ru/c/2981/shoes-krossovk-kedy-muzhskie/')

content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

i = 1
new_sneakers_amount = 0
for title in soup.findAll('div', attrs={'class': 'aBcLsXmgsBBuX2JnHhbPt'}):
    if i == 7:
        new_sneakers_amount = int(title.find('span').text)
        print('Current sneakers amount on website:', new_sneakers_amount)
    i += 1

# Open the file in binary mode
with open('last_sneakers_amount.pkl', 'rb') as file:
    # Call load method to deserialze
    last_sneakers_amount = pickle.load(file)

    print('Last saved sneakers amount:', last_sneakers_amount)

if last_sneakers_amount == new_sneakers_amount:
    print("Site wasn't changed, won't scrape")
else:
    print("Site was changed, scraping new sneakers and saving new amount value")
    # Open a file and use dump()
    with open('last_sneakers_amount.pkl', 'wb') as file:
        # A new file will be created
        pickle.dump(new_sneakers_amount, file)

    # running crawler with default config settings
    web_crawler.scrap_site_and_update_database()
