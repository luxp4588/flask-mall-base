# -*- coding=utf-8 -*-

def create_filter(app):
    @app.template_filter()
    def get_order_status(status):
        status_list = {"0":"未支付", "1":"等待发货", "2":"等待收货", "3":"已收货"}
        return status_list[status]



