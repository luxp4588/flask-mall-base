# -*- coding=utf-8 -*-
from datetime import datetime
from xp_mall.extensions import db, whooshee
from xp_mall.models.member import Member


# order_course = db.Table('order_course',
#                        db.Column('order_id', db.ForeignKey("order.id")),
#                        db.Column('order_course_id', db.ForeignKey('order_course.id')))

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    total_price = db.Column(db.FLOAT)
    status = db.Column(db.String(10))
    seller = db.Column(db.String(50))
    buyer = db.Column(db.String(50))
    createTime = db.Column(db.DATETIME)
    payment = db.Column(db.String(30))
    paytime = db.Column(db.DATETIME)

    goods = db.relationship('OrderGoods', back_populates='order', cascade='all, delete-orphan')
    logistics = db.relationship('Logistics', back_populates='order', cascade='all, delete-orphan')

class OrderGoods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    price = db.Column(db.FLOAT)
    order_price = db.Column(db.FLOAT)
    order_active = db.Column(db.Integer, default=None)
    amount = db.Column(db.Integer)
    discount = db.Column(db.FLOAT)

    order = db.relationship('Order', back_populates='goods')




class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.goods_id'))
    amount = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('member.user_id'))

    user = db.relationship('Member')
    goods = db.relationship('Goods')


class Logistics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    receiver = db.Column(db.String(20))
    mobile = db.Column(db.String(30))
    address = db.Column(db.String(100))
    status = db.Column(db.String(100))

    order = db.relationship('Order')







