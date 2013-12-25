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
    return render_template("accueil.html")


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        email=request.form['email']
        password=request.form['password']
        login_infos = accutils.check_login(g.con, email, password)
        if login_infos:
            session['user_first_name'] = login_infos['first_name']
            session['user_last_name'] = login_infos['last_name']
            session['user_id'] = login_infos['id']
            session['logged_in'] = True
            return "login successful"
        else:
            return "login failed"
    else:
        return render_template("login.html")
        #return render_template("form_login.html")

    

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
        return render_template("login.html")
        #return render_template("form_create_account.html")
    return render_template("login.html")

@app.route('/add-content', methods=['GET', 'POST'])
def add_content():
    if request.method == 'GET':
        if session["logged_in"]:
            entries = accutils.get_content_by_userid(g.con,
                                                     session["user_id"])
            nextup = [entry for entry in entries if entry['next_up']]
            if len(nextup) > 0:
                nextup = nextup[0]
            else:
                nextup = None
                
            return render_template("add_content.html",
                                   entries=entries,
                                   nextup=nextup)
    else:
        if session['logged_in']:
            entries = accutils.get_content_by_userid(g.con,
                                                     session["user_id"])
            accutils.add_phrase(g.con,
                                request.form['content'],
                                session['user_id'])
        #return redirect(url_for('dump_tables'))
        return redirect(url_for('add_content'))

            

@app.route('/logout')
def logout():
    session.pop('user_first_name', None)
    session.pop('user_last_name', None)
    session.pop('user_id', None)
    session.pop('logged_in', None)
    app.logger.debug('WARNING - You were logged out')
    return redirect(url_for('index'))
                           

@app.route('/dump-tables')
def dump_tables():
    #users = jsonify([map(str, subls) for subls in dbutils.dump_users(g.con)])
    return jsonify([map(str, subls) for subls in dbutils.dump_phrases(g.con)])
    #return jsonify(map(str,dbutils.dump_users(g.con)))

@app.route('/check-session')
def dump_session():
    return jsonify({"user_first_name": session["user_first_name"],
                    "user_last_name": session["user_last_name"],
                    "user_id": session["user_id"]})

@app.route('/check-login')
def dump_login():
    if "logged_in" in session:
        return "Logged in as %s %s" % (session["user_first_name"],
                                       session["user_last_name"])
    else:
        return "Not logged in"


if __name__ == '__main__':
    app.run()
