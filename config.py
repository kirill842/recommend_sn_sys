import os
try:
    RUN_FROM_DOCKER = os.environ['RUN_FROM_DOCKER']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    DB_CONNECT_LINK = os.environ['DB_CONNECT_LINK']
    URL_TO_SCRAP = os.environ['URL_TO_SCRAP']
    CHROME_DRIVER_PATH = os.environ['CHROME_DRIVER_PATH']
    NUM_OF_PAGES_TO_SCRAP = os.environ['NUM_OF_PAGES_TO_SCRAP']
    SCROLL_PAUSE_TIME = os.environ['SCROLL_PAUSE_TIME']
    USER = os.environ['USER']
    PASSWORD = os.environ['PASSWORD']
    HOST = os.environ['HOST']
    PORT = os.environ['PORT']
    DATABASE = os.environ['DATABASE']
    TABLE_NAME = os.environ['TABLE_NAME']
except Exception as e:
    print('Unable to find one of env vars', e, 'Using default script')
    import yaml
    with open("config.yaml", "r") as stream:
        print('Opening yaml file')
        try:
            configs = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    RUN_FROM_DOCKER = 0
    BOT_TOKEN = configs['bot_token']
    DB_CONNECT_LINK = configs['db_connect_link']
    URL_TO_SCRAP = configs['url_to_scrap']
    CHROME_DRIVER_PATH = configs['chrome_driver_path']
    NUM_OF_PAGES_TO_SCRAP = configs['num_of_pages_to_scrap']
    SCROLL_PAUSE_TIME = configs['scroll_pause_time']
    USER = configs['user']
    PASSWORD = configs['password']
    HOST = configs['host']
    PORT = configs['port']
    DATABASE = configs['database']
    TABLE_NAME = configs['table_name']

print('Configuration was loaded')

# import pickle
# with open('./first_launch.pkl', 'rb') as file:
#     first_launch = pickle.load(file)
#
# if first_launch:
#     print('Insert your bot token')
#     bot_token = input()
#     with open('./bot_token.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(bot_token, file)
#     print('Insert info for connection to database. Example: postgresql://<user>:<password>@<ip>:<port>/<database_name>')
#     db_connect_link = input()
#     with open('./db_connect_link.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(db_connect_link, file)
#     print('url to scrap images from, only lamoda.ru supported with exactly 60 products on 1 page ' +
#           'example: https://www.lamoda.ru/c/5971/shoes-muzhkrossovki +- /?sort=new')
#     url_to_scrap = input()
#     with open('./url_to_scrap.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(url_to_scrap, file)
#     print('path to chrome driver. ./chromedriver for Docker')
#     chrome_driver_path = input()
#     with open('./chrome_driver_path.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(chrome_driver_path, file)
#     print('How many pages to scrape on first launch')
#     num_of_pages_to_scrap = int(input())
#     with open('./num_of_pages_to_scrap.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(num_of_pages_to_scrap, file)
#     print('Scrolling pause while scraping. 0.2 is enough for lamoda.ru')
#     scroll_pause_time = float(input())
#     with open('./scroll_pause_time.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(scroll_pause_time, file)
#     print('Insert sql info to connect to your database')
#     print('<user>')
#     user = input()
#     with open('./user.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(user, file)
#     print('<password>')
#     password = input()
#     with open('./password.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(password, file)
#     print('<host>')
#     host = input()
#     with open('./host.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(host, file)
#     print('<port>')
#     port = int(input())
#     with open('./port.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(port, file)
#     print('Insert sql database name')
#     database = str(input())
#     with open('./database.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(database, file)
#     print('Insert sql table name where to save scraped data')
#     table_name = input()
#     with open('./table_name.pkl', 'wb') as file:
#         # A new file will be created
#         pickle.dump(table_name, file)
# else:
#     with open('./bot_token.pkl', 'rb') as file:
#         # A new file will be created
#         bot_token = pickle.load(file)
#     with open('./db_connect_link.pkl', 'rb') as file:
#         # A new file will be created
#         db_connect_link = pickle.load(file)
#     with open('./url_to_scrap.pkl', 'rb') as file:
#         # A new file will be created
#         url_to_scrap = pickle.load(file)
#     with open('./chrome_driver_path.pkl', 'rb') as file:
#         # A new file will be created
#         chrome_driver_path = pickle.load(file)
#     with open('./num_of_pages_to_scrap.pkl', 'rb') as file:
#         # A new file will be created
#         num_of_pages_to_scrap = pickle.load(file)
#     with open('./scroll_pause_time.pkl', 'rb') as file:
#         # A new file will be created
#         scroll_pause_time = pickle.load(file)
#     with open('./user.pkl', 'rb') as file:
#         # A new file will be created
#         user = pickle.load(file)
#     with open('./password.pkl', 'rb') as file:
#         # A new file will be created
#         password = pickle.load(file)
#     with open('./host.pkl', 'rb') as file:
#         # A new file will be created
#         host = pickle.load(file)
#     with open('./port.pkl', 'rb') as file:
#         # A new file will be created
#         port = pickle.load(file)
#     with open('./database.pkl', 'rb') as file:
#         # A new file will be created
#         database = pickle.load(file)
#     with open('./table_name.pkl', 'rb') as file:
#         # A new file will be created
#         table_name = pickle.load(file)
#
# print('Config files saved')
