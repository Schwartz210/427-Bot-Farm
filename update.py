from requests import get


def update_file(url, filename):
    data = get(url)
    lines = data.text.strip('\n')
    file = open(filename, 'w')
    for line in lines:
        file.write(line)
    file.close()


files = {
    'bot_rss_crawler.py' : 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/bot_rss_crawler.py',
    '__init__.py' : 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/__init__.py'
}


def run_updates():
    for filename in files.keys():
        url = files[filename]
        update_file(url, filename)
        print('updated:', filename)
