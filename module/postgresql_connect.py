import os
import psycopg2
import json
import pprint

##############################################
# heroku link
# https://data.heroku.com/dataclips/cmsxhjkwexsjiuwzrqhrsfdlohpm


##############################################
# heroku とデータベース接続参考サイト
#
# postgres × python (+ heroku)
# https://qiita.com/ryuichi1208/items/8a631d6ffc55a03a400b
#
# FlaskとPostgreSQLでウェブアプリを作ってHerokuで無料で運用する
# https://qiita.com/croquette0212/items/9b4dc5377e7d6f292671


##############################################
# データベース基本サイト(よく見るサイト)
#
# データを追加する(INSERT文)
# https://www.dbonline.jp/mysql/insert/index1.html


class PostgreSql:
    def __init__(self):
        self.conn = self.get_connection()
        self.cur  = self.conn.cursor()
        self.insert_cols_name_list = ["item_delivery_candidate_date01",
                                    "item_delivery_candidate_date02",
                                    "item_delivery_candidate_date03",
                                    "item_img_url",
                                    "item_name",
                                    "item_period1",
                                    "item_period2",
                                    "item_price",
                                    "item_usage",
                                #    "public_id",
                                    "regist_day",
                                    "user_name",
                                    "category1",
                                    "category2",
                                    "rent_type",
                                    "delivery_city",]

        self.select_cols_name_list = ["item_delivery_candidate_date01",
                                    "item_delivery_candidate_date02",
                                    "item_delivery_candidate_date03",
                                    "item_img_url",
                                    "item_name",
                                    "item_period1",
                                    "item_period2",
                                    "item_price",
                                    "item_usage",
                                    "public_id",
                                    "regist_day",
                                    "user_name",
                                    "category1",
                                    "category2",
                                    "rent_type",
                                    "delivery_city",]

        self.public_id_idx = self.select_cols_name_list.index('public_id')
    ##############################################
    # DBコネクション取得関数
    #
    def get_connection(self):
        dsn = "host=ec2-52-204-232-46.compute-1.amazonaws.com\
            port=5432 \
            dbname=d449e2ctiv5ie4 \
            user=qtchdxxhajazix \
            password=32b00b27e761f0d7f0025f78707e919ef94c2837ac4928dad933ab4f696f7633"
        return psycopg2.connect(dsn)
    

    ##############################################
    # データベースデータの接続チェック
    #
    def get_response_test(self):
        sqlStr = "SELECT * FROM weather ;"
        print("sqlStr   : {}".format(sqlStr))
        self.cur.execute(sqlStr)
        print("self.cur : {}".format(self.cur))
        for i, row in enumerate(self.cur):
            print("result[{}]:{}".format(i, row))
    #
    def get_response_test2(self):
        sqlStr = "SELECT * FROM kangaroo_db;"
        print("sqlStr   : {}".format(sqlStr))
        self.cur.execute(sqlStr)
        print("self.cur : {}".format(self.cur))
        for i, row in enumerate(self.cur):
            print("result[{}]:{}".format(i, row))
    

    ##############################################
    # json のインポート関数
    #
    @staticmethod
    def import_json(json_path):
        json_open = open(json_path, 'r', encoding="utf-8_sig")
        json_load = json.load(json_open)
        return json_load

    ##############################################
    # insert関数
    #
    def insert(self, sqlStr):
        self.cur.execute('BEGIN')
        self.cur.execute(sqlStr)
        self.cur.execute('COMMIT')


    ##############################################
    # json ファイルのinsert関数
    #   * 主にfirebaseからの移行に使用
    #
    def json_insert(self, json_load):
        pprint.pprint(json_load)
        for _, v in json_load['items'].items():
            # insert の列名の部分
            insert_front = []
            # insert の値の部分
            insert_back  = []


            for iname in self.insert_cols_name_list:
                # 入力の列数に対してチェック
                assert iname in v.keys() , '!!! 入力の列数が足りません !!!'
                insert_front.append("{}".format(iname))
                insert_back.append("'{}'".format(v[iname]))
            
            cols = ', '.join(insert_front)
            values = ', '.join(insert_back)
            sqlStr = 'insert into kangaroo_db ({}) values ({});'.format(cols, values)
            # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            # print(cols)
            # print(values)
            print(sqlStr)
            self.insert(sqlStr)

    ##############################################
    # データベースデータをすべて表示する用の関数
    #
    def select_all(self):
        sqlStr = "SELECT * FROM kangaroo_db;"
        # print("sqlStr   : {}".format(sqlStr))
        self.cur.execute(sqlStr)
        # print("self.cur : {}".format(self.cur))
        return list(self.cur)

    ##############################################
    # mysqlでselectする用の関数
    #
    def select(self,  sqlStr):
        self.cur.execute(sqlStr)
        # print("self.cur : {}".format(self.cur))
        return list(self.cur)

    ##############################################
    # selectの返り値をdict型に変換
    #   * すべての列を返している場合に使用
    #
    def result_list2dict(self, result_list):
        result_dict = {}
        for _, values in enumerate(result_list):
            public_id = str(values[self.public_id_idx])
            result_dict[public_id] = {}
            for v, name in zip(values, self.select_cols_name_list):
                result_dict[public_id][name] = v
        
        return result_dict

if __name__ == "__main__":
    # get_response_message2()

    psql = PostgreSql()
    # psql.get_response_test2()
    # result = psql.select_all()
    # pprint.pprint(list(result))
    # result_dict = psql.result_list2dict(result)
    # pprint.pprint(result_dict)

    # # raise
    # json_load = psql.import_json(r'..\datasets\kangaroo-flask-v1-export.json')
    # # pprint.pprint(json_load['items'])
    # psql.json_insert(json_load)

    ##############################################
    # カラムの追加
    #
    # sql = "ALTER TABLE kangaroo_db ADD COLUMN category2 text;"
    # psql.insert(sql)
    # sql = "ALTER TABLE kangaroo_db ADD COLUMN rent_type text;"
    # psql.insert(sql)
    # sql = "ALTER TABLE kangaroo_db ADD COLUMN delivery_city text;"
    # psql.insert(sql)
    # raise

    result = psql.select_all()
    result_dict = psql.result_list2dict(result)
    pprint.pprint(result_dict)



