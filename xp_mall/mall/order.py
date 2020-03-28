# -*- coding=utf-8 -*-
import math
from flask import Flask, current_app, request, \
    render_template
from xp_mall.mall import mall_module
from xp_mall.models.order import Order
from xp_mall.extensions import db,csrf
from xp_mall.utils import get_pay_obj

@csrf.exempt
@mall_module.route('/pay/<string:payment>/<string:call_type>', methods=['GET', 'POST'])
def pay_confirm(payment, call_type):
    current_app.logger.debug(request)
    pay = get_pay_obj(payment)
    res, order_info, out_html = pay.confirm_pay(request)
    if res:
        if call_type == "return":
            return render_template("member/order/success.html")
        elif call_type == "notify":
            out_trade_no = order_info['out_trade_no']
            order = Order.query.filter_by(order_no=out_trade_no,  status=0).first()
            total_price = order_info['total_price']
            if math.isclose(order.total_price,total_price):
                # status 0:等待付款， 1：已付款，2：已发货，3 已收货
                order.status=1
                db.session.commit()
            return  out_html
    else:
        if call_type == "return":
            return "尚未到账，请稍后刷新页面"
        elif call_type == "notify":
            return out_html
