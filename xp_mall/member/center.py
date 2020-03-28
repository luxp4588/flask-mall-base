# -*- coding=utf-8 -*-

from flask import Flask, request, render_template,url_for, \
    jsonify,current_app

from flask_login import current_user

from xp_mall.models.member import Member
from xp_mall.models.goods import Goods
from xp_mall.models.order import Order, OrderGoods, Cart
from xp_mall.extensions import db
from xp_mall.member import  member_module
from xp_mall.forms.order  import SearchForm

@member_module.route("/")
def center_index():

    return render_template("member/member_index.html")

@member_module.route("/cart")
def cart_list():
    cart_list = Cart.query.filter_by(user_id=current_user.user_id).all()
    return render_template("member/cart/cart_list.html", cart_list=cart_list)

@member_module.route("/profile")
def profile():
    cart_list = Cart.query.filter_by(
        Cart.user_id==current_user.user_id).all()
    print(cart_list)
    return ""

@member_module.route('/myorders', defaults={'page': 1})
@member_module.route('/myorders/<int:page>', methods=['GET'])
def manage_orders(page):
    form = SearchForm()
    order_query =  Order.query.filter_by(buyer=current_user.user_id)
    status = request.args.get("status", None)
    if status:
        form.status = status
        order_query = order_query.filter_by(status=status)
    #
    keyword = request.args.get("keyword", None)
    if keyword:
        form.keyword.data = keyword
        order_query = order_query.whooshee_search(keyword)

    if request.args.get("order_type"):
        order_type = request.args.get("order_type")
        form.order_type.data = order_type
        if order_type == "1":
            order_type = Order.create_time.asc()
        elif order_type == "2":
            order_type = Order.create_time.desc()
        elif order_type == "3":
            order_type = Order.price.asc()
        else:
            order_type = Order.create_time.desc()
        order_query = order_query.order_by(order_type)
    print(order_query)
    pagination = order_query.paginate(
         page,current_app.config['XPMALL_MANAGE_GOODS_PER_PAGE'])
    condition = request.query_string.decode()
    return render_template('member/order/order_list.html', page=page,
                           pagination=pagination, form=form,
                           condition=condition)

