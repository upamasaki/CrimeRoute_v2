# dockerfile to use heroku with flask

# Command to build : docker build -t light606f/kangaroo .
# Command to run : docker run --rm --name kangaroo -it -v $PWD:/home/Light606F/pk -p 5000:5000 light606f/kangaroo

FROM light606f/python
# 作成したユーザの情報
MAINTAINER Light606F <light606f.tsukineko@gmail.com>

RUN sudo -H pip install flask gunicorn \
firebase_admin cloudinary

# install heroku
RUN sudo apt install -y curl; curl https://cli-assets.heroku.com/install.sh | sh

WORKDIR /home/Light606F

# pip install psycopg2-binary たぶんいらない
# heroku login --interactive
# pip freeze > requirements.txt
# heroku create kangaroo-demo
# heroku addons:create heroku-postgresql:hobby-dev
# git push heroku master
