from requests import get

FILES = {
    'bot_rss_crawler.py': 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/bot_rss_crawler.py',
    'go.py': 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/__init__.py',
    'logger_thingy.py': 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/logger_thingy.py',
    'database.py': 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/database.py',
    'update.py': 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/update.py',
    'bot_base_class.py': 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/bot_base_class.py'
}


def update_file(url, filename):
    """Overwrites old program files with new ones pulled from Github"""
    data = get(url)
    lines = data.text.strip('\n')
    file = open(filename, 'w')
    for line in lines:
        file.write(line)
    file.close()


def update_local_source_code():
    """Executes script"""
    for filename in FILES.keys():
        url = FILES[filename]
        update_file(url, filename)
        print('updated:', filename)



