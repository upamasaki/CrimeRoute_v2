# -*- coding: utf-8 -*-

import sqlite3
from contextlib import closing
from datetime import datetime as dt


tdatetime = dt.now()
tstr = tdatetime.strftime('%Y/%m/%d')



dbname = '../datasets/database6.db'

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()

    # executeメソッドでSQL文を実行する
    # create_table = '''create table route_lists (id integer primary key autoincrement, 
    #                                             name varchar(64),
    #                                             grade int, 
    #                                             img_path text,
    #                                             regit_date DATE)'''
    # c.execute(create_table)

    # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
    # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
    # タプルで渡す．
    tstr = dt.now().strftime('%Y-%m-%d')
    sql = 'insert into route_lists (name, grade, img_path, regit_date) values (?,?,?,?)'
    user = ('Taro', 20, 'male', tstr)
    c.execute(sql, user)

    # 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
    # executemanyメソッドを実行する
    tstr = dt.now().strftime('%Y-%m-%d')
    insert_sql = 'insert into route_lists (name, grade, img_path, regit_date) values (?,?,?,?)'
    route_lists = [
        ('Shota', 54, 'male', tstr),
        ('Nana', 40, 'female', tstr),
        ('Tooru', 78, 'male', tstr),
        ('Saki', 31, 'female', tstr)
    ]
    c.executemany(insert_sql, route_lists)
    conn.commit()

    select_sql = 'select * from route_lists'
    for row in c.execute(select_sql):
        print(row)