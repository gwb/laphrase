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
    categories = accutils.get_all_categories(g.con)
    categories1 = categories[:3]
    categories2 = categories[3:]
    return render_template("accueil.html",
                           categories1 = categories1,
                           categories2 = categories2)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/process-login', methods=['POST'])
def process_login():
    email=request.form['email']
    password=request.form['password']
    login_infos = accutils.check_login(g.con, email, password)
    if login_infos:
        session['user_first_name'] = login_infos['first_name']
        session['user_last_name'] = login_infos['last_name']
        session['user_id'] = login_infos['id']
        session['logged_in'] = True
        return redirect(url_for('my_account'))
    else:
        return "login failed"


@app.route('/process-create-account', methods=['GET', 'POST'])
def process_create_account():
    try:
        accutils.create_account(g.con,
                                request.form['first_name'],
                                request.form['last_name'],
                                request.form['email'],
                                request.form['password'])
    except IOError:
        app.logger.debug("ERROR - couldn't add account")
        return "Couldn't create account"
    return redirect(url_for('my_account'))

@app.route('/add-content', methods=['POST'])
def add_content():
    if session['logged_in']:
        if not accutils.check_exists_thread(g.con, session['user_id']):
            return redirect(url_for('my_account'))
        else:
            accutils.add_phrase(g.con,
                                request.form['content'],
                                session['user_id'])
            return redirect(url_for('my_account', display="thread"))

            

@app.route('/my-account')
def my_account():
    if not "logged_in" in session:
        return redirect(url_for('login'))
    else:
        entries = accutils.get_content_by_userid(g.con,
                                                 session["user_id"])
        nextup = [entry for entry in entries if entry['next_up']]
        if len(nextup) > 0:
            nextup = nextup[0]
        else:
            nextup = None

        display = {"thread": 'display:none',
                   "favorites": ''}

        if 'display' in request.args:
            if request.args['display'] == 'favorites':
                display = {"thread": 'display:none',
                           "favorites": ''}
            else:
                display = {"thread": '',
                           "favorites": 'display:none',}

        user = accutils.get_user_by_id(g.con, session["user_id"])

        thread = accutils.get_thread_by_userid(g.con, session["user_id"])

        category = accutils.get_category_by_userid(g.con, session["user_id"])

        favorites_info = accutils.get_favorites_info(g.con, session["user_id"])

        if category:
            category = category["name"]

        if user["publication_time"] not in (None, 'None'):
            user["hour"], user["minutes"] = user["publication_time"].split(":")[:2]

        
        return render_template('user_account.html',
                               entries=entries,
                               nextup=nextup,
                               display=display,
                               user=user,
                               thread=thread,
                               category=category,
                               favorites=favorites_info)


@app.route('/contenu')
def contenu():
    if not "logged_in" in session:
        return redirect(url_for('login'))
    return redirect(url_for('index')) #render_template('contenu.html')

@app.route('/contenu/<int:thread_id>')
def contenu_thread(thread_id):
    if not "logged_in" in session:
        return redirect(url_for('login'))
    try:
        auteur = accutils.get_user_by_threadid(g.con, thread_id)
        threads_name = accutils.get_thread_by_id(g.con, thread_id)['name']
    except TypeError:
        return redirect(url_for('login'))
    phrase_nextup = accutils.get_current_nextup_by_threadid(g.con, thread_id)

    is_fav = accutils.check_if_exists_favorite(g.con, session['user_id'], thread_id)

    return render_template('contenu.html',
                           auteur = auteur,
                           nextup = phrase_nextup,
                           threads_id = thread_id,
                           threads_name = threads_name,
                           is_fav = is_fav
                           )
    
@app.route('/category')
def category_redir():
    return redirect(url_for('index'))

@app.route('/category/<int:category_id>')
def category_list(category_id):
    if not accutils.check_if_exists_category(g.con, category_id):
        return redirect(url_for('index'))
    else:
        category = accutils.get_category_by_id(g.con, category_id)
        threads = accutils.get_threads_by_categoryid(g.con, category_id)
        for thread in threads:
            thread["is_fav"] = accutils.check_if_exists_favorite(g.con, session['user_id'], thread["id"])
        return render_template('categorie.html',
                               category=category,
                               threads=threads)
    



@app.route('/settings', methods=['POST'])
def settings():
    if not "logged_in" in session:
        return redirect(url_for('login'))
    else:
        publication_time = "%s:%s"%(request.form["hour"],
                                    request.form["minutes"])
        accutils.update_settings(g.con,
                                 session['user_id'],
                                 request.form["first_name"],
                                 request.form["last_name"],
                                 request.form["user_name"],
                                 request.form["thread_name"],
                                 request.form["thread_category"],
                                 request.form["thread_description"],
                                 publication_time)
        return redirect(url_for('my_account'))


@app.route('/add-category', methods=['GET','POST'])
def add_category():
    if request.method == 'GET':
        categories = accutils.get_all_categories(g.con)
        return render_template("add_category.html",
                               categories=categories)
    else:
        accutils.add_category(g.con, request.form['name'])
        return redirect(url_for("add_category"))
                              

@app.route('/category')
def category():
    return render_template("categorie.html")

@app.route('/nextup')
def nextup():
    return(redirect(url_for('my_account')))

@app.route('/nextup/<int:phrases_id>')
def switch_nextup(phrases_id):
    # TODO: check that user is the right one
    app.logger.debug('WARNING - phrases_id = %s' % phrases_id)
    accutils.switch_nextup(g.con, session['user_id'], phrases_id)
    return redirect(url_for('my_account'))

@app.route('/add-favorite')
def add_favorite():
    return redirect(url_for('index'))

@app.route('/add-favorite/<int:thread_id>')
def do_add_favorite(thread_id):
    if "logged_in" not in session:
        return redirect(url_for('login'))
    is_fav = accutils.check_if_exists_favorite(g.con, session['user_id'], thread_id)
    if not is_fav:
        accutils.add_thread_to_favorites(g.con,
                                         session['user_id'],
                                         thread_id)
    else:
        # check that the user logged in is the one to which the
        # favorite belongs
        accutils.remove_thread_from_favorites(g.con,
                                              session["user_id"],
                                              thread_id)
    if 'next' in request.args:
        return redirect(request.args['next'])
    else:
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user_first_name', None)
    session.pop('user_last_name', None)
    session.pop('user_id', None)
    session.pop('logged_in', None)
    app.logger.debug('WARNING - You were logged out')
    return redirect(url_for('index'))
                           

@app.route('/delete')
def delete():
    return redirect(url_for('my_accout'))

@app.route('/delete/<int:phrases_id>')
def delete_phrase(phrases_id):
    # TODO check that user is the right one
    accutils.delete_phrase(g.con, session['user_id'], phrases_id)
    return redirect(url_for('my_account'))

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
