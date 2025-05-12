import configparser
import os
from src.utils.helpers import resource_path

LANG_DIR = resource_path(os.path.join('src', 'settings', 'languages'))
LANG_FILE = resource_path(os.path.join(LANG_DIR, 'lang.ini'))

def get_default_language():
    config = configparser.ConfigParser()
    config.read(LANG_FILE, encoding='utf-8')
    return config.get('Language', 'default', fallback='en')

def load_translations():
    lang = get_default_language()
    ini_file = os.path.join(LANG_DIR, f'{lang}.ini')
    config = configparser.ConfigParser()
    if os.path.exists(ini_file):
        config.read(ini_file, encoding='utf-8')
        return {section: dict(config.items(section)) for section in config.sections()}
    return {}
