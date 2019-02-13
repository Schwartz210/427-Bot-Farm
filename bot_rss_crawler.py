__author__ = 'Avi Schwartz, Schwartz210@gmail.com, AviSchwartzCoding.com'
from random import choice
from requests import get
from time import sleep

from feedparser import parse

from bot_base_class import Bot
from credits import bot_cred
from database import RssDB
from logger_thingy import logger, to_console


class RssCrawlerBot(Bot):
    def __init__(self):
        first_credential = bot_cred[0]
        Bot.__init__(self, first_credential[0], first_credential[1], first_credential[2], first_credential[3])
        self.credential_iterator = 0
        self.db = RssDB('database.db', 'articles')

    @logger
    def read_file(self):
        """Reads RSS Feed file and returns values delimited to list"""
        request = get('https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/rss_feeds.txt')
        return request.text.split('\n')

    @logger
    def print_feed(self):
        """Dumps RSS data to console for testing"""
        data = self.read_file()
        for record in data:
            feed = parse(record)
            print(record)
            for entry in feed['entries']:
                print(entry)

    @logger
    def reset_credentials(self):
        """Changes bot credentials to circumvent API posting frequency limits. A bot can only post an article
        every 10 min"""
        self.credential_iterator += 1
        if self.credential_iterator == len(bot_cred):
            self.credential_iterator = 0
        new_credentials = bot_cred[self.credential_iterator]
        self.set_credentials(new_credentials[0], new_credentials[1], new_credentials[2], new_credentials[3])

    @logger
    def get_random_article(self):
        """Chooses random article"""
        rss_feed_list = self.read_file()
        while True:
            try:
                record = choice(rss_feed_list)
                feed = parse(record)
                article = choice(feed['entries'])
                url = article['link']
                if not self.db.contains(url):
                    return article
            except:
                continue

    @logger
    def act(self):
        """Public main sequence"""
        while True:
            article = self.get_random_article()
            self.subreddit.submit(title=article['title'], url=article['link'])
            self.db.insert_into(article['link'])
            to_console(1, 'Published:')
            to_console(2, article['title'])
            to_console(2, article['link'])
            self.reset_credentials()
            sleep(Bot.MINUTE * 3.5)
