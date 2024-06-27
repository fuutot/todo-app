import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# auth機能グループの作成
bp = Blueprint('auth', __name__, url_prefix='/auth')

# 登録機能を /auth/register で提供
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST': # formを提出してきたとき
        username = request.form['username'] # dictのように扱える
        password = request.form['password']
        db = get_db()
        error = None

        if not username: # 入力がないとダメ
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute( # 実行
                    "INSERT INTO user (username, password) VALUES (?, ?)", # ?: placeholder
                    (username, generate_password_hash(password)), # databaseにそのままpassword入れない
                )
                db.commit() # 実行のセーブ
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login")) # auth.loginページのurlへ遷移

        flash(error)

    return render_template('auth/register.html') # 表示


# ログイン機能を /auth/login で提供
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone() # 1つのレコード返す

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password): # ハッシュして比べる
            error = 'Incorrect password.'

        if error is None:
            session.clear() # リクエスト間でデータを保持するdict
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# usrに関する情報をとってくる
@bp.before_app_request # どのURLでも view functionが呼ばれる前に呼ばれる
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


# ログアウト機能を auth/logout で提供
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ログインしているかの確認
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view