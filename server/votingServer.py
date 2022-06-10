import flask
from flask import request, jsonify
import random
from typing import Optional
from DBController import DBController
from constants import *
from flask_cors import CORS
import requests as req

sessionKeys={'testSessionKey':0}
dbConn=DBController()
server = flask.Flask(__name__)
CORS(server)

# Request return format
# Json dict containing:
#   - 'success' -> result of request - true or false
#   - 'message' -> error message, provided only if 'success' is false
#   - additional request data appropriate for request


# useless, only for connection testing
@server.route('/', methods=['GET','POST'])
def home():
    return '''<h1>Voting server</h1><p>hello</p>'''


@server.route('/api/users/register', methods=['POST'])
def apiRegisterUser():
    pass
    

# arguments in request form:
#   - 'login' -> string, unikalny login uzytkownika
#   - 'password' -> string, haslo uzytkownika
# return on success:
#   - 'sessionKey' -> string, unique key of session
#   - 'admin' -> bool, user is admin
# return on No success:
#   - 'sessionKey' -> None
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

    res=req.post(AUTHENTICATION_SERVER_ADRESS+f':{AUTHENTICATION_SERVER_PORT}'+"/api/authenticate"
        ,data={"login":login,"password":password})
    resData=res.json()
    if(resData['success'] !=True):
        result['success']=False
        result['message']="Error: Authentication error:\n"+res['message']
        return jsonify(result)
    token=resData['sessionKey']

    user=dbConn.getUser(login)
    
    if user is None:
        result['success']=False
        result['message']="Error: User does not exist"
        return jsonify(result)
    
    if((user["FullName"]!=login) or (user["Password"]!=password)):
        result['success']=False
        result['message']= "Error: wrong login or password"
        return jsonify(result)
    
    sessionKeys[token]=user['UserId']
    result['success']=True
    result['sessionKey']=token
    result['admin']=dbConn.isAdmin(user['UserId'])
    result['voter']=dbConn.isVoter(user['UserId'])
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


# arguments in request data:
#   - 'sessionKey' -> string, users unique session key
#   - 'electionName' -> string, name of new elction
#   - 'voteType' -> lower case string of VoteType of new election
#   - 'options' ->list of string, list of available options for election
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
        (data['voteType']!=str(VoteType.SINGLE) and data['voteType']!=str(VoteType.APPROVAL))or 
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
    if data['voteType']==str(VoteType.SINGLE):
        voteType=VoteType.SINGLE
    if data['voteType']==str(VoteType.APPROVAL):
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


# arguments in request data:
#   - 'sessionKey' -> string, users unique session key
# return on success:
#   - 'electionList' -> list of dicts, available elections for user as:
#       - 'electionId' -> int, id of available election
#       - 'electionName' -> string, name of available election
#       - 'electionActive' -> bool, finished or not
#       - 'electionType' -> string, string of voteType
#       - 'electionVotable' -> bool, can user vote
@server.route('/api/elections/list', methods=['POST'])
def apiGetElectionList():
    data=request.json
    result={}
    if not 'sessionKey' in data:
        result['success']=False
        result['message']="Error: Request missing data"
        return jsonify(result)

    if data['sessionKey']=='':
        result['success']=False
        result['message']= "Error: Wrong data"
        return jsonify(result)

    userId=verifyUser(data['sessionKey'])    
    if userId is None:
        result['success']=False
        result['message']="Error: Non existant session"
        return jsonify(result)

    result['electionList']=dbConn.getElectionList(userId)
    if result['electionList'] is None:
        result['electionList']=[]
    
    result['success']=True
    return jsonify(result)


# arguments in request path:
#   - <electionId> -> string of int, id of election
# arguments in request data:
#   - 'sessionKey' -> string, users unique session key
# return on success:
#   - 'electionId' -> int, id of election
#   - 'finished' -> true | false, status of election 
#   - 'electionName' -> string, name of election
#   - voteType -> lower case string of VoteType, election voting type
#   - 'options' -> list of dict, List of options for election as:
#       - 'optionId' -> int, id of available option
#       - 'optionName' -> string, name of available option
@server.route('/api/elections/details/<electionId>', methods=['POST'])
def apiGetElectionDetails(electionId):
    data=request.json
    data['electionId']=int(electionId)
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
    
    electionDetails['success']=True
    return jsonify(electionDetails)


# arguments in request data:
#   - 'sessionKey' -> string, users unique session key
#   - 'electionId' -> int, id of election
#   - optionIds -> list of int, list of setected options
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


# arguments in request data:
#   - 'sessionKey' -> string, users unique session key
#   - 'electionId' -> int, id of election to close
@server.route('/api/elections/end', methods=['PATCH'])
def apiElectionEnd():
    data=request.json
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


# arguments in request path:
#   - <electionId> -> string of int, id of finished election
# arguments in request data:
#   - 'sessionKey' -> string, users unique session key
# return on success:
#   - 'electionId' -> int, id of election
#   - 'finished' -> true, status of election - has to be finished
#   - 'electionName' -> string, name of election
#   - voteType -> lower case string of VoteType, election voting type
#   - 'options' -> list of dict, List of options for election as:
#       - 'optionId' -> int, id of available option
#       - 'optionName' -> string, name of available option
#       - 'voteCount' -> int, total amount of votes for option
@server.route('/api/elections/results/<electionId>', methods=['POST'])
def apiGetElectionResults(electionId):
    data=request.json
    data['electionId']=int(electionId)
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
