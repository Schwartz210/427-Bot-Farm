from bot_rss_crawler import RssCrawlerBot
from database import DB


def execute():
    """Starts 427_Bot_Farm"""
    subreddits = DB.query_value(DB.FILE_CONFIG, 'select subreddit from bots where active=1')
    for subreddit in subreddits:
        bot = RssCrawlerBot(subreddit[0])
        bot.post_one_random_article()


if __name__ == '__main__':
    execute()
