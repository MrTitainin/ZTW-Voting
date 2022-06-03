from typing import Optional
import sqlalchemy as sqla
from constants import *
import os

class DBController():
    def __init__(self):
        if os.path.exists(DATABASE_FILE_PATH+DATABASE_FILE_NAME):
            os.remove(DATABASE_FILE_PATH+DATABASE_FILE_NAME)
        if os.path.exists(DATABASE_FILE_PATH+DATABASE_FILE_NAME+'-journal'):
            os.remove(DATABASE_FILE_PATH+DATABASE_FILE_NAME+'-journal')
        self.engine = sqla.create_engine('sqlite:///'+DATABASE_FILE_PATH+DATABASE_FILE_NAME)
        conn = self.engine.connect()
        metadata = sqla.MetaData()

        self.users = sqla.Table('User', metadata,
            sqla.Column('UserId', sqla.Integer,primary_key=True),
            sqla.Column('FullName', sqla.String(255),unique=True),
            sqla.Column('Password', sqla.String(255), nullable=False),
            sqla.Column('AdministrativeRight', sqla.Boolean, default=False),
            sqla.Column('AllowedToVote', sqla.Boolean, default=True)
        )

        self.elections = sqla.Table('Election', metadata,
            sqla.Column('ElectionId', sqla.Integer,primary_key=True),
            sqla.Column('Name', sqla.String(255),nullable=False),
            sqla.Column('Finished', sqla.Boolean, default=False),
            sqla.Column('VoteType', sqla.Enum(VoteType), default=VoteType.SINGLE)
        )

        self.options= sqla.Table('Option', metadata,
            sqla.Column('OptionId', sqla.Integer,primary_key=True),
            sqla.Column('ElectionId',sqla.ForeignKey('Election.ElectionId'),primary_key=True),
            sqla.Column('Name', sqla.String(255),nullable=False)
        )

        self.votes=sqla.Table('Vote',metadata,
            sqla.Column('VoteId', sqla.Integer,primary_key=True),
            sqla.Column('Selected', sqla.ForeignKey('Option.OptionId')),
            sqla.Column('ElectionId',sqla.ForeignKey('Election.ElectionId'))
        )

        self.voted=sqla.Table('Voted',metadata,
            sqla.Column('UserId',sqla.ForeignKey('User.UserId')),
            sqla.Column('ElectionId',sqla.ForeignKey('Election.ElectionId'))
        )

        metadata.create_all(self.engine)
        conn.close()
        self.fillDefault()
        

    def getUser(self,login)->Optional[sqla.engine.row.LegacyRow]:
        conn = self.engine.connect()
        query=sqla.select([self.users]).where(self.users.columns.FullName == login)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        conn.close()

        if len(resultSet)==0:
            return None
        return resultSet[0]


    def isAdmin(self,userId)->bool:
        conn = self.engine.connect()
        query=sqla.select([self.users]).where(self.users.columns.UserId == userId)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        conn.close()

        if len(resultSet)==0:
            return False
        return resultSet[0]['AdministrativeRight']


    def isVoter(self,userId)->bool:
        conn = self.engine.connect()
        query=sqla.select([self.users]).where(self.users.columns.UserId == userId)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        conn.close()

        if len(resultSet)==0:
            return False
        return resultSet[0]['AllowedToVote']
        

    def getElectionList(self,userId)->dict:
        conn = self.engine.connect()
        
        query=sqla.select([self.elections])
        resultProxy = conn.execute(query)
        resultSet1 = resultProxy.fetchall()
        
        query=sqla.select([self.voted]).where(self.voted.columns.UserId == userId)
        resultProxy = conn.execute(query)
        resultSet2 = resultProxy.fetchall()
        
        conn.close()

        result=[]
        voted=list(map(lambda res:res['ElectionId'],resultSet2))
        for election in resultSet1:
            result.append({
                'electionId':election['ElectionId'],
                'electionName':election['Name'],
                'electionType':str(election['VoteType']),
                'electionFinished':not election['Finished'],
                'electionVotable':(not election['ElectionId'] in voted) and not election['Finished']
            })
                
        
        if len(result)==0:
            return None
        return result


    def addElection(self,electionName,voteType)->Optional[int]:
        conn=self.engine.connect()
        query = sqla.insert(self.elections).values(Name=electionName,VoteType=voteType)
        resultProxy = conn.execute(query)
        result=resultProxy.inserted_primary_key
        conn.close()
        return result[0]


    def addOptions(self,electionId,options):
        result=[]
        conn=self.engine.connect()
        for i,option in enumerate(options):
            query = sqla.insert(self.options).values(OptionId=i,ElectionId=electionId,Name=option)
            resultProxy = conn.execute(query)
            result.append(resultProxy.inserted_primary_key)
        conn.close()
        return result


    def getElectionDetails(self,electionId)->Optional[dict]:
        conn = self.engine.connect()

        query=sqla.select([self.elections]).where(self.elections.columns.ElectionId == electionId)
        resultProxy = conn.execute(query)
        resultElection = resultProxy.fetchall()

        query=sqla.select([self.options]).where(self.options.columns.ElectionId == electionId)
        resultProxy = conn.execute(query)
        resultOptions = resultProxy.fetchall()
        
        conn.close()

        if len(resultElection)==0 or len(resultOptions)==0:
            return None
        
        result={}
        for key in resultElection[0].keys():
            result[key[0].lower()+key[1:]]=resultElection[0][key]
        if result['voteType']==VoteType.SINGLE:
            result['voteType']=str(VoteType.SINGLE)
        if result['voteType']==VoteType.APPROVAL:
            result['voteType']=str(VoteType.APPROVAL)
        result['options']=[]
        for option in resultOptions:
            result['options'].append({'optionId':option['OptionId'],'optionName':option['Name']})
        result['electionName']=result['name']
        result.pop('name')
        return result


    def addVote(self,userId,electionId,optionIds)->bool:
        conn=self.engine.connect()

        query=sqla.select([self.voted]).where(self.voted.columns.UserId == userId)
        query=query.where(self.voted.columns.ElectionId == electionId)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()

        if len(resultSet)!=0:
            return False

        query=sqla.select([self.elections]).where(self.elections.columns.ElectionId == electionId)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()

        if len(resultSet)==0:
            return False
        voteType=resultSet[0]['VoteType']

        if voteType==VoteType.SINGLE and len(optionIds)!=1:
            return False
        elif voteType==VoteType.APPROVAL and len(optionIds)==0:
            return False

        for optionId in optionIds:
            query = sqla.insert(self.votes).values(Selected=optionId,ElectionId=electionId)
            resultProxy = conn.execute(query)
        query = sqla.insert(self.voted).values(UserId=userId,ElectionId=electionId)
        resultProxy = conn.execute(query)

        conn.close()
        return True


    def endElection(self,electionId)->bool:
        conn = self.engine.connect()

        query=sqla.select([self.elections]).where(self.elections.columns.ElectionId == electionId)
        resultProxy = conn.execute(query)
        resultElection = resultProxy.fetchall()
        
        if len(resultElection)==0:
            return False
        if resultElection[0]['Finished']:
            return False
        
        query=sqla.update(self.elections).values(Finished=True)
        query=query.where(self.elections.columns.ElectionId == electionId)
        resultProxy = conn.execute(query)

        conn.close()
        return True

        
    def getResult(self,electionId)->Optional[dict]:
        conn = self.engine.connect()

        query=sqla.select([self.elections]).where(self.elections.columns.ElectionId == electionId)
        resultProxy = conn.execute(query)
        resultElection = resultProxy.fetchall()
        
        query=sqla.select([self.options]).where(self.options.columns.ElectionId == electionId)
        resultProxy = conn.execute(query)
        resultOptions = resultProxy.fetchall()

        if len(resultElection)==0 or len(resultOptions)==0:
            return None
        if not resultElection[0]['Finished']:
            return None

        result={}
        result['electionId']=resultElection[0]['ElectionId']
        result['electionName']=resultElection[0]['Name']
        result['finished']=resultElection[0]['Finished']
        if resultElection[0]['VoteType'] ==VoteType.SINGLE:
            result['voteType']=str(VoteType.SINGLE)
        if resultElection[0]['VoteType'] ==VoteType.APPROVAL:
            result['voteType']=str(VoteType.APPROVAL)
        result['options']=[]
        for option in resultOptions:
            query=sqla.select([self.votes]).where(self.votes.columns.ElectionId == electionId)
            query=query.where(self.votes.columns.Selected == option['OptionId'])
            resultProxy = conn.execute(query)
            resultCount = len(resultProxy.fetchall())
            result['options'].append({
                'optionId':option['OptionId'],
                'optionName':option['Name'],
                'voteCount':resultCount
            })

        conn.close()
        return result


    def fillDefault(self):
        conn=self.engine.connect()

        query=sqla.select([self.users]).where(self.users.columns.FullName == "aaa")
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.users).values(UserId=0,FullName="aaa", Password="aaa",AdministrativeRight=True,AllowedToVote=True)
            resultProxy = conn.execute(query)

        query=sqla.select([self.users]).where(self.users.columns.FullName == "bbb")
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.users).values(UserId=1,FullName="bbb", Password="bbb",AdministrativeRight=True,AllowedToVote=False)
            resultProxy = conn.execute(query)

        query=sqla.select([self.users]).where(self.users.columns.FullName == "ccc")
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.users).values(UserId=2,FullName="ccc", Password="ccc",AdministrativeRight=False,AllowedToVote=True)
            resultProxy = conn.execute(query)

        query=sqla.select([self.elections]).where(self.elections.columns.ElectionId == 0)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.elections).values(ElectionId=0,Name="Election 0")
            resultProxy = conn.execute(query)
        
        query=sqla.select([self.options]).where(self.options.columns.ElectionId == 0).where(self.options.columns.OptionId == 0)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.options).values(OptionId=0,ElectionId=0,Name='Election 0 Option 0')
            resultProxy = conn.execute(query)

        query=sqla.select([self.options]).where(self.options.columns.ElectionId == 0).where(self.options.columns.OptionId == 1)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.options).values(OptionId=1,ElectionId=0,Name='Election 0 Option 1')
            resultProxy = conn.execute(query)

        query=sqla.select([self.options]).where(self.options.columns.ElectionId == 0).where(self.options.columns.OptionId == 2)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.options).values(OptionId=2,ElectionId=0,Name='Election 0 Option 2')
            resultProxy = conn.execute(query)

        conn.close()


    


