# -*- coding=utf-8 -*-

from flask import render_template,g,request, \
    jsonify,current_app, redirect, flash, url_for
from flask_login import login_required
from xp_mall.admin import admin_module
from xp_mall.extensions import db
from xp_mall.forms.goods import CategoryForm
from xp_mall.models.goods import Goods
from xp_mall.models.category import GoodsCategory



"""
Category 商品分类管理
"""
@admin_module.route('/category/manage/', defaults={"parent_id":0}, methods=["GET"])
@admin_module.route('/category/manage/<int:parent_id>', methods=["GET"])
@login_required
def manage_category(parent_id):
    parent_id = parent_id if parent_id else None
    categories = GoodsCategory.query.filter_by(parent_id=parent_id).order_by(GoodsCategory.order_id).all()
    return render_template('admin/category/category_list.html', categories=categories)

@admin_module.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        # 第一层级目录的父级为""
        # 使用0会发生约束完整性问题
        parent_id = form.parent_id.data if int(form.parent_id.data) else None
        name = form.name.data
        order_id = form.order_id.data
        category = GoodsCategory(name=name, parent_id=parent_id,  order_id=order_id)
        db.session.add(category)
        db.session.commit()
        # flash('Category created.', 'success')
        # return redirect(url_for('.manage_category'))
        return str(category.id)
    elif form.errors:
        return jsonify(form.errors)
    return render_template('admin/category/category_add.html', form=form)


@admin_module.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    message = None
    form = CategoryForm()
    category = GoodsCategory.query.get_or_404(category_id)
    g.category_id = category.id
    g.category_name = category.name
    if form.validate_on_submit():
        try:
            category.name = form.name.data
            category.parent_id = form.parent_id.data
            category.order_id = form.order_id.data
            db.session.commit()
        except Exception as e:
            print(e)
            current_app.logge.debug(e)
            message = e
        else:
            return redirect(url_for("admin.manage_category"))
    else:
        print(form.errors)
        current_app.logger.error("表单数据验证错误")
        message = str(form.errors)

    form.name.data = category.name
    form.parent_id.data = category.parent_id
    form.order_id.data = category.order_id
    return render_template('admin/category/category_edit.html', form=form, message=message)

@admin_module.route('/category/delete', methods=['POST'])
@login_required
def delete_category():
    category_id = int(request.form['cate_id'])
    category = GoodsCategory.query.get_or_404(category_id)
    try:
        category.delete()
    except Exception as e:
        return "fail"
    return "ok"


@admin_module.route('/category', methods=['get'])
@login_required
def get_cate():
    parent_id = request.args.get("parent_id", 0, type=int)
    parent_id = parent_id if parent_id else None
    sub_cates = GoodsCategory.query.filter_by(parent_id=parent_id).all()
    cate_dicts = [(sub_cate.name,sub_cate.id) for sub_cate in sub_cates]
    # print(cate_dicts)
    return jsonify(cate_dicts)
#