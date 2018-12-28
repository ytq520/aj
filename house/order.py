from datetime import datetime

from flask import Blueprint, request, render_template, session, jsonify, redirect, url_for

from house.models import House, Order
from utils import status_code

order = Blueprint('order', __name__)


@order.route('/booking/', methods=['GET'])
def booking():
    if request.method == 'GET':
        return render_template('booking.html')


@order.before_request
def before_req():
    if not session.get('user_id'):
        return redirect(url_for('user.login'))


@order.route('/my_booking/', methods=['POST'])
def my_booking():
    # 创建订单模型
    start_data = datetime.strptime(request.form.get('start_data'), '%Y-%m-%d')
    end_data = datetime.strptime(request.form.get('end_data'), '%Y-%m-%d')

    # 获取当前用户和房屋id
    user_id = session['user_id']
    house_id = request.form.get('house_id')

    # 获取房屋对象
    house = House.query.get(house_id)
    if house.max_days == 0:
        days = (end_data - start_data).days
    elif (end_data - start_data).days > house.max_days:
        return jsonify(status_code.BOOKING_DAYS_IS_GT_MAX_DAYS)
    elif house.max_days != 0:
        days = (end_data - start_data).days
    my_order = Order()
    my_order.house_id = house_id
    my_order.user_id = user_id
    my_order.begin_date = start_data
    my_order.end_date = end_data
    my_order.days = days
    my_order.amount = my_order.days * house.price
    my_order.house_price = house.price
    my_order.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@order.teardown_request
def teardown_req(e):
    return e


@order.route('/orders/', methods=['GET'])
def orders():
    if request.method == 'GET':
        return render_template('orders.html')


@order.route('/my_order/', methods=['GET'])
def my_order():
    # 获取user_id
    orders = Order.query.filter(Order.user_id == session['user_id'])
    order_list = [my_orders.to_dict() for my_orders in orders]
    return jsonify({'code': 200, 'msg': '请求成功', 'order_info': order_list})


@order.route('/my_comment/', methods=['POST'])
def my_comment():
    order_id = request.form.get('orderId')
    comment = request.form.get('comment')
    in_order = Order.query.get(order_id)
    in_order.comment = comment
    in_order.add_update()
    return jsonify({'code': 200, 'msg': '请求成功', 'id': order_id})


@order.route('/accept/', methods=['POST'])
def accept():
    order_id = request.form.get('orderId')
    in_order = Order.query.get(order_id)
    in_order.status = 'WAIT_PAYMENT'
    in_order.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


@order.route('/lorders/', methods=['GET'])
def lorders():
    return render_template('lorders.html')


@order.route('/lorder_info/', methods=['GET'])
def lorder_info():
    # 获取别人对自己房屋的下单信息
    # 先查询自己发布的房屋信息
    houses = House.query.filter(House.user_id == session['user_id'])
    houses_ids = [house.id for house in houses]
    # 查询订单
    orders = Order.query.filter(Order.house_id.in_(houses_ids))
    lorder_info = [order.to_dict() for order in orders]
    return jsonify({'code': 200, 'msg': '请求成功', 'lorder_info': lorder_info})
