import psycopg2
import urlparse
import os
from datetime import datetime

def get_con():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    con = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        host=url.hostname,
        password=url.password,
        port=url.port
        )
    return con

def commit_con(con):
    con.commit()
    return con

def kill_con(con):
    con.close()


def add_user(con, first_name, last_name, email, password):
    cur = con.cursor()
    cur.execute("INSERT INTO users("
                "date_created,"
                "first_name,"
                "last_name,"
                "email,"
                "password) "
                "VALUES(%s,%s,%s,%s,%s) ",
                (datetime.utcnow(),
                first_name,
                last_name,
                email,
                password))
    return con

def dump_users(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    return cur.fetchall()

def get_user_by_email(con, email):
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    return cur.fetchone()
