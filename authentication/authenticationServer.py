import flask
from flask import request, jsonify
import random
from typing import Optional
from constants import *
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta

sessionKeys={'testSessionKey':0}
server = flask.Flask(__name__)
CORS(server)

users=[
    {'login':'aaa', 'password':'aaa'},
    {'login':'bbb', 'password':'bbb'},
    {'login':'ccc', 'password':'ccc'}
]


# useless, only for connection testing
@server.route('/', methods=['GET','POST'])
def home():
    return '''<h1>Authentication server</h1><p>hello</p>'''

@server.route('/', defaults={'path': ''}, methods=['OPTIONS'])
@server.route('/<path:path>', methods=['OPTION'])
def corsOptionHandling():
    return ''

@server.route('/api/users/register', methods=['POST'])
def apiRegisterUser():
    pass
    

@server.route('/api/authenticate', methods=['POST'])
def apiLoginUser():
    result={}
    result['sessionKey']=None

    data=request.form
    print(data)
    if not 'login' in data or not 'password' in data:
        result['success']=False
        result['message']="Error: No login or password provided. Please specify a login and password."
        return jsonify(result)

    login=data["login"]
    password=data["password"]

    if((login=="") or (password=="")):
        result['success']=False
        result['message']="Error: Login or Password empty. Please specify a login and password."
        return jsonify(result)

    user=None
    if {'login':login,'password':password} in users:
        user=generateSessionKey(login)
    
    if user is None:
        result['success']=False
        result['message']="Error: Wrong login or password"
        return jsonify(result)
    
    result['success']=True
    result['sessionKey']=user
    return jsonify(result)


def generateSessionKey(userId)->str:
    token = jwt.encode({
        'sub': userId,
        'iat':datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=30)},
        SECRET_KEY,algorithm="HS256")
    sessionKeys[token]=userId
    #print(jwt.decode(token, SECRET_KEY,algorithms=["HS256"]))
    return token


def verifyUser(key)->Optional[str]:   #for sessionKey returns UserId
    if(key==""):
        return None
    if key in sessionKeys:
        return sessionKeys[key]
    return None




if __name__ == '__main__':
    server.run(host=SERVER_ADRESS, port=SERVER_PORT,debug=True)
