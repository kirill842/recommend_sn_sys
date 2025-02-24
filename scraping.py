from sys import executable

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
    driver = webdriver.Chrome(chrome_options)

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

    for a in soup.findAll('a', attrs={'class': '_root_aroml_2 _label_aroml_17 x-product-card__pic x-product-card__pic-catalog x-product-card__pic x-product-card__pic-catalog'}):
        product_url = 'lamoda.ru' + a['href']
        product_urls.append(product_url)
        image_url = a.find('img')['src']
        image_urls.append(image_url)

    print(product_urls)

    for div in soup.findAll('div', attrs={'class': 'x-product-card-description x-product-card-description__faded'}):
        price = div.find('span', attrs={'class': "_price_163e7_8 x-product-card-description__price-new x-product-card-description__price-WEB8507_price_bold"})
        if price:
            prices.append(price.text.strip(' ₽').replace(" ", ""))
        else:
            prices.append(-1)
        brand_name = div.find('div', attrs={'class': 'x-product-card-description__brand-name _brandName_163e7_6 x-product-card-description__brand-name_faded'})
        if brand_name:
            brand_names.append(brand_name.text)
        else:
            brand_names.append('NO DATA')
        product_name = div.find('div', attrs={'class': 'x-product-card-description__product-name _productName_163e7_7 x-product-card-description__product-name_faded'})
        if product_name:
            product_names.append(product_name.text)
        else:
            product_names.append('NO DATA')

    return image_urls, product_urls, brand_names, product_names, prices
