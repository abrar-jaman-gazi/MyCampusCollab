# PyMySQL provides a pure-Python MySQLdb-compatible driver for local development.
try:
    import pymysql
    pymysql.version_info = (2, 2, 1, "final", 0)
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
