# -*- coding=utf-8 -*-
from datetime import datetime
from flask import  current_app
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from xp_mall.extensions import db


class Member(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(50))
    reg_date = db.Column(db.DateTime)
    reg_ip = db.Column(db.String(20))
    reg_sex = db.Column(db.String(2))
    last_login_ip = db.Column(db.String(20))
    last_login_time = db.Column(db.DateTime)
    mobile = db.Column(db.String(12))
    is_approve = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.user_id)

class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False



class OAuth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    authorized_from = db.Column(db.String(30))
    authorized = db.Column(db.String(30))
    authorized_info = db.Column(db.String(500))
    bind_to_username = db.Column(db.String(30))
    bind_date = db.Column(db.DateTime)


