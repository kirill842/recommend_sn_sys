from scraping import get_data_from_url
from postgres_connection import append_scraped_data_to_postgres_database
import argparse
import config


def scrap_site_and_update_database(scrape_new=False):
    parser = argparse.ArgumentParser(description='hello!')
    parser.add_argument('--db_connect_link', type=str,
                        default=config.db_connect_link,
                        help='Connection link to database. Example: postgresql://login:password@ip:port/db_name')
    parser.add_argument('--url_to_scrap', type=str, default=config.url_to_scrap,
                        help='Url to scrap. Example: https://www.lamoda.ru/c/5971/shoes-muzhkrossovki')
    parser.add_argument('--num_of_pages_to_scrap', type=int, default=config.num_of_pages_to_scrap,
                        help='Number of pages to scrap images everytime web crawler script is executed')
    parser.add_argument('--scroll_pause_time', type=float, default=config.scroll_pause_time,
                        help='Pause during scrolling. Bigger values guarantee loading all dynamic content.' +
                        '0.2sec is enough for https://www.lamoda.ru')

    args = parser.parse_args()

    url_to_scrap = args.url_to_scrap
    if scrape_new:
        url_to_scrap += '/?sort=new'

    errors = 0
    for page_number in range(1, config.num_of_pages_to_scrap + 1):
        # get page data from scraper
        image_urls, product_urls, brand_names, product_names, prices = \
            get_data_from_url(args.url_to_scrap, page_number=page_number, scroll_pause_time=args.scroll_pause_time)
        good_imgs = 0
        for image_url in image_urls:
            if '236x341' in image_url:
                good_imgs += 1
        if good_imgs == 60:
            print("Page " + str(page_number) + " has 60 imgs in good resolution")
        else:
            print("Page " + str(page_number) + " doesnt have 60 imgs in good resolution. Skipping push to sql")
            continue
        if (len(image_urls) == 60 and len(product_urls) == 60 and len(brand_names) == 60
                and len(product_names) == 60 and len(prices) == 60):
            print("Page " + str(page_number) + " was scraped successfully")

            scraped_data = {'image_urls': image_urls, 'product_urls': product_urls, 'brand_names': brand_names,
                            'product_names': product_names, 'prices': prices}

            # sending image urls to database
            append_scraped_data_to_postgres_database(scraped_data, args.db_connect_link)
        else:
            print("Page " + str(page_number) + " wasn't scrapped because it doesnt contain exactly 60 objects" +
                  " per product column with high resolution. Duplicates? Bugs?")
            errors += 1

    print('Number of errors during scraping:', errors)


if __name__ == "__main__":
    scrap_site_and_update_database()
