import os

from flask import Flask

# Khi chạy localhost hãy sử dụng đường dẫn database này
# postgresql://forum:123456@localhost:5432/postgres
def create_app(test_config=None):
    # Tạo và cấu hình ứng dụng
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='',
        DATABASE='postgres://u414qssced6lgj:pad4f7ad587b122467d65d025678d2f2b730b8a6a13410829b5c128714ff9b283@ccba8a0vn4fb2p.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d2huvf9c1v999i',
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