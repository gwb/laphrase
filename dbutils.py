import psycopg2
import urlparse
import os
#from datetime import datetime

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
