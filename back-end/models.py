from pony.orm import *

db = Database()


class RequestToken(db.Entity):
    user_id = PrimaryKey(str)
    oauth_token = Required(str, nullable=False)
    oauth_token_secret = Required(str, nullable=False)

class User(db.Entity):
    user_nsid = PrimaryKey(str)
    user_id = Required(str,nullable=False)
    username = Required(str,nullable=False)
    fullname = Required(str, nullable =False)
    oauth_token = Required(str, nullable=False)
    oauth_token_secret = Required(str, nullable=False)


def generate_mappings():
    db.bind(provider='sqlite', filename='database.db', create_db=True)
    db.generate_mapping(create_tables=True)
