# -*- coding=utf-8 -*-
from flask import request, render_template, current_app, flash, url_for, Response
from flask_login import current_user, login_required
from xp_mall.mall import mall_module
from xp_mall.extensions import db
from xp_mall.models.category import GoodsCategory
from xp_mall.utils import redirect_back, redirect
from xp_mall.models.goods import Goods
from ..utils import get_all_subcate, get_all_parent
import os

@mall_module.route('/')
def index():
    '''
    网站首页
    :return:
    '''
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['XPMALL_GOODS_PER_PAGE']
    pagination = Goods.query.order_by(Goods.create_time.desc()).paginate(page, per_page=per_page)
    goods_list = pagination.items
    categories = GoodsCategory.query.order_by(GoodsCategory.id).first()
    return render_template("mall/index.html", goods_list=goods_list)


@mall_module.route("/search")
def search():
    q = request.args.get('q', '')
    if q == '':
        flash('请输入搜索关键字')
        return redirect_back()
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['XPMALL_GOODS_PER_PAGE']

    pagination = Goods.query.whooshee_search(q).paginate(page, per_page)
    goods = pagination.items
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['XPCMS_ARTICLE_PER_PAGE']
    pagination = Goods.query.filter(Goods.category_id.in_(sub_categories)).order_by(Goods.timestamp.desc()).paginate(
        page, per_page=per_page)
    goods = pagination.items
    return render_template("article/search.html", q=q,
                           goods=goods, pagination=pagination,
                           )


@mall_module.route('/detail/<int:category_id>/<int:goods_id>', methods=['GET', 'POST'])
def show_goods(category_id, goods_id):

    goods = Goods.query.get_or_404(goods_id)

    category_tree = get_all_parent(goods.category_id)  #
    category_tree.sort(key=lambda x: x[1], reverse=False)
    categories = GoodsCategory.query.filter_by(id=category_tree[0][1]).order_by(GoodsCategory.order_id).first()
    print(category_tree)
    return render_template('mall/goods/detail.html', goods=goods,
                           category=categories,category_tree=category_tree,
                           )


@mall_module.route('/category/<int:category_id>/',methods=["GET"])
def category_lists(category_id):
    category_tree = get_all_parent(category_id)  #
    category_tree.sort(key=lambda x: x[1], reverse=False)
    categories = GoodsCategory.query.filter_by(id=category_tree[0][1]).order_by(GoodsCategory.order_id).first()
    sub_categories = get_all_subcate(category_id, [])



    return render_template('goods/lists.html', category=categories,
                           category_tree=category_tree)


