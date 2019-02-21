from bot_rss_crawler import RssCrawlerBot


def execute():
    """Starts 427_Bot_Farm"""
    feed_list = 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/rss_feeds.txt'
    bot = RssCrawlerBot(feed_list, 'rssbot')
    bot.set_next_article()


if __name__ == '__main__':
    execute()
