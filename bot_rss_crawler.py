__author__ = 'Avi Schwartz, Schwartz210@gmail.com, AviSchwartzCoding.com'
from random import choice
from requests import get

from feedparser import parse

from bot_base_class import Bot
from credits import bot_cred
from database import DB
from logger_thingy import logger, to_console
from gg import out


class RssCrawlerBot(Bot):
    def __init__(self, feed_file, sub):
        self.feed_file = feed_file
        self.sub = sub
        first_credential = bot_cred[0]
        Bot.__init__(self, sub, first_credential[0], first_credential[1], first_credential[2], first_credential[3])
        self.db = DB('/home/pi/Desktop/database.db', 'articles5')

    def get_rss_feed_list(self):
        """Reads RSS Feed file and returns values delimited to list"""
        request = get(self.feed_file)
        requests = request.text.split('\n')
        return [r for r in requests if len(r) != 0]

    def validate_all_feeds(self):
        """Tests all feeds upon startup"""
        bad_feeds = []
        for record in self.get_rss_feed_list():
            feed = parse(record)
            try:
                choice(feed['entries'])
            except:
                bad_feeds.append(record)
        if len(bad_feeds) > 0:
            raise Exception('Bad feeds:', bad_feeds)

    def get_random_article(self, rss_feed_list):
        """Chooses random article"""
        while True:
            out('while loop iteration')
            record = choice(rss_feed_list)
            out(record)
            to_console(2, 'rss: ' + record)
            feed = parse(record)
            out('feed var')
            try:
                article = choice(feed['entries'])
                out('exception not triggered')
            except:
                out('exception triggered')
                with open('/home/pi/Desktop/bad feeds.txt', 'a') as file:
                    file.write(record + '\n')
                continue
            url = article['link']
            out(url)
            to_console(2, 'random article title: ' + article['title'])
            out('after to_console')
            if not self.db.contains(self.sub, url):
                out('DB does not contain')
                return article

    def post(self):
        """Public main sequence"""
        rss_feed_list = self.get_rss_feed_list()
        article = self.get_random_article(rss_feed_list)
        title = article['title']
        link = article['link']
        self.subreddit.submit(title=title, url=link)
        self.db.insert_into(self.sub, link)
        to_console(1, 'Published:')
        to_console(2, title)
        to_console(2, link)
        out('post method')

