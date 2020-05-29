from sqlite3 import connect
from sys import stdout


class DB(object):
    PRODUCTION_DIR = '/home/pi/Desktop/'
    FILE_ACTIVITY_LOG = PRODUCTION_DIR+'database.db'
    FILE_CONFIG = PRODUCTION_DIR+'config.db'
    def __init__(self, file, table):
        self.FILE = file
        self.TABLE = table

    def insert_into(self, sub, url):
        """Commits single record to DB"""
        conn = connect(self.FILE)
        c = conn.cursor()
        sql = 'INSERT INTO %s VALUES("%s", "%s")' % (self.TABLE, sub, url)
        c.execute(sql)
        conn.commit()
        conn.close()

    def contains(self, sub, url):
        """Evaluates if url is in DB. Returns bool"""
        conn = connect(self.FILE)
        c = conn.cursor()
        sql = 'SELECT * FROM %s WHERE subreddit="%s" AND url="%s"' % (self.TABLE, sub, url)
        data = list(c.execute(sql))
        conn.close()
        if len(data) > 0:
            return True
        else:
            return False

    def print_fields(self):
        conn = connect(self.FILE)
        c = conn.execute('SELECT * FROM articles5')
        print(c.description)

    def dump(self):
        conn = connect(self.FILE)
        c = conn.execute('SELECT * FROM articles5')
        for record in c:
            print(record)

    @staticmethod
    def query(file, sql):
        conn = connect(file)
        c = conn.cursor()
        for record in c.execute(sql):
            print(record)
        conn.close()

    @staticmethod
    def query_value(file, sql):
        print(file+ ' - ' + sql)
        conn = connect(file)
        c = conn.cursor()
        data = list(c.execute(sql))
        conn.close()
        return data

    @staticmethod
    def statement(file, sql):
        conn = connect(file)
        c = conn.cursor()
        c.execute(sql)
        conn.commit()
        conn.close()
