import pymysql

# 公众号信息表
class Mysqldb:
    def __init__(self):
        self.db = pymysql.connect(host='localhost', user='root', password='041220', port=3306)
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS spiders DEFAULT CHARACTER SET utf8")

        self.dbconn = pymysql.connect(host='localhost', user='root', password='041220', port=3306, db='spiders')
        self.dbcursor = self.dbconn.cursor()
        self.dbcursor.execute('''CREATE TABLE IF NOT EXISTS Accounts 
            (public_name    VARCHAR(255)    NOT NULL, 
             wechat_id      VARCHAR(255)    NOT NULL, 
             public_image   VARCHAR(255)    NOT NULL,
             authentication VARCHAR(255),
             introduction   VARCHAR(255)    NOT NULL,
             PRIMARY KEY (wechat_id));''')  # wechat_id为唯一主键
        print("初始化成功")

    def __del__(self):
        self.dbconn.close()
        self.db.close()

if __name__ == "__main__":
    Database = Mysqldb()