from enum import Enum


SESSION_KEY_LENGTH=50
SERVER_ADRESS='0.0.0.0'
SERVER_PORT=5123
DATABASE_FILE_PATH=''
DATABASE_FILE_NAME='votingServer.db'
CELAR_DATABASE_ON_START=True

AUTHENTICATION_SERVER_ADRESS='http://host.docker.internal'
#AUTHENTICATION_SERVER_ADRESS='http://127.0.0.1'
AUTHENTICATION_SERVER_PORT=6123


class VoteType(Enum):
    SINGLE=0
    APPROVAL=1

    def __str__(self):
        return self.name.lower()

