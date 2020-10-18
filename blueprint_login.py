import flask
import urllib.parse

client_id = '889047026615-j8ql7mrveofltv3dn6be6ve272racbi2.apps.googleusercontent.com'
client_secret = '_G4tJF-mzFE-v-nfk4HSfgLG'
redirect_uri = 'https://flask-web-project-kangaroo-v3.herokuapp.com/login/check'
state = 'this is test'  # 本当はこれはランダム

bp_login = flask.Blueprint("bp_login", __name__)

@bp_login.route('/login')
def login():
	return flask.redirect('https://accounts.google.com/o/oauth2/auth?{}'.format(urllib.parse.urlencode({
		'client_id': client_id,
		'scope': 'email',
		'redirect_uri': redirect_uri,
		'state': state,
		'openid.realm': 'https://flask-web-project-kangaroo-v3.herokuapp.com',
		'response_type': 'code'
	})))

@bp_login.route("/privacy_policy")
def privacy_policy():
	return flask.render_template('privacy_policy.html')
