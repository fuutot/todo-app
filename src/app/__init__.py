from flask import Flask

def create_app():
    app = Flask(__name__)

    # データベースを初期化
    from . import db
    db.init_app(app)

    # appに機能グループの追加
    from . import auth
    from . import todo
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(todo.bp)
    
    @app.route("/hello")
    def hello():
        return "Hello, World!"
    
    return app