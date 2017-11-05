import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="adonese12", db="flask")
    c = conn.cursor()

    return c, conn