import urlparse
import os
import sys
import psycopg2


def get_dburl():
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])
        return url

def get_con(url):
    con = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        host=url.hostname,
        password=url.password,
        port=url.port
        )
    return con

def _init_db(con):
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS users_phrases")
    cur.execute("DROP TABLE IF EXISTS statistics")
    cur.execute("DROP TABLE IF EXISTS users")
    cur.execute("DROP TABLE IF EXISTS phrases")
    cur.execute("DROP TABLE IF EXISTS threads_categories")
    cur.execute("DROP TABLE IF EXISTS categories")
    cur.execute("DROP TABLE IF EXISTS threads")

    cur.execute("CREATE TABLE users ("
                "id SERIAL PRIMARY KEY, "
                "date_created TIMESTAMP, "
                "first_name VARCHAR(50), "
                "last_name VARCHAR(50), "
                "email VARCHAR(50), "
                "username VARCHAR(50), "
                "password VARCHAR(250), "
                "publication_time TIME)"
                )

    cur.execute("CREATE TABLE phrases ("
                "id SERIAL PRIMARY KEY, "
                "date_created TIMESTAMP, "
                "next_up BOOLEAN, "
                "content VARCHAR(300), "
                "published BOOLEAN, "
                "num_views INT, "
                "num_up INT, "
                "num_down INT)"
                )

    cur.execute("CREATE TABLE users_phrases ("
                "id SERIAL PRIMARY KEY, "
                "date_created TIMESTAMP, "
                "users_id INT REFERENCES users(id), "
                "phrases_id INT REFERENCES phrases(id))"
                )

    cur.execute("CREATE TABLE categories ("
                "id SERIAL PRIMARY KEY, "
                "date_created TIMESTAMP, "
                "name VARCHAR(50))")

    cur.execute("CREATE TABLE threads ("
                "id SERIAL PRIMARY KEY, "
                "date_created TIMESTAMP, "
                "name VARCHAR(50))"
                )

    cur.execute("CREATE TABLE threads_categories ("
                "id SERIAL PRIMARY KEY, "
                "date_created TIMESTAMP, "
                "threads_id INT REFERENCES threads(id), "
                "categories_id INT REFERENCES categories(id))"
                )
                
    con.commit()
    return con


def init_con():
    con = None

    try:
        url = get_dburl()
        con = get_con(url)
        con = _init_db(con)

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)
        
    finally:
        if con:
            con.close()
    

if __name__ == "__main__":
        init_con()
