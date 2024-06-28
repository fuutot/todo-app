import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True) # todo instance_relative_configとは

    app.config.from_mapping( # 構成を設定
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True) # config.pyを利用して構成を更新
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # データベースを初期化
    from . import model
    model.init_app(app)

    # appに機能グループの追加
    from . import auth
    from . import todo
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)
    app.add_url_rule('/', endpoint='index') # indexと/を関連付け
    
    @app.route("/hello")
    def hello():
        return "Hello, World!"
    
    return app