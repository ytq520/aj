from flask import Flask

from house.home import home
from house.models import db
from house.order import order
from house.user import user
from utils.config import Conf
from utils.settings import STATIC_PATH, TEMPLATE_PATH


def create_app():
    app = Flask(__name__, static_folder=STATIC_PATH, template_folder=TEMPLATE_PATH)

    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.register_blueprint(blueprint=home, url_prefix='/home')
    app.register_blueprint(blueprint=order, url_prefix='/order')
    # 加载配置文件
    app.config.from_object(Conf)
    # 初始化
    db.init_app(app)

    return app
