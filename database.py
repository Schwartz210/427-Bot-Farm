from sqlite3 import connect


class DB:
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
