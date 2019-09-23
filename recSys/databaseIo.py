import pymssql

import traceback
class DatabaseIo:

    def __init__ (self, info:dict):
        self.info = {'address': info['address'], 'username': info['username'], 'passwd': info['passwd'],
                     'basename': info['basename']}

    def open(self):
        self.db = pymssql.connect("47.106.213.57", "sa", "ASElab905", "learningrecommend")
        self.cursor = self.db.cursor()

    def write(self, sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            print('Error: unable to write data')

    def writeMany(self, sql,li):
        print('进入many')
        try:
            print('进入try')
            n = self.cursor.executemany(sql,li)
            self.db.commit()
            return n
        except Exception as e:
            traceback.print_exc()
            self.db.rollback()
#            print('Error: unable to write data')

    def read(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except:
            print('Error: unable to fetch data')

    def close(self):
        self.db.close()





