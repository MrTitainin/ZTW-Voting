from enum import Enum


SESSION_KEY_LENGTH=50
SERVER_ADRESS='127.0.0.1'
SERVER_PORT=5123
DATABASE_FILE_PATH='server/'
DATABASE_FILE_NAME='votingServer.db'


class VoteType(Enum):
    SINGLE=0
    APPROVAL=1

