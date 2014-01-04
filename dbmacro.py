import psycopg2
import json
import datetime
from collections import OrderedDict
from optparse import OptionParser
import sys

def get_con_1():
    con = psycopg2.connect(
        database="laphrasedb",
        user="gwb",
        host="localhost",
        password="",
        port="5432")
    return con

def get_con_2():
    con = psycopg2.connect(
        database="laphrasedb_test",
        user="gwb",
        host="localhost",
        password="",
        port="5432")
    return con

db_tables = OrderedDict()


db_tables["users"] = [("id", "SERIAL PRIMARY KEY"),
                      ("date_created", "TIMESTAMP"),
                      ("first_name", "VARCHAR(50)"),
                      ("last_name", "VARCHAR(50)"),
                      ("email", "VARCHAR(50)"),
                      ("username", "VARCHAR(50)"),
                      ("password", "VARCHAR(250)"),
                      ("publication_time", "TIME")]

db_tables["phrases"] = [("id", "SERIAL PRIMARY KEY"),
                        ("date_created", "TIMESTAMP"),
                        ("next_up", "BOOLEAN"),
                        ("content", "VARCHAR(300)"),
                        ("published", "BOOLEAN"),
                        ("num_views", "INT"),
                        ("num_up", "INT"),
                        ("num_down", "INT")]

db_tables["categories"] = [("id", "SERIAL PRIMARY KEY"),
                           ("date_created", "TIMESTAMP"),
                           ("name", "VARCHAR(50)"),
                           ("description", "VARCHAR(300)")]

db_tables["threads"] = [("id", "SERIAL PRIMARY KEY"),
                        ("date_created", "TIMESTAMP"),
                        ("name", "VARCHAR(50)"),
                        ("description", "VARCHAR(300)")]

db_tables["threads_categories"] = [("id", "SERIAL PRIMARY KEY"),
                                   ("date_created", "TIMESTAMP"),
                                   ("threads_id",
                                    "INT REFERENCES threads(id)"),
                                   ("categories_id",
                                    "INT REFERENCES categories(id)")]

db_tables["threads_users"] = [("id", "SERIAL PRIMARY KEY"),
                              ("date_created", "TIMESTAMP"),
                              ("threads_id", "INT REFERENCES threads(id)"),
                              ("users_id", "INT REFERENCES users(id)")]

db_tables["favorites"] = [("id", "SERIAL PRIMARY KEY"),
                          ("date_created", "TIMESTAMP"),
                          ("threads_id", "INT REFERENCES threads(id)"),
                          ("users_id", "INT REFERENCES users(id)")]

db_tables["threads_phrases"] = [("id", "SERIAL PRIMARY KEY"),
                                ("date_created", "TIMESTAMP"),
                                ("threads_id", "INT REFERENCES threads(id)"),
                                ("phrases_id", "INT REFERENCES phrases(id)")]




def gen_create_query(table_name, fragments):
    query_head = "CREATE TABLE %s (" % table_name
    query_body = ','.join([item[0]+' '+item[1] for item in fragments])
    query_tail = ')'
    return query_head + query_body + query_tail

def drop_all_tables(con, tables):
    for table_name in reversed(tables.keys()):
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS %s" % table_name)
    return None
    

def create_all_tables(con, tables):
    for table_name, query_fragments in tables.items():
        query = gen_create_query(table_name, query_fragments)
        cur = con.cursor()
        cur.execute(query)
    return None



def jsonify(dico):
    return json.JSONEncoder().encode(dico)

def adapt_time(table):
    table = list(table)
    for i in range(len(table)):
        if type(table[i]) is datetime.datetime:
            table[i] = str(table[i])
        if type(table[i]) is datetime.time:
            table[i] = str(table[i])
    table = tuple(table)
    return table

def _dump_tables_all(con, table):
    cur = con.cursor()
    # what's below is very ugly, but there's no other way..
    cur.execute("SELECT * FROM %s" % table)
    return cur.fetchall()

def dump_tables_all(con, tables):
    res = {}
    for table in tables:
        res[table] = _dump_tables_all(con, table)
        if res[table]:
            res[table] = map(adapt_time, res[table])
    return jsonify(res)


def dump_tables_to_file(con, tables, filename):
    res = dump_tables_all(con, tables)
    fout = open(filename, 'w')
    fout.write(res)
    fout.close()
    return None

def gen_load_query(table_name, table_ref):
    n = len(table_ref)
    query_head = "INSERT INTO %s" % table_name
    query_cols = '('+','.join([item[0] for item in table_ref])+') '
    query_vals = 'VALUES(' + ','.join(['%s'] * n) + ') '
    return query_head + query_cols + query_vals
    
def load_table(con, table_values, query, len_table_ref):
    cur = con.cursor()
    try:
        cur.execute(query, table_values)
    except IndexError:
        if len(table_values) < len_table_ref:
            # the table schema has been augmented. Fill in with
            # none values
            print "table schema has been augmented. Filling with None"
            diff = len_table_ref - len(table_values) 
            table_values = tuple(list(table_values) + [None] * diff)
            cur.execute(query, table_values)
    return None

def load_all_tables(con, tables_ref, tables_to_load):
    for table_name in tables_ref:
        #if '_' in table_name:
        #    continue
        query = gen_load_query(table_name, tables_ref[table_name])
        for i in range(len(tables_to_load[table_name])):
            load_table(con,
                       tables_to_load[table_name][i],
                       query,
                       len(tables_ref[table_name]))
    return None


def get_options(argv):
    parser = OptionParser()
    parser.add_option("--reset", action="store_true", dest="reset", default=False,
                      help="Drop all tables and re-create DB schema")
    parser.add_option("--dump", dest="filename_out", default="",
                      help="Dumps content of database into file")
    parser.add_option("--load", dest="filename_in", default="",
                      help="Loads content of file into database")
    (options, args) = parser.parse_args()
    return (options, args)

if __name__ == "__main__":
    options, args = get_options(sys.argv)
    con = get_con_1()
    if options.reset:
        drop_all_tables(con, db_tables)
        create_all_tables(con, db_tables)
    elif options.filename_out != "":
        dump_tables_to_file(con, db_tables.keys(), options.filename_out)
    elif options.filename_in != "":
        fin = open(options.filename_in)
        data = json.load(fin)
        load_all_tables(con, db_tables, data)
    con.commit()
    con.close()

