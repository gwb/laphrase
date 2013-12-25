import dbutils

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
    dbutils.bind_content_user(con, phrases_id, users_id)
    return None

def user_adaptator(user):
    return {"id": user[0],
            "date_created": user[1],
            "first_name": user[2],
            "last_name": user[3],
            "email": user[4],
            "username": user[5],
            "password": user[6],
            "publication_time": user[7]}

def get_content_by_userid(con, users_id):
    content_list = dbutils.get_content_by_userid(con, users_id)
    content_list = map(phrase_adaptator, content_list)
    return content_list

def phrase_adaptator(phrase):
    return {"id": phrase[0],
            "date_created": str(phrase[1]),
            "next_up": phrase[2],
            "content": phrase[3],
            "published": phrase[4],
            "num_views": phrase[5],
            "num_up": phrase[6],
            "num_down": phrase[7]}
