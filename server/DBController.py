from typing import Optional


class DBController():
    def __init__(self):
        pass

    def getUser(self,login):#optional
        """connection = engine.connect()
        query=db.select([users]).where(users.columns.id == id)
        resultProxy = connection.execute(query)
        resultSet = resultProxy.fetchall()"""
        return {'login':'aaa','password':'aaa'}


    def getElectionList(self,login)->list[tuple]:
        return [(1,'elect1'),(2,'elect2'),(3,'elect3')]



