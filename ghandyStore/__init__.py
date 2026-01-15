import pymysql

# Tell Django to use PyMySQL instead of mysqlclient
pymysql.install_as_MySQLdb()
