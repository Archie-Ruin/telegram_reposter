from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

data_file = config.get('default', 'data_file', fallback='data.txt')

api_id = config.get('pyrogram', 'api_id')
api_hash = config.get('pyrogram', 'api_hash')
