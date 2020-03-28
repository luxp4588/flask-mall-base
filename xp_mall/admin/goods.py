# -*- coding=utf-8 -*-

from flask import render_template, request, current_app, flash
from flask import jsonify, json
from flask_login import login_required

from xp_mall.extensions import db
from xp_mall.utils import redirect_back
from xp_mall.admin import admin_module
from xp_mall.models.goods import Goods
from xp_mall.models.category import GoodsCategory

from xp_mall.forms.goods import GoodsForm, SearchForm

@admin_module.route('/manage/goods', defaults={'page': 1})
@admin_module.route('/manage/goods/<int:page>', methods=['GET'])
@login_required
def manage_goods(page):
    form = SearchForm()
    goods_query =  Goods.query
    if request.args.get("category_id"):
        category_id = request.args.get("category_id")
        form.category_id.data = category_id
        goods_query = goods_query.filter_by(category_id=category_id)
    #
    if request.args.get("keyword"):
        keyword = request.args.get("keyword")
        form.keyword.data = keyword
        goods_query = goods_query.whooshee_search(keyword)

    if request.args.get("order_type"):
        order_type = request.args.get("order_type")
        form.order_type.data = order_type
        if order_type == "1":
            order_type = Goods.create_time.asc()
        elif order_type == "2":
            order_type = Goods.create_time.desc()
        elif order_type == "3":
            order_type = Goods.price.asc()
        else:
            order_type = Goods.create_time.desc()
        goods_query = goods_query.order_by(order_type)
    print(goods_query)
    pagination = goods_query.paginate(
         page,current_app.config['XPMALL_MANAGE_GOODS_PER_PAGE'])
    condition = request.query_string.decode()
    return render_template('admin/goods/goods_list.html', page=page,
                           pagination=pagination, form=form,
                           condition=condition)


@admin_module.route('/manage/goods/new', methods=['GET', 'POST'])
@login_required
def new_goods():
    form = GoodsForm()
    if form.validate_on_submit():
        title = form.title.data
        thumb = form.thumb.data
        main_pic = form.main_pic.data
        body = form.body.data
        category_id = form.category.data
        price = form.price.data
        goods = Goods(goods_title=title,
                      thumb = thumb,
                      main_pic = main_pic,
                      category_id=category_id,
                      detail=body,
                      price=price)
        try:
            db.session.add(goods)
            db.session.commit()
        except Exception as e:
            print(e)
            # current_app.logger.error(e)
        return jsonify({"goods_id":goods.goods_id})
    elif request.method == 'POST' and form.errors:
        return jsonify(form.errors)

    return render_template('admin/goods/goods_add.html', form=form)


@admin_module.route('/goods/<int:goods_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_goods(goods_id):
    form = GoodsForm()
    goods = Goods.query.get_or_404(goods_id)
    if form.validate_on_submit():
        goods.goods_title = form.title.data
        goods.detail  = form.body.data
        goods.thumb = form.thumb.data
        goods.main_pic = form.main_pic.data
        goods.category_id = form.category.data
        goods.price = form.price.data
        db.session.commit()
    elif form.errors:
        print(form.errors)
    form.title.data = goods.goods_title
    form.body.data = goods.detail
    thumbs = goods.main_pic
    form.category.data = goods.category_id
    form.price.data = goods.price
    current_cate = goods.category.name
    return render_template('admin/goods/goods_edit.html',
                           form=form, thumbs=thumbs,
                           current_cate=current_cate)


@admin_module.route('/goods/delete/<int:goods_id>', methods=['POST'])
@login_required
def delete_goods(goods_id):
    goods = Goods.query.get_or_404(goods_id)
    db.session.delete(goods)
    db.session.commit()
    return "ok"

@admin_module.route("/goods/batch_delete", methods=['POST'])
@login_required
def batch_delete_goods():
    '''
    批量删除商品
    :return:
    '''
    ids = request.form.getlist("checkID[]")
    Goods.query.filter(Goods.goods_id.in_(ids)).delete(synchronize_session="fetch")
    db.session.commit()
    return "ok"


