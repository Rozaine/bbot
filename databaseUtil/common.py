from datetime import datetime

from . import sql_database
from . import mongo_database


def getCount():
    return len(list(mongo_database.getCountBooks()))


def addDownload(user_id, book_name: str):
    _current_dateTime = datetime.now()
    sql_database.addDownloadBookToUser(_current_dateTime, user_id, book_name)


def hasRegistered(msg):
    if sql_database.hasRegistered(msg.from_user.id) == []:
        return False
    else:
        return True


def updateLastUserActivity(msg):
    _chat_id = msg.from_user.id
    _current_dateTime = datetime.now()
    sql_database.updateLastUserActivitySql(_chat_id, _current_dateTime)


def getTodayRegUsersCount():
    return sql_database.getTodayRegUsersCount()


def getAllUsersCount():
    return sql_database.getAllUsersCount()


def registerUser(msg):
    if not hasRegistered(msg):
        _chat_id = msg.from_user.id
        _user_name = msg.from_user.first_name
        _current_dateTime = datetime.now()
        sql_database.addUserSql(_chat_id, _user_name, _current_dateTime, _current_dateTime)
