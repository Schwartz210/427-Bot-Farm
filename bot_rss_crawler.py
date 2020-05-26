__author__ = 'Avi Schwartz, Schwartz210@gmail.com, AviSchwartzCoding.com'
from random import choice
from requests import get

from feedparser import parse

from bot_base_class import Bot
from credits import bot_cred
from database import DB
from logger_thingy import logger, to_console


class RssCrawlerBot(Bot):
    def __init__(self, sub):
        self.feed_file = 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/rss_feeds.txt'
        bot_info = DB.query_value(DB.FILE_CONFIG, 'select user_name, password, client_id, client_secret from bots where subreddit="{}"'.format(sub))[0]
        self.user_name = bot_info[0]
        Bot.__init__(self, sub, bot_info[0], bot_info[1], bot_info[2], bot_info[3])
        self.db = DB(DB.FILE_ACTIVITY_LOG, 'articles5')

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
            record = choice(rss_feed_list)
            to_console(2, 'rss: ' + record)
            feed = parse(record)
            try:
                article = choice(feed['entries'])
            except:
                with open('/home/pi/Desktop/bad feeds.txt', 'a') as file:
                    file.write(record + '\n')
                continue
            url = article['link']
            to_console(2, 'random article title: ' + article['title'])
            if not self.db.contains(self.sub, url):
                return article

    def post_one_random_article(self):
        """Public main sequence"""
        if self.sub == 'rssbot':
            rss_feed_list = self.get_rss_feed_list()
        else:
            sql = 'select word from searchterms where user_name="{}"'.format(self.user_name)
            rss_feed_list = ['https://news.google.com/rss/search?q='+elem[0] for elem in DB.query_value(DB.FILE_CONFIG, sql)]
        article = self.get_random_article(rss_feed_list)
        title = article['title']
        link = article['link']
        self.subreddit.submit(title=title, url=link)
        self.db.insert_into(self.sub, link)
        to_console(1, 'Published:')
        to_console(2, title)
        to_console(2, link)

    def post_all_of_a_feeds_article(self):
        """Selects a feed and posts all of the article into a single post"""
        iterator = DB.query_value('SELECT VALUE FROM flags WHERE ID=1')[0][0]
        feed = self.get_rss_feed_list()[iterator]
        entries = parse(feed)['entries']
        '''todo: api call all article and store var'''
        post_text = ''
        for elem in entries:
            #print(elem['title']+ ' | ' +elem['link']+ ' | ' +str(elem['authors'][0]['name']))
            author = elem['authors'][0]['name']
            title = elem['title']
            url = elem['link']

            post_text += '[{}]({}) by {}\n*****'.format(title, url, author)
        print(post_text)
        '''todo: post text to reddit'''

    def test_feed(self):
        entries = parse('https://news.google.com/rss/search?q=monticello')['entries']
        print(entries)
        post_text = ''
        for elem in entries:
            #print(elem['title']+ ' | ' +elem['link']+ ' | ' +str(elem['authors'][0]['name']))
            #author = elem['authors'][0]['name']
            title = elem['title']
            url = elem['link']

            post_text += '[{}]({})\n'.format(title, url)
            #post_text += '[{}]({})|{}\n\n'.format(title, url, author)
        print(post_text)


