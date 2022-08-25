from bs4 import BeautifulSoup
from selenium import webdriver
import time
import config
from selenium.webdriver.chrome.options import Options


def get_data_from_url(url_to_scrap: str, page_number: int, scroll_pause_time=config.SCROLL_PAUSE_TIME):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path=config.CHROME_DRIVER_PATH, chrome_options=chrome_options)

    if '?' in url_to_scrap:
        url = url_to_scrap + '&page=' + str(page_number)
    else:
        url = url_to_scrap + '/?page=' + str(page_number)

    driver.get(url)

    y = 800
    for step in range(0, 13):
        # Scroll down
        driver.execute_script("window.scrollTo(0, " + str(y) + ");")

        # Wait to load page
        time.sleep(scroll_pause_time)

        y = y + 800

    time.sleep(0.2)

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    product_urls = []
    image_urls = []
    prices = []
    brand_names = []
    product_names = []

    for a in soup.findAll('a', attrs={'class': 'wCjUeog4KtWw64IplV1e6 _3dch7Ytt3ivpea7TIsKVjb x-product-card__pic x-product-card__pic-catalog'}):
        product_url = 'lamoda.ru' + a['href']
        product_urls.append(product_url)
        image_url = a.find('img')['src']
        image_urls.append(image_url)

    for div in soup.findAll('div', attrs={'class': 'x-product-card-description'}):
        price = div.find('span').text
        prices.append(price.strip(' ₽').replace(" ", ""))
        brand_name = div.find('div', attrs={'class': 'x-product-card-description__brand-name'}).text
        brand_names.append(brand_name)
        product_name = div.find('div', attrs={'class': 'x-product-card-description__product-name'}).text
        product_names.append(product_name)

    return image_urls, product_urls, brand_names, product_names, prices
