import sqlite3

from flask import current_app, g

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f: # パッケージに関係しているファイルを開く
        db.executescript(f.read().decode('utf8'))


@click.command('init-db') # command line commandの定義
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db) # 応答が終わったらこの関数呼んで
    app.cli.add_command(init_db_command) # flaskから呼べるコマンド追加


def get_db():
    if 'db' not in g: # gはリクエスト毎にユニークなデータを蓄えるオブジェクト
        # コネクションを確立する
        g.db = sqlite3.connect(
            current_app.config['DATABASE'], # current_appはリクエストを処理しているアプリを指すオブジェクト
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # 列に名前でアクセスできるように

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()