# -*- coding: UTF-8 -*- 

"""
Django settings for archer project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import pymysql
pymysql.install_as_MySQLdb()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hfusaf2m4ot#7)fkw#di2bu6(cv0@opwmafx5n#6=3d%x^hpl6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sql',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'sql.check_login_middleware.CheckLoginMiddleware',
)

ROOT_URLCONF = 'archer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'sql/static')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'sql.processor.global_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'archer.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = False

# 时间格式化
USE_L10N = False
DATETIME_FORMAT = 'Y-m-d H:i:s'
DATE_FORMAT = 'Y-m-d'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#扩展django admin里users字段用到，指定了sql/models.py里的class users
AUTH_USER_MODEL="sql.users"

###############以下部分需要用户根据自己环境自行修改###################

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

#该项目本身的mysql数据库地址
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'archer',
        'USER': 'root',
        'PASSWORD': 'admin+1234',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}

#inception组件所在的地址
INCEPTION_HOST = '127.0.0.1'
INCEPTION_PORT = '6669'

#查看回滚SQL时候会用到，这里要告诉archer去哪个mysql里读取inception备份的回滚信息和SQL.
#注意这里要和inception组件的inception.conf里的inception_remote_XX部分保持一致.
INCEPTION_REMOTE_BACKUP_HOST='127.0.0.1'
INCEPTION_REMOTE_BACKUP_PORT=3306
INCEPTION_REMOTE_BACKUP_USER='root'
INCEPTION_REMOTE_BACKUP_PASSWORD='admin+1234'

# 账户登录失败锁定时间(秒)
LOCK_TIME_THRESHOLD = 300
# 账户登录失败 几次 锁账户
LOCK_CNT_THRESHOLD = 5

# LDAP
ENABLE_LDAP = False
if ENABLE_LDAP:
    import ldap
    # from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
    from django_auth_ldap.config import LDAPSearch, GroupOfUniqueNamesType
    # if use self signed certificate, Remove AUTH_LDAP_GLOBAL_OPTIONS annotations
    #AUTH_LDAP_GLOBAL_OPTIONS={
    #    ldap.OPT_X_TLS_REQUIRE_CERT: ldap.OPT_X_TLS_NEVER
    #}
    AUTH_LDAP_BIND_DN = "cn=ro,dc=xxx,dc=cn"
    AUTH_LDAP_BIND_PASSWORD = "xxxxxx"
    AUTH_LDAP_SERVER_URI = "ldap://auth.xxx.com"
    AUTH_LDAP_BASEDN = "ou=users,dc=xxx,dc=cn"
    AUTH_LDAP_USER_DN_TEMPLATE = "cn=%(user)s,ou=users,dc=xxx,dc=cn"
    AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=groups,dc=xxx,dc=cn",
        ldap.SCOPE_SUBTREE, "(objectClass=groupOfUniqueNames)"
    )
    AUTH_LDAP_GROUP_TYPE = GroupOfUniqueNamesType()
    AUTH_LDAP_USER_ATTRLIST = ["cn", "sn", "mail"]
    AUTH_LDAP_USER_ATTR_MAP = {
        "username": "cn",
        "display": "sn",
        "email": "mail"
    }

    # AUTH_LDAP_MIRROR_GROUPS = True  # 直接把ldap的组复制到django一份，和AUTH_LDAP_FIND_GROUP_PERMS互斥.用户每次登录会根据ldap来更新数据库的组关系
    # AUTH_LDAP_FIND_GROUP_PERMS = True  # django从ldap的组权限中获取权限,这种方式，django自身不创建组，每次请求都调用ldap
    # AUTH_LDAP_CACHE_GROUPS = True  # 如打开FIND_GROUP_PERMS后，此配置生效，对组关系进行缓存，不用每次请求都调用ldap
    # AUTH_LDAP_GROUP_CACHE_TIMEOUT = 600  # 缓存时间

#开启以下配置注释，可以帮助调试ldap集成
LDAP_LOGS = '/tmp/ldap.log'
DEFAULT_LOGS = '/tmp/default.log'
stamdard_format = '[%(asctime)s][%(threadName)s:%(thread)d]' + \
                  '[task_id:%(name)s][%(filename)s:%(lineno)d] ' + \
                  '[%(levelname)s]- %(message)s'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {  # 详细
            'format': stamdard_format
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': DEFAULT_LOGS,
            'maxBytes': 1024 * 1024 * 100,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'ldap': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LDAP_LOGS,
            'maxBytes': 1024 * 1024 * 100,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'default': {  # default日志，存放于log中
            'handlers': ['default'],
            'level': 'DEBUG',
        },
        'django_auth_ldap': {  # django_auth_ldap模块相关日志打印到console
            'handlers': ['ldap'],
            'level': 'DEBUG',
            'propagate': True,  # 选择关闭继承，不然这个logger继承自默认，日志就会被记录2次了(''一次，自己一次)
        }
    }
}

#是否开启邮件提醒功能：发起SQL上线后会发送邮件提醒审核人审核，执行完毕会发送给DBA. on是开，off是关，配置为其他值均会被archer认为不开启邮件功能
MAIL_ON_OFF='on'

MAIL_REVIEW_SMTP_SERVER='mail.xxx.com'
MAIL_REVIEW_SMTP_PORT=25
MAIL_REVIEW_FROM_ADDR='archer@xxx.com'                                               #发件人，也是登录SMTP server需要提供的用户名
MAIL_REVIEW_FROM_PASSWORD=''                                                         #发件人邮箱密码，如果为空则不需要login SMTP server
MAIL_REVIEW_DBA_ADDR=['zhangsan@abc.com', 'lisi01@abc.com']        #DBA地址，执行完毕会发邮件给DBA，以list形式保存
MAIL_REVIEW_SECURE_ADDR=['zhangsan@abc.com', 'lisi01@abc.com']     #登录失败，等安全相关发送地址
#是否过滤【DROP DATABASE】|【DROP TABLE】|【TRUNCATE PARTITION】|【TRUNCATE TABLE】等高危DDL操作：
#on是开，会首先用正则表达式匹配sqlContent，如果匹配到高危DDL操作，则判断为“自动审核不通过”；off是关，直接将所有的SQL语句提交给inception，对于上述高危DDL操作，只备份元数据
CRITICAL_DDL_ON_OFF='off'

# 在线查询当inception语法树打印失败时的控制，on是允许继续执行，off是禁止执行返回错误，允许执行会导致解析失败的查询表权限验证和脱敏功能失效
CRITICAL_QUERY_ON_OFF = 'on'

# 是否开启动态脱敏查询，由于采取遍历处理结果集的方式，会影响部分查询效率
CRITICAL_DATA_MASKING_ON_OFF = 'on'
