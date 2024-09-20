import os

from flask import Flask


def create_app(test_config=None):
    # Tạo và cấu hình ứng dụng
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE='postgresql://forum:123456@localhost:5432/postgres',
    )

    if test_config is None:
        # Tải cấu hình cá thể, nếu nó tồn tại thì không kiểm tra
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Tải cấu hình kiểm tra nếu qua điều kiện trên
        app.config.from_mapping(test_config)

    # đảm bảo thư mục này tồn tại
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    return app