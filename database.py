from sqlite3 import connect
from gg import out


class DB(object):
    def __init__(self, file, table):
        self.FILE = file
        self.TABLE = table

    def insert_into(self, sub, url):
        """Commits single record to DB"""
        conn = connect(self.FILE)
        c = conn.cursor()
        sql = 'INSERT INTO %s VALUES("%s", "%s")' % (self.TABLE, sub, url)
        c.execute(sql)
        out('after execute')
        conn.commit()
        conn.close()

    def contains(self, sub, url):
        """Evaluates if url is in DB. Returns bool"""
        out('contains')
        conn = connect(self.FILE)
        c = conn.cursor()
        sql = 'SELECT * FROM %s WHERE subreddit="%s" AND url="%s"' % (self.TABLE, sub, url)
        out(sql)
        data = list(c.execute(sql))
        out('after execute')
        conn.close()
        if len(data) > 0:
            out('true')
            return True
        else:
            out('false')
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


