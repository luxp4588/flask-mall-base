# -*- coding=utf-8 -*-

from xp_mall.extensions import db, whooshee
from datetime import datetime

@whooshee.register_model("goods_title", "detail")
class Goods(db.Model):
    '''
    商品模型
    goods_id : 商品主键
    goods_title : 商品标题
    goods_subhead : 商品副标题
    category_id : 商品分类
    main_pic : 商品主图
    price : 商品价格
    detail : 商品详情
    '''
    goods_id = db.Column(db.Integer, primary_key=True)
    goods_title = db.Column(db.String(100))
    goods_subhead = db.Column(db.String(100))
    category_id = db.Column(db.Integer, db.ForeignKey('goods_category.id'))
    thumb = db.Column(db.String(100))
    main_pic = db.Column(db.String(500))
    price = db.Column(db.DECIMAL)
    detail = db.Column(db.TEXT)
    create_time = db.Column(db.DateTime)
    category = db.relationship('GoodsCategory')