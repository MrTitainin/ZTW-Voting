import flask
from flask import request, jsonify
import random
from typing import Optional
from DBController import DBController
from constants import *

sessionKeys={}
dbConn=DBController()
server = flask.Flask(__name__)



@server.route('/', methods=['GET','post'])  #test
def home():
    return '''<h1>Voting server</h1><p>hello</p>'''


@server.route('/api/users/register', methods=['POST'])
def apiRegisterUser():
    pass
    

# returns dict:
# 'sessionKey' -> string | None if failed login
# 'electionList' -> list of tuples (electionId, electionName), not provided if fail login
# 'message' -> reason for failed login, only provided on fail login
@server.route('/api/users/login', methods=['POST'])
def apiLoginUser():
    result={}
    result['sessionKey']=None

    data=request.form
    login=data["login"]
    password=data["password"]

    if((login=="") or (password=="")):
        result['message']="Error: No login or password provided. Please specify a login and password."
        return jsonify(result)

    user=dbConn.getUser(login)
    
    if user is None:
        result['message']="User does not exist"
        return jsonify(result)
    
    if((user["login"]!=login) or (user["password"]!=password)):
        result['message']= "wrong login or password"
        return jsonify(result)
    
    result['sessionKey']=generateSessionKey(login)
    result['electionList']=dbConn.getElectionList(login)
    return jsonify(result)     #"Login successfull"


def generateSessionKey(login)->str:
    key=""
    for i in range(0,SESSION_KEY_LENGTH):
        key+=f"{random.randint(0,9)}"
    sessionKeys[key]=login
    return key


def verifyUser(key)->Optional[str]:   #returns login of user
    if(key==""):
        return None
    if key in sessionKeys:
        return sessionKeys[key]
    return None


@server.route('/api/elections/start', methods=['POST'])
def apiElectionStart():
    pass


@server.route('/api/elections/list', methods=['POST'])
def apiGetElectionList():
    pass


@server.route('/api/elections/details', methods=['POST'])
def apiGetElectionDetails():
    pass


@server.route('/api/elections/vote', methods=['POST'])
def apiVote():
    pass


@server.route('/api/elections/end', methods=['POST'])
def apiElectionEnd():
    pass


@server.route('/api/elections/results', methods=['POST'])
def apigetElectionResults():
    pass



if __name__ == '__main__':
    server.run(host=SERVER_ADRESS, port=SERVER_PORT,debug=True)
