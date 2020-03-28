# -*- coding=utf-8 -*-

from flask import Blueprint, redirect, url_for


member_module = Blueprint('member', __name__)

from xp_mall.member.center import *
from xp_mall.member.cart import *
from xp_mall.member.buy import *
from xp_mall.member.auth import *
from flask_login import login_required,current_user

@member_module.before_request
@login_required
def is_login():
    # print(current_user.username)
    pass

@member_module.route("/")
def index():
    redirect(url_for("index"))
