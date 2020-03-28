# -*- coding=utf-8 -*-
import decimal
from .wechatpay import WechatPay
from .utils import random_str


class Wxpay:
    '''
    创建微信支付对象
    '''

    def __init__(self, app=None):
        if  app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = app.config['WXPAY']
        self.model = WechatPay(config)
        self.notify_url = config['WXPAY_NOTIFY_URL']
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions['wxpay'] = self


    def pay_order(self, order):

        params = {
            'body'            : order.subject,
            'out_trade_no'    : order.order_no,
            'total_fee'       : int(decimal.Decimal(order.total_price)*100),
            'fee_type'        : 'CNY',
            'spbill_create_ip': '127.0.0.1',
            'product_id'      : order.id,
            'notify_url' : self.notify_url,
            'trade_type' : 'NATIVE',
            'nonce_str' : random_str(32, True)
        }
        return self.model.unifiedorder(params)

    def confirm_pay(self, request):
        res, data = self.model.pay_notify(request.data)
        data['total_price'] = int(data['total_fee'])/100
        if res:
            return res, data, self.model.response('ok')
        return True