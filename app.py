import os

from flask import Flask

#from tests.test_factory import test_config

# Khi chạy localhost hãy sử dụng đường dẫn database này
# postgresql://forum:123456@localhost:5432/postgres
# Còn đây là khi chạy trên server
# DATABASE='postgres://ubrdvueo3n2sqm:p80ef9be13726152a3edd4e12ee5f9c43ca51204b643745c6a6f45deaeb8d5157@c3gtj1dt5vh48j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d91leg6kh8n84l',
# SECRET_KEY='ba427dae3500189dea8a8072d30c8087a8c605e18e063bc21d5f6540a4f011c2',


# Tạo và cấu hình ứng dụng
app = Flask(__name__, instance_relative_config=True)
test_config = None
app.config.from_mapping(
    SECRET_KEY='ba427dae3500189dea8a8072d30c8087a8c605e18e063bc21d5f6540a4f011c2',
    DATABASE='postgres://ubrdvueo3n2sqm:p80ef9be13726152a3edd4e12ee5f9c43ca51204b643745c6a6f45deaeb8d5157@c3gtj1dt5vh48j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d91leg6kh8n84l',
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


import db

db.init_app(app)

import auth

app.register_blueprint(auth.bp)

import blog

app.register_blueprint(blog.bp)
app.add_url_rule('/', endpoint='index')
