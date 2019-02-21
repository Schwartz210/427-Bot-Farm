__author__ = 'Avi Schwartz, Schwartz210@gmail.com, AviSchwartzCoding.com'
from random import choice
from requests import get

from feedparser import parse

from bot_base_class import Bot
from credits import bot_cred
from database import DB
from logger_thingy import logger, to_console


class RssCrawlerBot(Bot):
    def __init__(self, feed_file, sub):
        self.feed_file = feed_file
        self.sub = sub
        first_credential = bot_cred[0]
        Bot.__init__(self, sub, first_credential[0], first_credential[1], first_credential[2], first_credential[3])
        self.next_article_file = 'next_article.txt'
        self.db = DB('database.db', 'articles5')
        self.validate_all_feeds()
        self.set_next_article()

    @logger
    def get_rss_feed_list(self):
        """Reads RSS Feed file and returns values delimited to list"""
        request = get(self.feed_file)
        requests = request.text.split('\n')
        return [r for r in requests if len(r) != 0]

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
        if len(bad_feeds) > 0:
            raise Exception('Bad feeds:', bad_feeds)

    @logger
    def get_random_article(self, rss_feed_list):
        """Chooses random article"""
        while True:
            to_console(1, 'while loop iteration')
            record = choice(rss_feed_list)
            to_console(2, 'rss: ' + record)
            feed = parse(record)
            try:
                article = choice(feed['entries'])
            except:
                raise Exception('Bad feed', record)
            url = article['link']
            to_console(2, 'random article title: ' + article['title'])
            if not self.db.contains(self.sub, url):
                return article

    @logger
    def set_next_article(self):
        """Prepares next article"""
        to_console(1, 'Starting article fetch..')
        rss_feed_list = self.get_rss_feed_list()
        article = self.get_random_article(rss_feed_list)
        text = article['title'] + '||' + article['url']
        file = open(self.next_article_file, 'w')
        file.write(text)
        file.close()

    @logger
    def post(self):
        """Public main sequence"""
        article = open(self.next_article_file, 'r')
        title, link = article.read().strip('\n').split('||')
        self.subreddit.submit(title=title, url=link)
        self.db.insert_into(self.sub, link)
        to_console(1, 'Published:')
        to_console(2, title)
        to_console(2, link)
        to_console(1, 'Entering sleep phase...')

