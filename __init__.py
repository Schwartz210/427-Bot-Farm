from bot_rss_crawler import RssCrawlerBot


def execute():
    """Starts 427_Bot_Farm"""
    bot = RssCrawlerBot('rssbot')
    bot.test_feed()


if __name__ == '__main__':
    execute()
