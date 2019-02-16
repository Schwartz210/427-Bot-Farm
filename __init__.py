from _thread import start_new_thread

from bot_rss_crawler import RssCrawlerBot
from update import update_local_source_code

def execute():
    start_new_thread(update_local_source_code, ())
    feed_list = 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/rss_feeds.txt'
    sleep_phase = RssCrawlerBot.MINUTE * 15
    bot = RssCrawlerBot(feed_list, sleep_phase, 'rssbot')
    while True:
        bot.act()


if __name__ == '__main__':
    execute()
