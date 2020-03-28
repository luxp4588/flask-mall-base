# -*- coding=utf-8 -*-
import logging, os
import traceback
try:
    import alipay
except:
    os.system("pip install alipay-python")

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse
from alipay.aop.api.util.SignatureUtils import verify_with_rsa


"""
支付宝支付对象创建
"""
class Alipay():
    # 对照接口文档，构造请求对象
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        config = app.config['ALIPAY']
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions['alipay'] = self
        alipay_client_config = AlipayClientConfig(config['DEBUG'])
        alipay_client_config.app_id = config['ALIPAY_APP_ID']
        alipay_client_config.app_private_key = open(config['ALIPAY_PRIVATE_KEY_FILE'], "r").read()
        alipay_client_config.app_public_key = open(config['ALIPAY_PUB_KEY_FILE'], "r").read()

        self.alipay_client_config = alipay_client_config
        self.model = AlipayTradePagePayModel()
        self.model.product_code = "FAST_INSTANT_TRADE_PAY"
        self.return_url = config['ALIPAY_RETURN_URL']
        self.notify_url = config['ALIPAY_NOTIFY_URL']
        self.logger = self.get_logger(config['LOG_PATH'])
        self.logger.debug(self.notify_url)
        self.logger.debug(self.return_url)

        self.client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=self.logger)


    def pay_order(self, order):
        self.model.out_trade_no = order.order_no
        self.model.total_amount = order.total_price
        self.model.subject = order.subject
        self.model.body = order.subject

        _request = AlipayTradePagePayRequest(biz_model=self.model)

        _request.notify_url = self.notify_url
        _request.return_url = self.return_url

        # 得到构造的请求，如果http_method是GET，则是一个带完成请求参数的url，如果http_method是POST，则是一段HTML表单片段
        _response = self.client.page_execute(_request, http_method="GET")
        return _response

    def confirm_pay(self, request):
        if request.method == "GET":
            params = request.args.to_dict()
        else:
            params = request.form.to_dict()

        # 弹出签名
        sign = params.pop('sign', None)
        # 弹出签名类型
        params.pop('sign_type', None)
        params_sort = sorted(params.items(), key=lambda e: e[0], reverse=False)  # 取出字典元素按key的字母升序排序形成列表
        message = "&".join(u"{}={}".format(k, v) for k, v in params_sort).encode()  # 将列表转为二进制参数字符串
        self.logger.debug(message)
        try:
            # 验证签名并获取结果
            status = verify_with_rsa(self.alipay_client_config.app_public_key, message,
                                     sign)
        except Exception as e:
            # 验证失败
            return False, {}, "fail"

        if 'trade_status' in params:
            if params['trade_status'] == 'TRADE_SUCCESS':
                params['total_price'] = float(params['total_amount'])
                return True, params, 'success'
            else:
                return False, params, 'success'
        else:
            # 返回验证结果
            return True, False, ''

    def get_logger(self, logpath):
        logging.basicConfig(
            filename=logpath,
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(message)s',
            filemode='a', )
        return logging.getLogger('alipaylog')
