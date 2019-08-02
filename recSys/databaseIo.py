import pymysql


class DatabaseIo:

    def __init__(self, info:dict):
        self.info = {'address':info['address'],'username':info['username'],'passwd':info['passwd'],'basename':info['basename']}

    def open(self):
        self.db = pymysql.connect("localhost", "root", "123456", "learningrecommend")
        self.cursor = self.db.cursor()

    def write(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            print('Error: unable to write data')

    def read(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print('Error: unable to fetch data')

    def close(self):
        self.db.close()


sql = """select * 
         from course_dr"""


