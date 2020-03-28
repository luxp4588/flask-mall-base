# coding: utf-8
import requests

from .utils import to_dict, to_xml, sign_md5, sorted_str

def sign(key, params):
    """ 签名 """
    return sign_md5(sorted_str(params, key))


def request_post(api, data, cert=None, timeout=2):
    data = to_xml(data)
    ret = requests.post(api, data=data, timeout=timeout, cert=cert)
    ret = to_dict(ret.content)
    if ret['return_code'] == 'SUCCESS' and ret.get('result_code') == 'SUCCESS':
        return True, ret
    else:
        return False, ret


class WechatPay:

    def __init__(self, config):
        """
        :param app_id:  appid
        :param mch_id:  商户号
        :param key:  签名key
        :param cert_file:  证书路径
        :param cert_key:  证书key路径
        """
        self.app_id = config['APP_ID']
        self.mch_id = config['MCH_ID']
        self.key = config['KEY']
        self.cert_file = config['WXPAY_CERT_FILE']
        self.cert_key = config['WXPAY_CERT_KEY']
        self.debug = config['DEBUG']

    def common_api(self, api, params):
        """ 通用请求 """
        params.update({
            'appid': self.app_id,
            'mch_id': self.mch_id,
        })
        params['sign'] = sign(self.key, params)
        # 证书
        cert = (self.cert_file, self.cert_key) if self.cert_file and self.cert_key else None
        # 请求结果
        result, ret = request_post(api, params, cert=cert)
        # 检查其他参数
        if result and ret['appid'] == self.app_id and ret['mch_id'] == self.mch_id:
            return True, ret

        return False, ret

    def unifiedorder(self, params):
        """ 统一下单 """

        api = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
        return self.common_api(api, params)

    def orderquery(self, params):
        """ 查询订单 """
        api = 'https://api.mch.weixin.qq.com/pay/orderquery'
        return self.common_api(api, params)

    def closeorder(self, params):
        """ 关闭订单 """
        api = 'https://api.mch.weixin.qq.com/pay/closeorder'
        return self.common_api(api, params)

    def refund(self, params):
        """ 申请退款 """
        api = 'https://api.mch.weixin.qq.com/secapi/pay/refund'
        return self.common_api(api, params)

    def refundquery(self, params):
        """ 查询退款 """
        api = 'https://api.mch.weixin.qq.com/pay/refundquery'
        return self.common_api(api, params)

    def promotion_transfers(self, params):
        """ 企业付款 """
        api = 'https://api.mch.weixin.qq.com/mmpaymkttransfers/promotion/transfers'
        params.update({
            'mch_appid': self.app_id,
            'mchid': self.mch_id,
        })
        params['sign'] = sign(self.key, params)
        result, ret = request_post(api, params, cert=(self.cert_file, self.cert_key))
        # 检查其他参数
        if result and ret['mch_appid'] == self.app_id and ret['mchid'] == self.mch_id:
            return True, ret
        return False, ret

    def pay_notify(self, body):
        """
        支付结果通知，需要校验用户真实充值和订单金额是否一致
        :param body:  request.body
        :return: True, result dict or False, {}
        """
        data = to_dict(body.decode('utf-8'))
        if data['return_code'] == 'SUCCESS' and data['result_code'] == 'SUCCESS' and data['appid'] == self.app_id \
                and data['mch_id'] == self.mch_id:
            check_sign = data.pop('sign')
            if check_sign == sign(self.key, data):
                return True, data

        return False, {}

    def refund_notify(self):
        """ 退款结果通知 """
        # TODO

    def response(self, ok, return_msg=''):
        code = 'SUCCESS' if ok else 'FAIL'
        return to_xml({'return_code': code, 'return_msg': return_msg})
