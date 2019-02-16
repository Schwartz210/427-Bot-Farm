from time import sleep

from praw import Reddit

from logger_thingy import to_console


class Bot(object):
    MINUTE = 60
    HOUR = MINUTE * 60

    def __init__(self, sub, user_name, password, client_id, client_secret):
        self.sub = sub
        self.reddit = Reddit(user_agent='having fun',
                             username=user_name,
                             password=password,
                             client_id=client_id,
                             client_secret=client_secret)
        self.subreddit = self.reddit.subreddit('rssbot')

    def set_credentials(self, user_name, password, client_id, client_secret):
        self.reddit = Reddit(user_agent='having fun',
                             username=user_name,
                             password=password,
                             client_id=client_id,
                             client_secret=client_secret)
        self.subreddit = self.reddit.subreddit('rssbot')

    def wait(self, seconds):
        """Produces cleen console output for waiting"""
        while seconds > 0:
            sleep(1)
            seconds -= 1
            if seconds % 30 == 0:
                to_console(2, 'Seconds left in sleep phase: ' + str(seconds))

    def act(self):
        """Abstract method gets implemented in children classes"""
        pass


