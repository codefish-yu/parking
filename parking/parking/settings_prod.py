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
MEIDA_ROOT = '/var/whale/media'
