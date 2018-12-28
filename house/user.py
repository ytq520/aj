import os
import re

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from utils.functions import get_img_code, user_name
from house.models import User
from utils import status_code
from utils.settings import MEDIA_PATH


user = Blueprint('user', __name__)


@user.route('/register/', methods=['GET'])
def register():
    if request.method == 'GET':
        code = get_img_code()
        return render_template('register.html', code=code)


@user.route('/register/', methods=['POST'])
def my_register():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        img_code = request.form.get('img_code')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 校验完整性
        if not all([mobile, img_code, password, password2]):
            return jsonify(status_code.USER_REGISTER_PARAMS_IS_INVALID)

        # 检验电话是否存在
        phone = User.query.filter(User.phone == mobile).first()
        if phone:
            return jsonify(status_code.USER_REGISTER_PHONE_EXIST)
        # 校验密码和确认密码是否相等
        if not password == password2:
            return jsonify(status_code.USER_REGISTER_PED_EXIST)
        # 校验验证码是否相等
        if not img_code == session.get('code'):
            return jsonify(status_code.USER_REGISTER_CODE_EQUAL)
        # 电话不存在，密码一致，验证码一致，保存在数据库
        my_user = User()
        my_user.phone = mobile
        my_user.pwd_hash = generate_password_hash(password)
        username = user_name()
        my_user.name = username

        my_user.add_update()
        session['user_id'] = my_user.id
        return jsonify({'code': 200, 'msg': '请求成功'})


@user.route('/login/', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@user.route('/login/', methods=['POST'])
def my_login():
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        password = request.form.get('password')
        # 判断电话和密码是否为空
        if not all([mobile, password]):
            return jsonify(status_code.USER_REGISTER_PARAMS_IS_INVALID)
        phone = User.query.filter(User.phone == mobile).first()
        if not phone:
            return jsonify(status_code.USER_LOGIN_PARAMS_IS_REGISTER)
        # 验证密码
        if not check_password_hash(phone.pwd_hash, password):
            return jsonify(status_code.USER_LOGIN_PARAMS_IS_PWD)
        session['user_id'] = phone.id
        return jsonify({'code': 200, 'msg': '请求成功'})


@user.route('/my/', methods=['GET'])
def my():
    return render_template('my.html')


@user.route('/my_get/', methods=['GET'])
def my_get():
    if request.method == 'GET':
        user_id = session.get('user_id')
        my_user = User.query.filter(User.id == user_id).first()
        return jsonify({'code': 200, 'msg': '请求成功', 'img': my_user.avatar, 'name': my_user.name, 'phone': my_user.phone})


@user.route('/profile/', methods=['GET'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')


@user.route('/profile/', methods=['POST'])
def my_profile():
    if request.method == 'POST':
        # 获取头像和用户名
        avatar = request.files.get('avatar')
        # 保存图片
        path = os.path.join(MEDIA_PATH, avatar.filename)
        avatar.save(path)
        # 修改字段，并保存在数据库
        my_id = session['user_id']
        my_user = User.query.filter(User.id == my_id).first()
        my_user.avatar = avatar.filename
        my_user.add_update()
        return redirect(url_for('user.my'))


@user.route('/profile1/', methods=['POST'])
def profile_name():
    if request.method == 'POST':
        name = request.form.get('name')
        my_id = session.get('user_id')
        my_user = User.query.filter(User.id == my_id).first()
        if my_user == name:
            error = '用户名已存在'
            return render_template('profile.html', error=error)
        my_user.name = name
        my_user.add_update()
        return redirect(url_for('user.my'))


# 退出操作
@user.route('/quit/', methods=['GET'])
def logout():
    del session['user_id']
    return redirect(url_for('home.index'))


# 实名实名认证
@user.route('/auth/', methods=['GET'])
def auth():
    if request.method == 'GET':
        my_id = session.get('user_id')
        my_user = User.query.get(my_id)
        if my_user.id_card:
            return render_template('auth.html', my_user=my_user)
        return render_template('auth.html')


# 验证
@user.route('/auth/', methods=['POST'])
def my_auth():
    if request.method == 'POST':
        i_name = request.form.get('real_name')
        i_card = request.form.get('id_card')
        # 校验存在
        if not all([i_name, i_card]):
            return jsonify(status_code.USER_ID_CARD_NAME_IS_ERROR)
        re_str = r'[\u4E00-\u9fa5]+'
        if not re.match(re_str, i_name):
            return jsonify(status_code.USER_I_NAME_IS_ERROR)
        reg = r'^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$'
        if not re.match(reg, i_card):
            return jsonify(status_code.USER_ID_CARD_IS_ERROR)
        my_id = session.get('user_id')
        my_user = User.query.filter(User.id == my_id).first()
        if i_card == my_user.id_card:
            return jsonify(status_code.USER_ID_CARD_IS_EXIST)
        my_user.id_name = i_name
        my_user.id_card = i_card
        my_user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功'})
