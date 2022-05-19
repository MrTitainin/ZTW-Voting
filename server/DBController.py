from enum import unique
from typing import Optional
import sqlalchemy as sqla
from constants import *

class DBController():
    def __init__(self):
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
        


    def getElectionList(self,userId)->list[tuple]:
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
            if not election['ElectionId'] in voted:
                result.append((election['ElectionId'],election['Name']))
        
        if len(result)==0:
            return None
        return result











    def fillDefault(self):
        conn=self.engine.connect()

        query=sqla.select([self.users]).where(self.users.columns.FullName == "aaa")
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.users).values(FullName="aaa", Password="aaa",AdministrativeRight=True,AllowedToVote=True)
            resultProxy = conn.execute(query)

        query=sqla.select([self.users]).where(self.users.columns.FullName == "bbb")
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.users).values(FullName="bbb", Password="bbb",AdministrativeRight=True,AllowedToVote=False)
            resultProxy = conn.execute(query)

        query=sqla.select([self.users]).where(self.users.columns.FullName == "ccc")
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.users).values(FullName="ccc", Password="ccc",AdministrativeRight=False,AllowedToVote=True)
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

        query=sqla.select([self.options]).where(self.options.columns.ElectionId == 0).where(self.options.columns.OptionId == 1)
        resultProxy = conn.execute(query)
        resultSet = resultProxy.fetchall()
        if (len(resultSet)==0):
            query = sqla.insert(self.options).values(OptionId=2,ElectionId=0,Name='Election 0 Option 2')
            resultProxy = conn.execute(query)

        conn.close()


    


