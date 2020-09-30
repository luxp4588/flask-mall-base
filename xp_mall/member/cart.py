# -*- coding=utf-8 -*-

from flask import Flask, request, render_template, url_for, current_app, \
     jsonify

from flask_login import current_user
from xp_mall.extensions import db
from xp_mall.utils import queryObjToDicts
from xp_mall.models.order import Cart
from xp_mall.member import member_module

@member_module.route("/cart/<int:goods_id>", methods=['post'])
def add_cart(goods_id):
    message = {"result":False}
    cart_goods = Cart.query.filter(Cart.user_id==current_user.user_id,
                              Cart.goods_id==goods_id).one_or_none()
    if cart_goods:
        cart_goods.amount += 1
    else:
        cart_goods = Cart(
            goods_id = goods_id,
            user_id = current_user.user_id,
            amount = 1)
        db.session.add(cart_goods)
    try:
        db.session.commit()
    except Exception as e:
        current_app.logger.info(e)
    else:
        message = {"result":True}
    return jsonify(message)

@member_module.route("/cart/<int:cart_id>", methods=["delete"])
def delete_cart(cart_id):
    message = {"result": False}
    cart = Cart.query.get(cart_id)
    if cart:
        db.session.delete(cart)
        try:
            db.session.commit()
        except Exception as e:
            current_app.logger.info(e)
        else:
            message = {"result": True}
    return jsonify(message)

@member_module.route("/cart/<int:cart_id>", methods=["put"])
def edit_cart(cart_id):
    message = {"result": False}
    amount = request.form.get("amount", type=int)
    cart = Cart.query.get(cart_id)
    if cart:

        if amount <= 0:
            return jsonify(message)
        else:
            cart.amount = amount
            try:
                db.session.commit()
            except Exception as e:
                current_app.logger.info(e)
            else:
                message = {"result": True}
    return jsonify(message)


@member_module.route("/cart", methods=["get"])
def get_cart():
    cart_list = Cart.query.filter_by(user_id=current_user.user_id).all()
    return jsonify(queryObjToDicts(cart_list,
                                   ['id', 'goods_id', 'user_id', 'amount']))



def empty():
    try:
        user_cart = Cart.query.filter_by(user_id=current_user.user_id).delete(synchronize_session=False)
        db.session.commit()
    except Exception as e:
        print(e)











