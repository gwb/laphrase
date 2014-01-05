import dbutils
from adaptators import user_adaptator, phrase_adaptator, thread_adaptator, category_adaptator, favinfo_adaptator


class DBLogicError(Exception):
    pass

def create_account(con, first_name, last_name, email, password):
    # validate informations
    # TODO
    dbutils.add_user(con, first_name, last_name, email, password)
    return 0


def check_login(con, email, password):
    user = user_adaptator(dbutils.get_user_by_email(con, email))
    if user['password'] == password:
        return user
    else:
        return None
                          
def add_phrase(con, content, users_id):
    phrases_id = dbutils.add_content(con, content)
    threads_id = dbutils.get_thread_by_userid(con, users_id)[0]
    #dbutils.bind_content_user(con, phrases_id, users_id)
    dbutils.bind_threads_phrases(con, threads_id, phrases_id)
    return None


def get_user_by_id(con, id):
    user = user_adaptator(dbutils.get_user_by_id(con, id))
    return user

def get_content_by_userid(con, users_id):
    #content_list = dbutils.get_content_by_userid(con, users_id)
    if not check_exists_thread(con, users_id):
        return []
    threads_id = dbutils.get_thread_by_userid(con, users_id)[0]
    content_list = dbutils.get_content_by_threadid(con, threads_id)
    content_list = map(phrase_adaptator, content_list)
    return content_list
            

def check_exists_thread(con, user_id):
    thread_id = dbutils.get_thread_by_userid(con, user_id)
    return thread_id is not None


def create_thread(con, user_id, thread_name, thread_description):
    # Check if user already has a thread
    has_thread = check_exists_thread(con, user_id)

    if has_thread:
        raise DBLogicError

    else:
        thread_id = dbutils.create_thread(con, thread_name, thread_description)
        dbutils.bind_threads_users(con, thread_id, user_id)
    return thread_id
    

def update_settings(con, user_id, first_name, last_name, username, thread_name, thread_category, thread_description, publication_time):
    # update user specific informations
    dbutils.update_user_by_id(con,
                              user_id,
                              first_name,
                              last_name,
                              username,
                              publication_time)

    if not check_exists_thread(con, user_id):
        # create thread if doesn't exist
        create_thread(con, user_id, thread_name, thread_description)
    else:
        thread_id = dbutils.get_thread_by_userid(con, user_id)[0]
        dbutils.update_thread_by_id(con, thread_id, thread_name, thread_description)
        # update the category
        if thread_category.strip(" "):
            categories_id = dbutils.get_category_by_name(con, thread_category)[0]
            if categories_id:
                dbutils.unbind_threads_categories(con, thread_id)
                dbutils.bind_threads_categories(con, thread_id, categories_id)


def get_thread_by_userid(con, user_id):
    thread = dbutils.get_thread_by_userid(con, user_id)
    if thread is not None:
        return thread_adaptator(thread)
    else:
        return None

def get_thread_by_id(con, threads_id):
    thread = dbutils.get_thread_by_id(con, threads_id)
    if thread is not None:
        return thread_adaptator(thread)
    else:
        return None

def get_user_by_threadid(con, threads_id):
    return user_adaptator(dbutils.get_user_by_threadid(con, threads_id))

def get_all_categories(con):
    return map(category_adaptator, dbutils.get_all_categories(con))

def get_category_by_userid(con, users_id):
    thread = dbutils.get_thread_by_userid(con, users_id)
    if thread is None:
        return ""
    threads_id = thread[0]
    category = dbutils.get_category_by_threadid(con, threads_id)
    if category is not None:
        return category_adaptator(category)
    else:
        return ""

def add_category(con, name):
    categories = map(category_adaptator, dbutils.get_all_categories(con))
    # check if there's already a category with that name
    if len([cat for cat in categories if cat['name'] == name]) == 0:
        dbutils.add_category(con, name)
    return None


def toggle_nextup(con, phrases_id):
    phrase = dbutils.get_phrases_by_id(con, phrases_id)
    if phrase:
        phrase = phrase_adaptator(phrase)
        phrases_id = phrase['id']
        phrases_nextup = phrase['next_up']
        dbutils.update_nextup(con, phrases_id, not phrases_nextup)
    return None

def switch_nextup(con, users_id, phrases_id):
    threads_id = get_thread_by_userid(con, users_id)['id']
    old_nextup = dbutils.get_current_nextup_by_threadid(con, threads_id)
    if old_nextup:
        old_nextup_id = old_nextup[0]
        toggle_nextup(con, old_nextup_id)
    toggle_nextup(con, phrases_id)
    return None


def delete_phrase(con, users_id, phrases_id):
    threads_id = get_thread_by_userid(con, users_id)['id']
    dbutils.unbind_threads_phrases(con, threads_id, phrases_id)
    dbutils.delete_phrases_by_id(con, phrases_id)
    return None

def get_current_nextup_by_threadid(con, threads_id):
    phrase = dbutils.get_current_nextup_by_threadid(con, threads_id)
    if phrase is None:
        return None
    else:
        return phrase_adaptator(phrase)

def add_thread_to_favorites(con, users_id, threads_id):
    # TODO: check existence of thread and user
    if not check_if_exists_favorite(con, users_id, threads_id):
        dbutils.add_thread_to_favorites(con, users_id, threads_id)
    return None

def check_if_exists_favorite(con, users_id, threads_id):
    favorite = dbutils.get_favorite(con, users_id, threads_id)
    return favorite is not None

def get_favorites_info(con, users_id):
    favorites = dbutils.get_favorites_by_userid(con, users_id)
    if not favorites:
        return None
    favinfo_ls = map(favinfo_adaptator, favorites)
    for favinfo in favinfo_ls:
        author = user_adaptator(dbutils.get_user_by_threadid(con, favinfo['threads_id']))
        favinfo['author_first_name'] = author['first_name']
        favinfo['author_last_name'] = author['last_name']
        favinfo['author_username'] = author['username']
    return favinfo_ls
    
