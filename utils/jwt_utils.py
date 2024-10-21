# utils/jwt_utils.py
from flask_jwt_extended import get_jwt
from extensions import jwt

blacklist = set()

def is_token_blacklisted(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return jti in blacklist

def blacklist_token():
    jti = get_jwt()['jti']
    blacklist.add(jti)

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return is_token_blacklisted(jwt_header, jwt_payload)
