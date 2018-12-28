import random

from flask import session


def get_sqlalchemy_uri(DATABASE):
    # mysql+pymysql://root:123456@127.0.0.1:3306/house
    user = DATABASE['USER']
    password = DATABASE['PASSWORD']
    host = DATABASE['HOST']
    port = DATABASE['PORT']
    name = DATABASE['NAME']
    engine = DATABASE['ENGINE']
    driver = DATABASE['DRIVER']
    return '%s+%s://%s:%s@%s:%s/%s' % (engine, driver,
                                       user, password,
                                       host, port, name)


def get_img_code():
    code = ''
    key = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    for i in range(4):
        code += random.choice(key)
    session['code'] = code
    return code


def user_name():
    username = ''
    s = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    for i in range(12):
        username += random.choice(s)
    return username
