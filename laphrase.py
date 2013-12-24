from flask import Flask, redirect, url_for, session, flash, request, render_template, g
import dbutils
import accutils
import urlparse
import json

# GLOBAL SETUP - - - - - -

app = Flask(__name__)
app.secret_key = '\x14Z\x07\xc6Zv\xf6\xd1\xadu\x05\x08\xf7mgS\xdbF5;\xacwSb'
app.config["DEBUG"] = True

# END SETUP - - - - - - -


def jsonify(dico):
    return json.JSONEncoder().encode(dico)

@app.before_request
def before_request():
    g.con = dbutils.get_con()
    
@app.teardown_request
def teardown_request(exception):
    con = getattr(g, 'con', None)
    if con is not None:
        con = dbutils.commit_con(con)
        dbutils.kill_con(con)

@app.route('/')
def index():
    return 'Hello World!'


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']
        login_infos = accutils.check_login(g.con, email, password)
        if login_infos:
            session['user_first_name'] = login_infos['first_name']
            session['user_last_name'] = login_infos['last_name']
            session['user_id'] = login_infos['id']
            return "login successful"
        else:
            return "login failed"
    else:
        return render_template("form_login.html")
    

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        try:
            accutils.create_account(g.con,
                                    request.form['first_name'],
                                    request.form['last_name'],
                                    request.form['email'],
                                    request.form['password'])
        except IOError:
            app.logger.debug("ERROR - couldn't add account")                    
    else:
        return render_template("form_create_account.html")
    return "create account page"

@app.route('/dump-tables')
def dump_tables():
    return jsonify([map(str, subls) for subls in dbutils.dump_users(g.con)])
    #return jsonify(map(str,dbutils.dump_users(g.con)))

@app.route('/check-session')
def dump_session():
    return jsonify({"user_first_name": session["user_first_name"],
                    "user_last_name": session["user_last_name"],
                    "user_id": session["user_id"]})




if __name__ == '__main__':
    app.run()
