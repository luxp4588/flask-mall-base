# -*- coding: utf-8 -*-

import logging
import os
import re
from logging.handlers import  RotatingFileHandler

import click
from flask import Flask, request, \
    send_from_directory, redirect, url_for
from flask_login import current_user, login_manager
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError


from xp_mall.admin import admin_module
from xp_mall.mall import mall_module
from xp_mall.member import member_module


from xp_mall.models.category import GoodsCategory
from xp_mall.models.member import Guest

from xp_mall.extensions import  db, login_manager, csrf, ckeditor, moment, toolbar, migrate
from xp_mall.extensions import whooshee, dropzone, alipay, wxpay
from xp_mall.settings import config
from xp_mall.login_manage import AuthManage
from xp_mall.filters import create_filter


def create_app(config_name=None):
    '''
    app工厂函数
    :param config_name:
    :return: app - wsgi协议中的application
    '''
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask(__name__)
    app.config['secret_key'] = os.getenv("SECRET_KEY")
    app.config.from_object(config[config_name])

    @app.route('/')
    def index():
        '''
        网站默认页面为店铺商品列表页面
        :return:
        '''
        return redirect(url_for("mall.index"))

    @app.route('/uploads/<path:filename>')
    def get_image(filename):
        return send_from_directory(app.config['XPMALL_UPLOAD_PATH'], filename)

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_shell_context(app)
    register_request_handlers(app)
    login_manager.anonymous_user = Guest
    create_filter(app)
    return app


def register_logging(app):
    '''
    运行日志
    :param app:
    :return:
    '''

    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.method = request.method
            record.url = request.url
            record.remote_addr = request.remote_addr
            record.data = request.get_data(as_text=True)


            return super(RequestFormatter, self).format(record)

    # 请求日志
    request_formatter = RequestFormatter(
        '【%(levelname)s - %(asctime)s】%(method)s :: %(remote_addr)s - %(url)s - [ %(data)s]'
    )
    if not os.path.exists(app.config['LOG_FILES_PATH']):
        os.makedirs(app.config['LOG_FILES_PATH'], 0o755, True)
    log_file_path = os.path.join(app.config['LOG_FILES_PATH'], 'app.debug.log')

    request_file_handler = RotatingFileHandler(log_file_path,
                                           maxBytes=10 * 1024 * 1024, backupCount=10)
    request_file_handler.setFormatter(request_formatter)
    request_file_handler.setLevel(logging.DEBUG)

    if app.debug:
        app.logger.addHandler(request_file_handler)
#
#
def register_extensions(app):
    '''
    扩展初始化
    :param app:
    :return:
    '''
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    toolbar.init_app(app)
    migrate.init_app(app, db)
    whooshee.init_app(app)
    dropzone.init_app(app)
    # 配置支付宝后才会启用支付接口对象
    if app.config['ALIPAY']['ALIPAY_APP_ID']:
        alipay.init_app(app)

    # 配置微信支付后才会启用微信支付对象
    if app.config['WXPAY']['APP_ID']:
        wxpay.init_app(app)
#
#
def register_blueprints(app):
    """
    admin_module 后台管理模块
    member_module 会员模块
    mall_module 商城模块
    :param app:
    :return:
    """
    app.register_blueprint(AuthManage, url_prefix='/')
    app.register_blueprint(admin_module, url_prefix='/admin')
    app.register_blueprint(member_module, url_prefix='/member')
    app.register_blueprint(mall_module, url_prefix='/mall')
#
#
#
def register_shell_context(app):
    '''
    flask shell环境变量自动导入
    :param app:
    :return:
    '''
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)
#

#
def register_commands(app):
    '''
    flask 自定义命令
    :param app:
    :return:
    '''
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """创建数据库"""
        if drop:
            click.confirm('确认要删除原来的数据库吗?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to login.')
    def createadmin(username, password):
        '''
        创建管理员
        :param username:
        :param password:
        :return:
        '''
        from xp_mall.models.member import Member
        click.echo('创建店铺管理员')
        admin = Member(
            username=username,
            is_approve=1,
            is_admin=True
        )
        admin.set_password(password)
        try:
            db.session.add(admin)
            db.session.commit()
        except Exception as e:
            print(e)
        click.echo('Done.')
#
#
#
def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        for q in get_debug_queries():
            if q.duration >= app.config['XPMALL_SLOW_QUERY_THRESHOLD']:
                app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response



if __name__=="__main__":
   app =  create_app("development")
   app.run(host="0.0.0.0", port=5000, debug=True)