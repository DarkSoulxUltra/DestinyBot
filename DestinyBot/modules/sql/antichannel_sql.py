import threading
from sqlalchemy import Column, String
from DestinyBot.modules.sql import BASE, SESSION

#   |----------------------------------|
#   |  Test Module by @EverythingSuckz |
#   |        Kang with Credits         |
#   |----------------------------------|
class AntiChannelChats(BASE):
    __tablename__ = "antichannel_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


AntiChannelChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_antichannel(chat_id):
    try:
        chat = SESSION.query(AntiChannelChats).get(str(chat_id))
        if chat:
            return True
        else:
            return False
    finally:
        SESSION.close()


def set_antichannel(chat_id):
    with INSERTION_LOCK:
        antichannelchat = SESSION.query(AntiChannelChats).get(str(chat_id))
        if not antichannelchat:
            antichannelchat = AntiChannelChats(str(chat_id))
        SESSION.add(antichannelchat)
        SESSION.commit()


def rem_antichannel(chat_id):
    with INSERTION_LOCK:
        antichannelchat = SESSION.query(AntiChannelChats).get(str(chat_id))
        if antichannelchat:
            SESSION.delete(antichannelchat)
        SESSION.commit()


def get_all_antichannel_chats():
    try:
        return SESSION.query(AntiChannelChats.chat_id).all()
    finally:
        SESSION.close()
