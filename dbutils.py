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

def dump_phrases(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM phrases")
    return cur.fetchall()

def get_user_by_email(con, email):
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    return cur.fetchone()

def add_content(con, content):
    cur = con.cursor()
    cur.execute("INSERT INTO phrases ("
                "date_created,"
                "next_up,"
                "content,"
                "published,"
                "num_views,"
                "num_up,"
                "num_down) "
                "VALUES(%s,%s,%s,%s,%s,%s,%s) "
                "RETURNING id",
                (datetime.utcnow(),
                 False,
                 content,
                 False,
                 0,
                 0,
                 0))
    phrases_id = cur.fetchone()[0]
    return phrases_id

def bind_content_user(con, phrases_id, users_id):
    cur = con.cursor()
    cur.execute("INSERT INTO users_phrases ("
                "date_created,"
                "users_id,"
                "phrases_id) "
                "VALUES(%s,%s,%s) ",
                (datetime.utcnow(),
                 users_id,
                 phrases_id))
    return None

def get_content_by_userid(con, users_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM "
                "phrases AS p, "
                "users_phrases AS up "
                "WHERE "
                "up.users_id = %s AND "
                "up.phrases_id = p.id ",
                (users_id,))
    return cur.fetchall()
