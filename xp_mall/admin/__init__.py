# -*- coding=utf-8 -*-
import os
from datetime import date
from flask import render_template, flash, redirect, url_for, request,\
    current_app, Blueprint, send_from_directory, session
from flask_login import  current_user, login_required
from xp_mall.utils import redirect_back, allowed_file, rename_image, resize_image
from xp_mall.extensions import db

admin_module = Blueprint('admin', __name__)

from xp_mall.admin.goods import *
from xp_mall.admin.category import *
from xp_mall.admin.member import *
from xp_mall.admin.upload import *
from xp_mall.admin.orders import *
# from xp_mall.forms.settings import SettingForm
@admin_module.before_request
@login_required
def is_admin():
    if not current_user.is_admin :
        return redirect(url_for("login"))


@admin_module.route('/', methods=['GET'])
@login_required
def index():
    return  render_template("admin/admin_index.html")

@admin_module.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    '''
    通过后台配置参数
    比如数据库连接参数
    比如支付宝参数
    比如商家信息等等
    '''
    pass
    # form = SettingForm()
    # if form.validate_on_submit():
    #     current_user.name = form.name.data
    #     current_user.blog_title = form.blog_title.data
    #     current_user.blog_sub_title = form.blog_sub_title.data
    #     current_user.about = form.about.data
    #     db.session.commit()
    #     flash('Setting updated.', 'success')
    #     return redirect(url_for('blog.index'))
    #
    # return render_template('admin/settings.html', form=form)



