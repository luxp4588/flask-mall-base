# -*- coding=utf-8 -*-
import os, uuid
from PIL import Image
from flask import Blueprint, request, render_template
from flask import current_app
from flask_login import login_required
from flask import jsonify

from xp_mall.extensions import  csrf
from xp_mall.admin import admin_module


def upload(f):
    # 任何时候，后端都不要相信前端
    # 的数据检测结果，比如上传类型限制，所有必要的检查都须放在
    # 后端进行检测
    message = {"result": "", "error": "", "filepath_list": []}
    if f.content_type not in \
            current_app.config['XPMALL_ALLOWED_UPLOAD_TYPE']:
        print(f.content_type)
        message['result'] = "fail"
        message['error'] = "上传文件类型不对"
        return jsonify(message)

    # 使用新文件名保存
    path, full_path = get_dir()
    new_file_name = create_filename(f.filename)
    filename = os.path.join(path,new_file_name)
    file_path= os.path.join(full_path,
                            new_file_name)
    try:
        f.save(file_path)
    except Exception as e:
        message['result'] = "fail"
        message['error'] = "文件保存到 %s 失败" % file_path
        return message
    # [1:]将.static/相对路径转为/static绝对路径
    message['result'] = filename
    return message


@admin_module.route("/upload_multiple", methods=['post'])
def upload_multiple():
    csrf.protect()
    message = {"result": "", "error": "", "filepath_list": []}
    if request.method == "POST":
        if request.content_length > 300000 * 1000:
            message['result'] = "fail"
            message['error'] = "上传文件太大"
            return jsonify(message)
        file_storage_list = request.files.getlist("file")
        for file_storage in file_storage_list:
            res = upload(file_storage)
            if res['result']!="fail":
                message['filepath_list'].append(res['result'])
        return jsonify(message)


@admin_module.route("/ckeditor", methods=['post'])
def ckeditor_upload():

    csrf.protect()
    message = {
        "uploaded": "0",
        "fileName": "",
        "url"     : "",
        "error"   : {
            "message": ""
        }
    }
    if request.method == "POST":
        file_storage = request.files.get("upload")
        res = upload(file_storage)
        if res['result']!="fail":
            message['fileName'] =  res['result']
            message['url'] = "/uploads/"+res['result']
            message['uploaded'] = "1"
        else:
            message = {"uploaded":"0","error":str(res)}
        return jsonify(message)


@admin_module.route("/ckeditor/browser", methods=['get'])
def ckeditor_browser():
    images = []
    start_pos = len(current_app.config['BASEDIR'])
    for dirpath, dirnames, filenames in os.walk(current_app.config['XPMALL_UPLOAD_PATH']):
        for file in filenames:
            file_info = os.path.splitext(file)
            if file_info[0][-2:] not in ['_s', '_m']:
                images.append(os.path.join(dirpath[start_pos:], file))
    return render_template("upload/browser.html", images=images)


def get_dir():
    '''
    生成文件存放路径
    :return: 存放文件路径
    '''
    from  datetime import date
    # 上传文件存放路径
    base_path = current_app.config['XPMALL_UPLOAD_PATH']
    # 根据上传的日期存放
    d = date.today()
    # 生成存储路径
    path = os.path.join(str(d.year), str(d.month))
    full_path = os.path.join(base_path, path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    return path,full_path

def create_filename(filename):
    '''
    生成随机文件名
    :param filename:
    :return:
    '''
    import  uuid
    ext = os.path.splitext(filename)[1]
    new_file_name = str(uuid.uuid4())+ext
    return new_file_name


def resize_image(image, filename, base_width):
    base_size = current_app.config['XPMALL_IMAGE_SIZE'][base_width]
    filename, ext = os.path.splitext(filename)
    img = Image.open(image).convert("RGB")
    filename += current_app.config['XPMALL_IMAGE_SUFFIX'][base_width] + ext
    upload_path = current_app.config['XPMALL_UPLOAD_PATH']
    file_full_path = os.path.join(upload_path,filename)
    if img.size[0] > base_size:
        w_percent = (base_size / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_size, h_size), Image.ANTIALIAS)
        img.save(file_full_path, optimize=True, quality=85)
    else:
        img.save(file_full_path, optimize=True, quality=85)
    return filename

@admin_module.route("upload_thumb", methods=["post"])
def upload_thumb():
    if request.method == 'POST' and 'upload' in request.files:
        f = request.files.get('upload')
        master_filename = upload(f)['result']
        if master_filename!="fail":
            filename_s = resize_image(f, master_filename, 'small')
            filename_m = resize_image(f, master_filename, 'medium')

            return jsonify({"o":master_filename,
                    "s":filename_s,
                    "m":filename_m
                    })
        else:
            return "", 404
