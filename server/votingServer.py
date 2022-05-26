import flask
from flask import request, jsonify
import random
from typing import Optional
from DBController import DBController
from constants import *

sessionKeys={'testSessionKey':0}
dbConn=DBController()
server = flask.Flask(__name__)



@server.route('/', methods=['GET','POST'])  #test
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

    user=dbConn.getUser(login)
    
    if user is None:
        result['success']=False
        result['message']="Error: User does not exist"
        return jsonify(result)
    
    if((user["FullName"]!=login) or (user["Password"]!=password)):
        result['success']=False
        result['message']= "Error: wrong login or password"
        return jsonify(result)
    
    result['success']=True
    result['sessionKey']=generateSessionKey(user['UserId'])
    result['electionList']=dbConn.getElectionList(login)
    return jsonify(result)


def generateSessionKey(userId)->str:
    key=""
    for i in range(0,SESSION_KEY_LENGTH):
        key+=f"{random.randint(0,9)}"
    sessionKeys[key]=userId
    return key


def verifyUser(key)->Optional[str]:   #for sessionKey returns UserId
    if(key==""):
        return None
    if key in sessionKeys:
        return sessionKeys[key]
    return None


@server.route('/api/elections/start', methods=['POST'])
def apiElectionStart():
    data=request.json
    result={}
    if (not 'sessionKey' in data or 
        not 'electionName' in data or 
        not 'voteType' in data or 
        not 'options' in data ):
        result['success']=False
        result['message']="Error: Request missing data"
        return jsonify(result)

    if (data['sessionKey']=='' or
        data['electionName']=='' or
        (data['voteType']!='single' and data['voteType']!='approval')or 
           len(data['options'])==0):
        result['success']=False
        result['message']="Error: Wrong data"
        return jsonify(result)
    
    userId=verifyUser(data['sessionKey'])    
    if userId is None:
        result['success']=False
        result['message']="Error: Non existant session"    
        return jsonify(result)
    if not dbConn.isAdmin(userId):
        result['success']=False
        result['message']="No admin rights"
        return jsonify(result)

    for option in data['options']:
        if option =='':
            result['success']=False
            result['message']="Error: Wrong options"
            return jsonify(result)

    voteType=None
    if data['voteType']=='single':
        voteType=VoteType.SINGLE
    if data['voteType']=='approval':
        voteType=VoteType.APPROVAL

    electionId=dbConn.addElection(data['electionName'],voteType)
    if electionId is None:
        result['success']=False
        result['message']="Error: Election insert error"
        return jsonify(result)
    optionIds=dbConn.addOptions(electionId,data['options'])
    if len(optionIds)!= len(data['options']):
        result['success']=False
        result['message']="Error: Option insert error"
        return jsonify(result)
    
    result['success']=True
    return jsonify(result)


@server.route('/api/elections/list', methods=['POST'])
def apiGetElectionList():
    pass


@server.route('/api/elections/details', methods=['POST'])
def apiGetElectionDetails():
    data=request.form
    result={}
    if not 'sessionKey' in data or not 'electionId' in data:
        result['success']=False
        result['message']="Error: Request missing data"
        return jsonify(result)

    if data['sessionKey']=='' or data['electionId']=='':
        result['success']=False
        result['message']= "Error: Wrong data"
        return jsonify(result)

    userId=verifyUser(data['sessionKey'])    
    if userId is None:
        result['success']=False
        result['message']="Error: Non existant session"
        return jsonify(result)

    electionDetails=dbConn.getElectionDetails(data['electionId'])
    if electionDetails is None:
        result['success']=False
        result['message']="Error: Election does not exist"
        return jsonify(result)
    
    return electionDetails


@server.route('/api/elections/vote', methods=['POST'])
def apiVote():
    data=request.json
    result={}
    if (not 'sessionKey' in data or 
        not 'electionId' in data or 
        not 'optionIds' in data):
        result['success']=False
        result['message']="Error: Request missing data"
        return jsonify(result)

    if (data['sessionKey']=='' or
        len(data['optionIds'])==0):
        result['success']=False
        result['message']="Error: Wrong data"
        return jsonify(result)
    
    userId=verifyUser(data['sessionKey'])    
    if userId is None:
        result['success']=False
        result['message']="Error: Non existant session"    
        return jsonify(result)
    if not dbConn.isVoter(userId):
        return "No voting rights"

    if not dbConn.addVote(userId,data['electionId'],data['optionIds']):
        result['success']=False
        result['message']="Error: Option insert error"
        return jsonify(result)
    
    result['success']=True
    return jsonify(result)


@server.route('/api/elections/end', methods=['POST'])
def apiElectionEnd():
    data=request.form
    result={}
    if not 'sessionKey' in data or not 'electionId' in data:
        result['success']=False
        result['message']="Error: Request missing data"
        return jsonify(result)

    if data['sessionKey']=='' or data['electionId']=='':
        result['success']=False
        result['message']="Error: Wrong data"
        return jsonify(result)

    userId=verifyUser(data['sessionKey'])    
    if userId is None:
        result['success']=False
        result['message']="Error: Non existant session"
        return jsonify(result)

    if not dbConn.isAdmin(userId):
        result['success']=False
        result['message']="No admin rights"
        return jsonify(result)

    if not dbConn.endElection(data['electionId']):
        result['success']=False
        result['message']="Error: Can not End election"
        return jsonify(result)
    
    result['success']=True
    return jsonify(result)


@server.route('/api/elections/results', methods=['POST'])
def apiGetElectionResults():
    data=request.form
    result={}
    if not 'sessionKey' in data or not 'electionId' in data:
        result['success']=False
        result['message']="Error: Request missing data"
        return jsonify(result)

    if data['sessionKey']=='' or data['electionId']=='':
        result['success']=False
        result['message']="Error: Wrong data"
        return jsonify(result)

    userId=verifyUser(data['sessionKey'])    
    if userId is None:
        result['success']=False
        result['message']="Error: Non existant session"
        return jsonify(result)

    result=dbConn.getResult(data['electionId'])
    if result is None:
        result={}
        result['success']=False
        result['message']="Error: Results could not be retrieved"
        return jsonify(result)
    result['success']=True
    return jsonify(result)



if __name__ == '__main__':
    server.run(host=SERVER_ADRESS, port=SERVER_PORT,debug=True)
