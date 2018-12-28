from utils.functions import get_sqlalchemy_uri
from utils.settings import DATABASE


class Conf():
    # 配置前面要大写
    SQLALCHEMY_DATABASE_URI = get_sqlalchemy_uri(DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SECRET_KEY = 'qwertyuiopa'
