# -*- coding: utf-8 -*-
import json
from flask import request, render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from ..forms.member import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
from ..models.member import Member
from xp_mall.utils import redirect_back
from xp_mall.extensions import db
from xp_mall.utils import generate_token, validate_token
from xp_mall.member import member_module

@member_module.route('/logout')
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect_back()

