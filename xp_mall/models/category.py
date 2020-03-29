# -*- coding=utf-8 -*-

from xp_mall.extensions import db
from datetime import datetime


class GoodsCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    order_id = db.Column(db.Integer)
    parent_id = db.Column(db.Integer, db.ForeignKey('goods_category.id'), default=None)

    goods = db.relationship('Goods', back_populates='category')
    parent = db.relationship('GoodsCategory', back_populates="sub_cates", remote_side=[id])
    sub_cates = db.relationship('GoodsCategory', back_populates="parent", cascade='all, delete-orphan', order_by=order_id)

    def delete(self):
        default_category = GoodsCategory.query.get(1)
        goods_list = self.goods[:]
        for goods in goods_list:
            goods.category = default_category
        db.session.delete(self)
        db.session.commit()

