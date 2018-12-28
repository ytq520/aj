import os
from datetime import datetime

from flask import Blueprint, render_template, session, request, jsonify

from house.models import User, Area, House, Facility, HouseImage, Order
from utils import status_code
from utils.settings import MEDIA_PATH

home = Blueprint('home', __name__)


@home.route('/newhouse/', methods=['GET'])
def new_house():
    if request.method == 'GET':
        return render_template('newhouse.html')


@home.route('/my_area/', methods=['GET'])
def my_area():
    if request.method == 'GET':

        area = Area.query.all()
        facility = Facility.query.all()

        facility = [i.to_dict() for i in facility]
        area = [i.to_dict() for i in area]

        return jsonify({'code': 200, 'msg': '请求成功', 'area': area, 'facility': facility})


@home.route('/newhouse/', methods=['POST'])
def new_my_house():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        area_id = request.form.get('area_id')
        address = request.form.get('address')
        count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        user_id = session.get('user_id')
        facilitys = request.form.getlist('facility')
        house = House()
        for i in facilitys:
            f = Facility.query.get(int(i))
            house.facilities.append(f)
        house.user_id = user_id
        house.title = title
        house.price = price
        house.area_id = area_id
        house.address = address
        house.room_count = count
        house.acreage = acreage
        house.unit = unit
        house.beds = beds
        house.deposit = deposit
        house.min_days = min_days
        house.max_days = max_days
        house.add_update()

        # 添加中间表
        session['house_id'] = house.id
        return jsonify({'code': 200, 'msg': '请求成功'})


@home.route('/house_img/', methods=['POST'])
def house_img():
    if request.method == 'POST':
        house_id = session.get('house_id')
        # 获取头像和用户名
        icon = request.files.get('house_image')
        # 保存图片
        path = os.path.join(MEDIA_PATH, icon.filename)
        icon.save(path)
        # 判断house数据库里存在index-image
        house = House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url = icon.filename
            house.add_update()
        house_image = HouseImage()
        house_image.house_id = house_id
        house_image.url = icon.filename
        house_image.add_update()
        return jsonify({'code': 200, 'msg': '请求成功', 'img': icon.filename})

    return jsonify({'code': 1001, 'msg': '请求失败'})


@home.route('/myhouse/', methods=['GET'])
def my_house():
    if request.method == 'GET':
        return render_template('myhouse.html')


@home.route('/house_info/', methods=['GET'])
def house_info():
    if request.method == 'GET':
        user = User.query.get(session['user_id'])
        if user.id_card:
            # 已经实名认证
            houses = House.query.filter(House.user_id == user.id)
            house_inf = [house.to_dict() for house in houses]
            return jsonify({'code': 200, 'msg': '请求成功', 'house_info': house_inf})
        else:
            # 没有实名认证
            return jsonify(status_code.USER_ID_CARD_IS_NOT_EXIST)


@home.route('/detail/', methods=['GET'])
def datail():
    if request.method == 'GET':
        return render_template('detail.html')


@home.route('/detail/<int:id>/', methods=['GET'])
def house_detail(id):
    if request.method == 'GET':

        booking = 1  # 查询房间id
        house = House.query.get(id)
        # 查询设施信息
        facility_list = house.facilities
        facility_dict_list = [facility.to_dict() for facility in facility_list]
        # 判断当前房屋信息是否为登录的用户发布，如果是则不显示预定按钮
        if session.get('user_id'):
            if house.user_id == session['user_id']:
                booking = 0

        return jsonify({'code': 200, 'msg': '请求成功', 'house': house.to_full_dict(), 'facility': facility_dict_list, 'booking': booking})


@home.route('/index/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@home.route('/my_index/', methods=['GET'])
def my_index():
    # 获取登录用户信息
    username = ''
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        username = user.name
    # 获取房屋的轮播图
    houses = House.query.filter(House.index_image_url != '').order_by('id')
    houses_info = [house.to_dict() for house in houses]
    return jsonify({'code': 200, 'msg': '请求成功', 'username': username, 'houses_info': houses_info})


@home.route('/search/', methods=['GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')


@home.route('/my_search/', methods=['GET'])
def my_search():
    # 获取区域id，订单开始时间，结束时间
    aid = request.args.get('aid')
    sd = request.args.get('sd')
    ed = request.args.get('ed')
    sk = request.args.get('sk')
    # 获取某个区域的房屋信息
    if aid:
        houses = House.query.filter(House.area_id == aid)
    elif sd and ed:
        sd = datetime.strptime(sd, '%Y-%m-%d')
        ed = datetime.strptime(ed, '%Y-%m-%d')
        houses = House.query.filter(House.max_days >= (ed-sd).days)
    elif not all([aid, sd, ed]):
        houses = House.query.filter()

    # 满足条件时，查询入住时间和退房时间在首页选择时间内的房间，并排除这些房间
    order_list = Order.query.filter(Order.status.in_(['WAIT_ACCEPT', 'WAIT_PAYMENT', 'PAID']))
    # 条件一
    order1 = Order.query.filter(Order.begin_date >= sd, Order.end_date <= ed)
    # 条件2
    order2 = order_list.filter(Order.begin_date < sd, Order.end_date > ed)
    # 条件3
    order3 = order_list.filter(Order.end_date <= sd, Order.end_date >= ed)
    # 条件4
    order4 = order_list.filter(Order.begin_date >= sd, Order.begin_date >= ed)

    house1 = [order.house_id for order in order1]
    house2 = [order.house_id for order in order2]
    house3 = [order.house_id for order in order3]
    house4 = [order.house_id for order in order4]

    # 去重
    not_show_house_id = list(set(house1+house2+house3+house4))
    # 最终展示的房间信息
    houses = houses.filter(House.id.notin_(not_show_house_id))

    if sk == 'new':
        houses = houses.order_by('-id')
    elif sk == 'booking':
        houses = houses.order_by('-order_count')
    elif sk == 'price-inc':
        houses = houses.order_by('price')
    elif sk == 'price-des':
        houses = houses.order_by('-price')
    house_info = [house.to_dict() for house in houses]
    return jsonify({'code': 200, 'msg': '请求成功', 'house_info': house_info})