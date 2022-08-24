import yaml

with open("config.yaml", "r") as stream:
    print('Opening yaml file')
    try:
        configs = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

bot_token = configs['bot_token']
db_connect_link = configs['db_connect_link']
url_to_scrap = configs['url_to_scrap']
chrome_driver_path = configs['chrome_driver_path']
num_of_pages_to_scrap = configs['num_of_pages_to_scrap']
scroll_pause_time = configs['scroll_pause_time']
user = configs['user']
password = configs['password']
host = configs['host']
port = configs['port']
database = configs['database']
table_name = configs['table_name']

print('config file was loaded')
