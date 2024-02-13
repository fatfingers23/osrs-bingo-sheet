from time import sleep
import sys
import logging
import flask_login
import flask
from flask import Flask, jsonify, send_file, abort
from insomniacs.db.actions import query_database, init_table_from_config, MysqlConnection, get_tiles
from insomniacs.db.login import User, auth_user, check_for_username
from insomniacs.configuration import Teams
from insomniacs.db.queries import Query

login_manager = flask_login.LoginManager()
app = Flask(__name__, static_folder="/srv", static_url_path="/")
app.secret_key = b'jsutsomejunkfornow'  # TODO: Make this so more securely generated key from a config
app.TABLE_CREATED = False

handler = logging.StreamHandler(sys.stdout)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def user_loader(user_id):
    """
    Defined for flask_login for loading users

    :param user_id: str that identifies the user
    :return: User
    """
    app.logger.debug("User loader for user: %s", user_id)
    if user_id and check_for_username(User(user_id)):
        return User(user_id)


@login_manager.request_loader
def request_loader(request):
    """
    Defined for flask_login for loading users via a request

    :param request: A flask request obj for loading users from a form re-submission
    :return: User
    """
    user_id = request.form.get('username')
    app.logger.debug("Request loading for user: %s", user_id)
    if user_id and check_for_username(User(user_id)):
        return User(user_id)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized', 401


@app.route('/home')
@flask_login.login_required
def index():
    """
    Serves the homepage

    :return: index.html
    """
    if not app.TABLE_CREATED:
        init_table_from_config()
        app.TABLE_CREATED = True
    return send_file("/srv/index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    A brain dead, barebones, login page that takes a username and password
    """
    if flask.request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='username' id='username' placeholder='username'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    user = User(flask.request.form['username'], flask.request.form['password'])
    if auth_user(user):
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('/home'))

    return 'Bad login'


@app.route('/logout')
@flask_login.login_required
def logout():
    """
    Logs the user out.
    """
    flask_login.logout_user()
    return flask.redirect(flask.url_for('/login'))


@app.route('/teams-tiles')
@flask_login.login_required
def tile_query():
    """
    Endpoint responsible for serving tile information based on login

    TODO: Create an admin endpoint that allows admins to input the team tiles to load/view
    """
    if not app.TABLE_CREATED:
        init_table_from_config()
        app.TABLE_CREATED = True

    team = flask_login.current_user.get_id()

    if team not in Teams:
        abort(404)
    if team != flask_login.current_user.get_id():
        abort(401)

    return jsonify(get_tiles(team))
