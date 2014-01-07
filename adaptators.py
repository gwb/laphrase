def user_adaptator(user):
    if user is None:
        return None
    return {"id": user[0],
            "date_created": str(user[1]),
            "first_name": user[2],
            "last_name": user[3],
            "email": user[4],
            "username": user[5],
            "password": user[6],
            "publication_time": str(user[7])}

def phrase_adaptator(phrase):
    return {"id": phrase[0],
            "date_created": str(phrase[1]),
            "next_up": phrase[2],
            "content": phrase[3],
            "published": phrase[4],
            "num_views": phrase[5],
            "num_up": phrase[6],
            "num_down": phrase[7]}

def thread_adaptator(thread):
    return {"id": thread[0],
            "date_created": str(thread[1]),
            "name": thread[2],
            "description": thread[3]}

def category_adaptator(category):
    if category is None:
        return None
    return {"id": category[0],
            "date_created": str(category[1]),
            "name": category[2],
            "description": category[3]}

def favinfo_adaptator(favinfo):
    return {"id": favinfo[0],
            "threads_id": favinfo[2],
            "users_id": favinfo[3],
            "threads_name": favinfo[6],
            "threads_description": favinfo[7]}
