from flask import Flask, redirect, url_for, session, flash, request, render_template, g
import dbutils
import urlparse
import json

# GLOBAL SETUP - - - - - -

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
app.config["DEBUG"] = True

# END SETUP - - - - - - -


def jsonify(dico):
    return json.JSONEncoder().encode(dico)

@app.before_request
def before_request():
    pass
    #g.con = dbutils.get_con()
    
@app.teardown_request
def teardown_request(exception):
    pass
    #con = getattr(g, 'con', None)
    #if con is not None:
    #    con = dbutils.commit_con(con)
    #    dbutils.kill_con(con)

@app.route('/')
def index():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
