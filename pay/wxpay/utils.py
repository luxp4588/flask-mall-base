# coding: utf-8
import os,random
import hashlib
try:
    import xmltodict
except:
    os.system("pip install xmltodict")
    import xmltodict
try:
    import qrcode
except:
    os.system("pip install xmltodict")
    import qrcode

import base64
from io import StringIO

def sorted_str(params, key, null=False):
    """ key按照ASCII排序 """
    if null:
        s = '&'.join((str(k) + '=' + str(params[k])) for k in sorted(params))
    else:
        s = '&'.join((str(k) + '=' + str(params[k])) for k in sorted(params) if params[k])
    return s + '&key={}'.format(key)


def sign_md5(s, upper=True):
    """ md5 """
    if upper:
        return hashlib.md5(s.encode("utf-8")).hexdigest().upper()
    else:
        return hashlib.md5(s.encode("utf-8")).hexdigest()


def to_xml(params, cdata=True, encoding='utf-8'):
    """ dict转xml """
    tag = '<{0}><![CDATA[{1}]]></{0}>' if cdata else '<{0}>{1}</{0}>'
    s = ''.join(tag.format(k, v) for k, v in params.items())
    return '<xml>{}</xml>'.format(s).encode(encoding)


def to_dict(content):
    """ xml转dict """
    data = xmltodict.parse(content).get('xml')
    if '#text' in data:
        del data['#text']
    return data


def random_str(length, upper=True):
    """ 随机字符串 """
    sample = 'abcdefghijklmnopqrstuvwxyz'
    sample += sample.upper()
    sample += '1234567890'
    result = ''.join(random.sample(sample, length))
    return result.upper() if upper else result

def make_code(text):
    qr = qrcode.QRCode(
        version=5,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image()
    img_buffer = StringIO.StringIO()
    img.save(img_buffer, 'png')
    res = img_buffer.getvalue()
    img_buffer.close()
    return base64.b64encode(res)