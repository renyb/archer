# -*- coding: UTF-8 -*- 

from ldap3 import Server, Connection, ALL, SUBTREE, ServerPool
import pymysql,os
from django.conf import settings
from .models import users

LDAP_SERVER_POOL = ["42.62.10.155"]
#42.62.10.155
LDAP_SERVER_PORT = 389
ADMIN_DN = "cn=Manager,dc=sunlands,dc=com"
ADMIN_PASSWORD = "secret"
#添加部门筛选条件
SEARCH_BASE = "ou=10000,dc=sunlands,dc=com"



def ldap_auth(username,password):

    ldap_server_pool = ServerPool(LDAP_SERVER_POOL)
    conn = Connection(ldap_server_pool, user=ADMIN_DN, password=ADMIN_PASSWORD, check_names=True, lazy=False, raise_exceptions=True)
    conn.open()
    conn.bind()	
    res = conn.search( 
        search_base = SEARCH_BASE,
        search_filter = '(cn=%s@sunlands.com)' %username,
        search_scope = SUBTREE,
        attributes = ['cn','sn','office','name'],
        paged_size = 200
    )

    if res:
        entry = conn.response[0]
        dn = entry['dn']  
        attr_dict = entry['attributes']

        # check password by dn
        try:
            conn2 = Connection(ldap_server_pool, user=dn, password=password, check_names=True, lazy=False, raise_exceptions=False)
            conn2.bind() 
            if conn2.result["description"] == "success":
                #print((True, attr_dict["cn"], attr_dict["name"], attr_dict["office"]))
                #print(attr_dict)
                #print('usrname:',username)

                ##认证成功，同步本地账户
                dbs=getattr(settings, 'DATABASES')
                conn_HOST=dbs['default']['HOST']
                conn_USER=dbs['default']['USER']
                conn_PASSWORD=dbs['default']['PASSWORD']
                conn_NAME=dbs['default']['NAME']
                # 打开数据库连接
                db = pymysql.connect(conn_HOST,conn_USER,conn_PASSWORD,conn_NAME,charset='utf8mb4' )
                # 使用cursor()方法获取操作游标 
                cursor = db.cursor()
            
                # 使用 fetchone() 
                # 使用execute方法执行SQL语句 sql_users表的username字段是唯一索引
                cursor.execute("insert ignore  into sql_users (password,last_login,is_superuser,username,first_name,last_name,email,is_staff,is_active,date_joined,display,role,is_ldapuser) values('', NOW(),0,'{0}','','', '{1}',0,1,now(),'{2}','工程师',1)".format(username,attr_dict["cn"][0],attr_dict["name"][0]))
                # 使用 fetchone() 方法获取一条数据
                db.commit()
                cursor.close()
                # 关闭数据库连接
                db.close()
                
                return True
            else:
                print('auth conn fail')
            
                return False
        except Exception as e:
            print('auth Exception fail')
            return False
    else:
        print('auth  fail')
        return False


if __name__ == "__main__":
    ldap_auth("liuyangxu", "010428")



