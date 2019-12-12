from .settings import *

import pymysql

pymysql.install_as_MySQLdb()
 



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'parking',
        'HOST':'',
        'PORT':'3306',
        'USER':'root',
        'PASSWORD':'Quattro!',
    }
}


STATIC_ROOT = '/var/parking/static'
MEIDA_ROOT = '/var/parking/media'


WECHAT = {
    'domain': 'http://parking.metatype.cn',
    'public_account': {
        'appid': 'wxc7594d7d49e0235f',
        #'secret': '04e6251c3b54340f68e693dafe761a0c'
        'secret': 'dc3a49e03e50770d6246ffebc4e840c2'
    },
    # 'miniapp': {
    #     'appid': 'wxc6af1276b4340f68',
    #     'secret': 'fb36b4cddbc2d7c8d6ca8f2797edd004',
    # },
    'pay': {
        'mch_id': '1505199711',
        'pay_secret': '3783cf44953444c79c3d5efbde92b5c0',
        #'pay_secret': 'Applepie1314metatype121928284010', # 微信商户平台(pay.weixin.qq.com) -->账户设置 -->API安全 -->密钥设置，设置完成后把密钥复制到这里
    }
}
