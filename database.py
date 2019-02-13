from sqlite3 import connect


class DB(object):
    def __init__(self, file, table):
        self.FILE = file
        self.TABLE = table

    def insert_into(self, record):
        """Abstract method"""
        pass

    def contains(self, value):
        """Abstract method"""
        pass

    def dump(self):
        """Prints contents of DB to console"""
        conn = connect(self.FILE)
        c = conn.cursor()
        sql = 'SELECT * FROM %s' % self.TABLE
        data = list(c.execute(sql))
        conn.commit()
        conn.close()
        for record in data:
            print(record)


class RssDB(DB):
    def __init__(self, file, table):
        DB.__init__(self, file, table)

    def insert_into(self, url):
        """Commits single record to DB"""
        conn = connect(self.FILE)
        c = conn.cursor()
        sql = 'INSERT INTO %s VALUES("%s")' % (self.TABLE, url)
        c.execute(sql)
        conn.commit()
        conn.close()

    def contains(self, url):
        """Evaluates if url is in DB. Returns bool"""
        conn = connect(self.FILE)
        c = conn.cursor()
        sql = 'SELECT * FROM %s WHERE url="%s"' % (self.TABLE, url)
        data = list(c.execute(sql))
        conn.close()
        if len(data) > 0:
            return True
        else:
            return False


