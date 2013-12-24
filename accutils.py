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
                          

def user_adaptator(user):
    return {"id": user[0],
            "date_created": user[1],
            "first_name": user[2],
            "last_name": user[3],
            "email": user[4],
            "username": user[5],
            "password": user[6],
            "publication_time": user[7]}

            
