import os
try:
    RUN_FROM_DOCKER = os.environ['RUN_FROM_DOCKER']
    BOT_TOKEN = os.environ['BOT_TOKEN']
    DB_CONNECT_LINK = os.environ['DB_CONNECT_LINK']
    URL_TO_SCRAP = os.environ['URL_TO_SCRAP']
    CHROME_DRIVER_PATH = './chromedriver'
    NUM_OF_PAGES_TO_SCRAP = int(os.environ['NUM_OF_PAGES_TO_SCRAP'])
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
