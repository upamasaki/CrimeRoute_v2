from flask import Flask, render_template, session
from flask import *
from flask import request

import sys
import os

from module import Exhibit

# postgres database
from module import postgresql_connect

# ファイル名をチェックする関数
from werkzeug.utils import secure_filename

# cloudinary
import cloudinary
import cloudinary.uploader
cloudinary.config(
  cloud_name = "aichi-prefectural-university",
  api_key = "884251713832499",
  api_secret = "gVicsVp9HqJhu_Yxf7xxKDGjVTQ"
)

from pprint import pprint

import blueprint_login	# Add Blueprint for login page by kzh

UPLOAD_FOLDER = './uploads'
# アップロードされる拡張子の制限
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])

app = Flask(__name__)
app.register_blueprint(blueprint_login.bp_login)	# Add Blueprint for login page by kzh

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print("##############################################")
print("# 参照パス一覧")
pprint(sys.path)
print("##############################################")
message = {}
message['page_title_key'] = 'item-list'
message['target_item_key'] = ''

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#
# 必須項目のリスト
# 記載されている項目は必須です
# @author masaki tani 2020.04.29
#
essential_list = ['item_delivery_candidate_date01',
 'item_delivery_candidate_date02',
 'item_delivery_candidate_date03',
 'item_name',
 'item_period1',
 'item_period2',
 'item_price',
 'item_usage',
 'user_name',
 "item_delivery_method"]

essential_list_FLAG = Exhibit.checker_init(essential_list)
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#
# 必須項目のリスト
# 記載されている項目は必須です
# @author masaki tani 2020.04.29
#
essential_list = ['item_delivery_candidate_date01',
 'item_delivery_candidate_date02',
 'item_delivery_candidate_date03',
 'item_name',
 'item_period1',
 'item_period2',
 'item_price',
 'item_usage',
 'user_name',
 "item_delivery_method"]

essential_list_FLAG = Exhibit.checker_init(essential_list)
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
#
# postgres database関係
# @author masaki tani 2020.08.31
#
psql = postgresql_connect.PostgreSql()
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-

# @app.before_first_request
# def init_app():
#   session['username'] = 'me'
#   # pprint(session)
@app.before_first_request
def before_first_request():
    app.logger.info("before_first_request")

###############################################################################
#
# ----- 商品一覧関係のページ ---------------------------------------
#
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ メインページです
# | ここに商品の一覧が表示されます
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/', methods=['GET'])
def index():

  print("##############################################")
  print("# 登録商品一覧")

  ##############################################
  # postgres database ver
  #
  result = psql.select_all()
  result_dict = psql.result_list2dict(result)
  pprint(result_dict)
  message['firebase_get'] = result_dict
  print("##############################################")

  message['page_title_key'] = 'index'
  return render_template('index.html', message=message)




###############################################################################
#
# ----- ルート投稿関係のページ ---------------------------------------
#
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ ルート投稿ページです
# │                              @author masaki tani 2020.10.18
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/route_post', methods=['GET'])
def route_post():

  print("##############################################")
  print("# 登録商品一覧")

  ##############################################
  # postgres database ver
  #
  result = psql.select_all()
  result_dict = psql.result_list2dict(result)
  pprint(result_dict)
  message['firebase_get'] = result_dict
  print("##############################################")

  message['page_title_key'] = 'route_post'
  return render_template('route_post.html', message=message)


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 検索結果を表示するページ
# |    * 'search_key'に検索ワードが入っている
# |
# │                              @author masaki tani 2020.09.20
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/item_search', methods=["GET", "POST"])
def item_search():
  print("##############################################")
  print("> request.form >>>>>>>>>>>>>")
  pprint(request.form)
  print("##############################################")

  sql = "select * from kangaroo_db where item_name like '%{}%';".format(request.form['search_key'])
  result = psql.select(sql)
  result_dict = psql.result_list2dict(result)
  pprint(result_dict)
  message['firebase_get'] = result_dict
  print("##############################################")

  message['page_title'] = 'item-list'

  return render_template('index.html', message=message)


# @app.route('/Itemlist', methods=['GET'])
# def Itemlist():

#   item_dict = {}
#   item_dict['users_ref'] = db.reference('/items')

#   pprint(item_dict['users_ref'].get())
#   message['firebase_get'] = item_dict['users_ref'].get()
#   pprint(message['firebase_get'])
#   message['page_title'] = 'item-list'
#   return render_template('index.html', message=message)


###############################################################################
#
# ----- 商品投稿関係のページ ---------------------------------------
#
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 商品投稿ページです
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/Exhibition')
def Exhibition():
  message['page_title'] = 'Exhibition'
  message['essential_list_FLAG'] = essential_list_FLAG
  return render_template('Exhibition.html', message=message)

@app.route('/ItemDetail/<string:itemKey>')
def ItemDetail(itemKey):
  message['page_title'] = 'ItemDetail'

  ref = db.reference('/items')
  itemRef = ref.child(itemKey).get()

  print("itemRef")
  pprint(itemRef)
  message['target_item_info'] = itemRef
  return render_template('ItemDetail.html', message=message, itemRef=itemRef)

@app.route('/ItemCMD', methods=["GET", "POST"])
def ItemCMD():
  # ===================================================
  # debug
  print("##############################################")
  print(">request.form")
  print(request.form)
  print("##############################################")

  ##############################################
  # データベースから商品を削除
  #
  if('item_delete' in request.form['item_cmd']):
    public_id = request.form['item_cmd'].split("id_")[-1]
    sql = "DELETE FROM kangaroo_db WHERE public_id = {}".format(public_id)
    print(sql)
    psql.insert(sql)

  ##############################################
  # データベースの詳細を取得
  #
  if('item_detail' in request.form['item_cmd']):
    public_id = request.form['item_cmd'].split("id_")[-1]
    sql = "select * from kangaroo_db where public_id = {}".format(public_id)
    print(sql)
    result = psql.select(sql)
    pprint(result)
    result_dict = psql.result_list2dict(result)
    print(">>>>>> target_item_info >>>>>>>")
    pprint(result_dict)
    pprint(result_dict[public_id])
    message['target_item_info'] = result_dict[public_id]

    message['page_title'] = '商品の詳細'
    return render_template('ItemDetail.html', message=message)
    
    # sql = "select * from kangaroo_db where item_name like '%{}%';".format(request.form['public_key'])

  message['page_title'] = 'item-list'

  ##############################################
  # postgres database  all get
  #
  result = psql.select_all()
  result_dict = psql.result_list2dict(result)
  print("##############################################")
  pprint(result_dict)
  message['firebase_get'] = result_dict
  print("##############################################")

  return render_template('index.html', message=message)

###############################################################################
#
# ----- ここから借りる関係のページ ---------------------------------------------
#
#
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 商品を借りるページです
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/RentPage', methods=["GET", "POST"])
def RentPage():
  message['page_title'] = 'RentPage'
  return render_template('./Rent_html/RentPage.html', message=message)


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 配送関係のページです
# | (受け渡し方法、期間の設定ページ)
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/DeliveryPage', methods=["GET", "POST"])
def DeliveryPage():
  message['page_title'] = 'DeliveryPage'
  return render_template('./Rent_html/DeliveryPage.html', message=message)

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 支払いページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/PayPage', methods=["GET", "POST"])
def PayPage():
  message['page_title'] = 'PayPage'
  return render_template('./Rent_html/PayPage.html', message=message)


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 支払いの確認ページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/PayCfmPage', methods=["GET", "POST"])
def PayCfmPage():
  message['page_title'] = 'PayCfmPage'
  return render_template('./Rent_html/PayCfmPage.html', message=message)


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 支払いの結果・通知をするページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/PayCfmPageResult', methods=["GET", "POST"])
def PayCfmPageResult():
  message['page_title'] = 'PayCfmPageResult'
  return render_template('./Rent_html/PayCfmPageResult.html', message=message)


###############################################################################
#
# ----- ここからプロフィール関係のページ ---------------------------------------
#
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ プロフィールのページです
# | ここでユーザー情報などを閲覧できます
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/ProfilePage', methods=["GET", "POST"])
def ProfilePage():
  message['page_title'] = 'ProfilePage'
  return render_template('./Profile_html/ProfilePage.html', message=message)


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ お気に入りに登録した物品を閲覧するページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/FavoritePage', methods=["GET", "POST"])
def FavoritePage():
  message['page_title'] = 'FavoritePage'
  return render_template('./Profile_html/FavoritePage.html', message=message)


# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 投稿した物品を閲覧するページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/OwnItemPage', methods=["GET", "POST"])
def OwnItemPage():
  message['page_title'] = 'OwnItemPage'
  return render_template('./Profile_html/OwnItemPage.html', message=message)

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ ポイント情報を照会するページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/PointPage', methods=["GET", "POST"])
def PointPage():
  message['page_title'] = 'PointPage'
  return render_template('./Profile_html/PointPage.html', message=message)

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 下書きを閲覧するページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/DraftsPage', methods=["GET", "POST"])
def DraftsPage():
  message['page_title'] = 'DraftsPage'
  return render_template('./Profile_html/DraftsPage.html', message=message)


###############################################################################
#
# ----- その他のページ ---------------------------------------
#
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ ページが閲覧不可の場合に遷移するページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    message['page_title'] = '404'
    return render_template('index.html', message=message), 404

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ お問い合わせするページです
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/ContactUsPage', methods=["GET", "POST"])
def ContactUsPage():
  message['page_title'] = 'ContactUsPage'
  return render_template('ContactUsPage.html', message=message)




# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 開発用に使用するアイコン一覧ページです
# │ ここでアイコンのIDを調べて使用してください
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route('/IconsPage')
def IconsPage():
  message['page_title'] = 'IconsPage'
  return render_template('./original_html/IconsPage.html', message=message)

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ 商品を登録する関数です
# | + 写真のアップロード
# | + firebaseへの登録
# | + 登録情報の確認(入力漏れがないかどうか)
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
@app.route("/login_manager", methods=["POST"])  #追加
def login_manager():
  # ===================================================
  # page init
  message['page_title'] = 'Exhibition'

  # ===================================================
  # debug
  print("##############################################")
  print(">request.form")
  print(request.form)
  print("##############################################")
  print(">request.files")
  print(request.files)

  print("##############################################")
  print("> request.form >>>>>>>>>>>>>")
  pprint(request.form)
  print("##############################################")
  print("> request.file >>>>>>>>>>>>>")
  pprint(request.files['file'])

  # ===================================================
  # 必須項目の確認
  print("##############################################")
  print("# 必須項目の確認")
  essential_list_FLAG = Exhibit.checker(request, essential_list)
  message["essential_list_FLAG"] = essential_list_FLAG

  pprint(message)
  print("##############################################")
  # ===================================================
  # item image loading
  if 'file' not in request.files:
    print('ファイルがありません')
    return render_template('Exhibition.html', message=message)

  # データの取り出し
  file = request.files['file']

  # ファイル名がなかった時の処理
  if file.filename == '':
    print('ファイルがありません')
    return render_template('Exhibition.html', message=message)

  # ファイルのチェック
  if file and allwed_file(file.filename):
    # 危険な文字を削除（サニタイズ処理）
    filename = secure_filename(file.filename)
    # ファイルの保存
    img_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(img_path)
    # アップロード後のページに転送

    # cloudinary regist
    #res = cloudinary.uploader.upload(file=img_path, public_id=filename)
    res = cloudinary.uploader.upload(file=img_path)
    print("##############################################")
    print("# cloudinary regist info")
    pprint(res)
    print("##############################################")
    message['item_img_url'] = res['secure_url']
    message['public_id'] = res['public_id']

    # ===================================================
    # item databse writing
    item_dict = {}
    item_dict['user_name'] = request.form['user_name']
    item_dict['item_name'] = request.form['item_name']
    item_dict['item_usage'] = request.form['item_usage']
    item_dict['item_img_url'] = res['secure_url']

    item_dict['item_delivery_candidate_date01'] = request.form['item_delivery_candidate_date01']
    item_dict['item_delivery_candidate_date02'] = request.form['item_delivery_candidate_date02']
    item_dict['item_delivery_candidate_date03'] = request.form['item_delivery_candidate_date03']
    item_dict['item_period1'] = request.form['item_period1']
    item_dict['item_period2'] = request.form['item_period2']
    item_dict['item_price'] = request.form['item_price']
    item_dict['regist_day'] = request.form['regist_day']

    item_dict['delivery_city'] = request.form['delivery_city']
    item_dict['rent_type'] = request.form['rent_type']
    item_dict['category1'] = request.form['category1']
    item_dict['category2'] = request.form['category2']

    # 主キーを登録
    item_dict['public_id'] = res['public_id']

    ##############################################
    # postgres databaseへ登録
    #
    inset_dict = {}
    inset_dict['items'] = {}
    inset_dict['items'][0] = item_dict
    psql.json_insert(inset_dict)

  # ++++++++++++++++++++++++++++++++++++++
  # ポップアップがでるようにしたい

  # ++++++++++++++++++++++++++++++++++++++


  return render_template('Exhibition.html', message=message)

# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
# │
# │ アップロードされた写真のファイルが
# | 有効なファイルかどうかを確認します
# |
# │                              @author masaki tani 2020.05.24
# +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-
def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':

  app.run(host='0.0.0.0', port=5001, debug=True)

  ##############################################
  # +++++++++++++++++++++++++++++++++++++++++++
  #
  # requirements.txtが古いとエラーがでます．
  # 最新の状態にしましょう
  #
  # pip freeze > requirements.txt
  # +++++++++++++++++++++++++++++++++++++++++++
  ##############################################
