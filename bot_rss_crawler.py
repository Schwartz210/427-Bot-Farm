__author__ = 'Avi Schwartz, Schwartz210@gmail.com, AviSchwartzCoding.com'
from random import choice
from requests import get
from _thread import start_new_thread

from feedparser import parse

from bot_base_class import Bot
from credits import bot_cred
from database import DB
from logger_thingy import logger, to_console


class RssCrawlerBot(Bot):
    def __init__(self, feed_file, wait_time, sub):
        self.feed_file = feed_file
        self.wait_time = wait_time
        self.sub = sub
        first_credential = bot_cred[0]
        Bot.__init__(self, sub, first_credential[0], first_credential[1], first_credential[2], first_credential[3])
        self.credential_iterator = 0
        self.db = DB('database.db', 'articles5')
        self.rss_feed_list = []
        self.article = None
        self.validate_all_feeds()
        to_console(1, 'Starting article fetch..')
        self.read_file()
        self.get_random_article()

    @logger
    def read_file(self):
        """Reads RSS Feed file and returns values delimited to list"""
        request = get(self.feed_file)
        requests = request.text.split('\n')
        self.rss_feed_list = [r for r in requests if len(r) != 0]

    @logger
    def print_feed(self):
        """Dumps RSS data to console for testing"""
        data = self.read_file()
        for record in data:
            feed = parse(record)
            for entry in feed['entries']:
                print(entry)

    @logger
    def validate_all_feeds(self):
        """Tests all feeds upon startup"""
        bad_feeds = []
        for record in self.rss_feed_list:
            feed = parse(record)
            try:
                choice(feed['entries'])
            except:
                bad_feeds.append(record)
        if len(self.rss_feed_list) > 0:
            raise Exception('Bad feeds:', bad_feeds)
    
    @logger
    def get_random_article(self):
        """Chooses random article"""
        while True:
            to_console(1, 'while loop iteration')
            record = choice(self.rss_feed_list)
            to_console(2, 'rss: ' + record)
            feed = parse(record)
            try:
                article = choice(feed['entries'])
            except:
                raise Exception('Bad feed', record)
            url = article['link']
            to_console(2, 'random article title: ' + article['title'])
            if not self.db.contains(self.sub, url):
                self.article = article
                return

    @logger
    def sleep_phase(self):
        to_console(1, 'Starting article fetch..')
        self.read_file()
        self.get_random_article()

    @logger
    def act(self):
        """Public main sequence"""
        self.subreddit.submit(title=self.article['title'], url=self.article['link'])
        self.db.insert_into(self.sub, self.article['link'])
        to_console(1, 'Published:')
        to_console(2, self.article['title'])
        to_console(2, self.article['link'])
        to_console(1, 'Entering sleep phase...')
        start_new_thread(self.sleep_phase, ())
        self.wait(self.wait_time)
