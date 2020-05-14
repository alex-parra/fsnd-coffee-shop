import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import re

AUTH0_DOMAIN = 'alexparra.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'fsnd-drinks.alex-parra.com'


class AuthError(Exception):
    '''
    Standardized way to communicate auth failure modes
    '''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    '''
    Get JWT token from header
    '''
    authHeader = request.headers.get('Authorization', None)
    if authHeader is None:
        raise AuthError('Invalid auth header', 401)

    if not re.match('Bearer .*', authHeader, re.IGNORECASE):
        raise AuthError('Invalid auth header', 401)

    (_, token) = authHeader.split(' ')
    return token


def check_permissions(permission, payload):
    '''
    Ensure user has permission
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload
    '''
    if 'permissions' not in payload:
        raise AuthError('Permissions not included in JWT', 400)

    if permission not in payload['permissions']:
        raise AuthError('Permission not found.', 403)

    return True


def verify_decode_jwt(token):
    '''
    Get JWT payload
    @INPUTS
        token: a json web token (string)
    '''
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://"+AUTH0_DOMAIN+"/"
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError("token expired", 401)
        except jwt.JWTClaimsError:
            raise AuthError("invalid claims: check audience and issuer", 401)
        except Exception:
            raise AuthError("invalid header: Unable to parse auth token", 401)

    raise AuthError("invalid header: Unable to find appropriate key", 401)


def requires_auth(permission=''):
    '''
    Auth decorator
    @INPUTS
        permission: string permission (i.e. 'post:drink')
    '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
