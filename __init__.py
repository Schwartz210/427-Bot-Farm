from bot_rss_crawler import RssCrawlerBot


def execute():
    feed_list = 'https://raw.githubusercontent.com/Schwartz210/427-Bot-Farm/master/rss_feeds.txt'
    sleep_phase = RssCrawlerBot.MINUTE * 15
    bot = RssCrawlerBot(feed_list, sleep_phase)
    bot.act()


if __name__ == '__main__':
    execute()


