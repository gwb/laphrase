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

def get_user_by_id(con, id):
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id=%s", (id,))
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

def create_thread(con, name, description):
    cur = con.cursor()
    cur.execute("INSERT INTO threads ("
                "date_created,"
                "name,"
                "description) "
                "VALUES(%s,%s,%s) "
                "RETURNING id",
                (datetime.utcnow(),
                 name,
                 description
                 ))
    threads_id = cur.fetchone()[0]
    return threads_id


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

def bind_threads_users(con, threads_id, users_id):
    cur = con.cursor()
    cur.execute("INSERT INTO threads_users ("
                "date_created,"
                "threads_id,"
                "users_id) "
                "VALUES(%s,%s,%s) ",
                (datetime.utcnow(),
                 threads_id,
                 users_id))
    return None

def bind_threads_phrases(con, threads_id, phrases_id):
    cur = con.cursor()
    cur.execute("INSERT INTO threads_phrases ("
                "date_created,"
                "threads_id,"
                "phrases_id) "
                "VALUES(%s,%s,%s) ",
                (datetime.utcnow(),
                 threads_id,
                 phrases_id))
    return None

def bind_threads_categories(con, threads_id, categories_id):
    cur = con.cursor()
    cur.execute("INSERT INTO threads_categories ("
                "date_created,"
                "threads_id,"
                "categories_id) "
                "VALUES(%s,%s,%s) ",
                (datetime.utcnow(),
                 threads_id,
                 categories_id))
    return None

def get_content_by_threadid(con, threads_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM "
                "phrases AS p, "
                "threads_phrases AS tp "
                "WHERE "
                "tp.threads_id = %s AND "
                "tp.phrases_id = p.id ",
                (threads_id,))
    return cur.fetchall()

def get_thread_by_userid(con, users_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM "
                "threads AS t, "
                "threads_users AS tu "
                "WHERE "
                "tu.users_id = %s AND "
                "tu.threads_id = t.id ",
                (users_id,))
    return cur.fetchone()

def get_category_by_threadid(con, threads_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM "
                "categories as c, "
                "threads_categories as tc "
                "WHERE "
                "tc.threads_id = %s AND "
                "tc.categories_id = c.id ",
                (threads_id,))
    return cur.fetchone()

def get_category_by_name(con, name):
    cur = con.cursor()
    cur.execute("SELECT * FROM categories WHERE name=%s", (name,))
    return cur.fetchone()

def update_user_by_id(con, user_id, first_name, last_name, username, publication_time):
    cur = con.cursor()
    cur.execute("UPDATE users "
                "SET "
                "first_name=%s,"
                "last_name=%s,"
                "username=%s,"
                "publication_time=%s "
                "WHERE id=%s",
                (first_name, last_name, username, publication_time, user_id))
    return None


def update_thread_by_id(con, thread_id, thread_name, thread_description):
    cur = con.cursor()
    cur.execute("UPDATE threads "
                "SET "
                "name=%s,"
                "description=%s "
                "WHERE id=%s",
                (thread_name, thread_description, thread_id))
    return None
    

def get_all_categories(con):
    cur = con.cursor()
    cur.execute("SELECT * FROM categories")
    return cur.fetchall()

def add_category(con, name):
    cur = con.cursor()
    cur.execute("INSERT INTO categories ("
                "date_created,"
                "name) "
                "VALUES(%s,%s) "
                "RETURNING id",
                (datetime.utcnow(),
                 name))
    return cur.fetchone()[0]
                
def unbind_threads_categories(con, thread_id):
    cur = con.cursor()
    cur.execute("DELETE FROM threads_categories "
                "WHERE threads_id = %s",
                (thread_id,))
    return None

def unbind_threads_phrases(con, threads_id, phrases_id):
    cur = con.cursor()
    cur.execute("DELETE FROM threads_phrases "
                "WHERE threads_id = %s AND phrases_id = %s",
                (threads_id, phrases_id))
    return None

def delete_phrases_by_id(con, phrases_id):
    cur = con.cursor()
    cur.execute("DELETE FROM phrases "
                "WHERE id = %s",
                (phrases_id,))
    return None


def get_current_nextup_by_threadid(con, threads_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM "
                "phrases AS p, "
                "threads_phrases AS tp "
                "WHERE "
                "tp.threads_id = %s AND "
                "tp.phrases_id = p.id AND "
                "p.next_up = %s",
                (threads_id, True))
    return cur.fetchone()

def get_phrases_by_id(con, phrases_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM phrases WHERE id = %s", (phrases_id,))
    return cur.fetchone()

def update_nextup(con, phrases_id, nextup):
    cur = con.cursor()
    cur.execute("UPDATE phrases "
                "SET "
                "next_up=%s "
                "WHERE id=%s",
                (nextup, phrases_id))
    return None
    
