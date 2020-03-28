# -*- coding=utf-8 -*-

from flask import render_template, redirect, request, url_for, \
    current_app, flash, jsonify, Blueprint
from flask_login import login_user, current_user
from xp_mall.forms.member import LoginForm, RegisterForm
from xp_mall.models.member import Member
from xp_mall.utils import redirect_back
from xp_mall.extensions import db
from datetime import timedelta

AuthManage = Blueprint("auth",__name__)
@AuthManage.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        user = Member.query.filter_by(username=username).first()
        if user:
            if username == user.username and user.validate_password(password):
                login_user(user, remember, duration=timedelta(days=7))
                return redirect_back()
            else:
                flash('Invalid username or password.', 'warning')
        else:
            flash('No account.', 'warning')
    return render_template('member/auth/login.html', form=form)

@AuthManage.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = Member(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return "success"
    elif form.errors:
        return jsonify(form.errors)
    return render_template('member/auth/register.html', form=form, next=request.args.get('next', ''))
