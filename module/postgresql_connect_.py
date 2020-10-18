import os
import psycopg2
import json
import pprint

class PostgreSql:
    def __init__(self):
        self.conn = self.get_connection()
        self.cur  = self.conn.cursor()

    ##############################################
    # DBコネクション取得関数
    #
    def get_connection(self):
        dsn = "host=XXXXXXXXXXXXXX\
            port=XXXX \
            dbname=XXXXXXXXXX \
            user=XXXXXXXXX \
            password=XXXXXXXXXXXXXX"
        return psycopg2.connect(dsn)
    
    ##############################################
    # insert関数
    #
    def insert(self, sqlStr):
        self.cur.execute('BEGIN')
        self.cur.execute(sqlStr)
        self.cur.execute('COMMIT')


    ##############################################
    # mysqlでselectする用の関数
    #
    def select(self,  sqlStr):
        self.cur.execute(sqlStr)
        return list(self.cur)



if __name__ == "__main__":

    psql = PostgreSql()


    ##############################################
    # カラムの追加
    #
    sql = "ALTER TABLE tbl_name ADD COLUMN category2 text;"
    psql.insert(sql)
