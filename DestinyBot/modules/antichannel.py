import datetime
import re
from DestinyBot import telethn as tbot
from telethon import events
import html
import textwrap
client = tbot
import asyncio
import time
from DestinyBot.events import register
from telethon import Button
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
import os
import nekos
import requests
from PIL import Image
from telegram import ParseMode
from DestinyBot import dispatcher, updater
import DestinyBot.modules.sql.antichannel_sql as sql
from DestinyBot.modules.log_channel import gloggable
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import CommandHandler, run_async, CallbackContext
from DestinyBot.modules.helper_funcs.filters import CustomFilters
from DestinyBot.modules.helper_funcs.chat_status import user_admin
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown



@user_admin
@gloggable
def add_antichannel(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user #Remodified by @EverythingSuckz
    is_antichannel = sql.is_antichannel(chat.id)
    if not is_antichannel:
        sql.set_antichannel(chat.id)
        msg.reply_text("Antichannel Filter Activated!!!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"ACTIVATED_ANTI_CHANNEL\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message
    else:
        msg.reply_text("Antichannel is already ACTIVATED!")
        return ""


@user_admin
@gloggable
def rem_antichannel(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    is_antichannel = sql.is_antichannel(chat.id)
    if not is_antichannel:
        msg.reply_text("Antichannel Filter is already Deactivated")
        return ""
    else:
        sql.rem_antichannel(chat.id)
        msg.reply_text("Antichannel Filter Deactivated! Be aware of the Channel Spammers")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"DEACTIVATED_ANTI_CHANNEL\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message

def list_antichannel_chats(update: Update, context: CallbackContext):
    chats = sql.get_all_antichannel_chats()
    text = "<b>Antichannel Activated Chats</b>\n"
    for chat in chats:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title if x.title else x.first_name
            text += f"• <code>{name}</code>\n"
        except BadRequest:
            sql.rem_antichannel(*chat)
        except Unauthorized:
            sql.rem_antichannel(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")


@tbot.on(events.NewMessage(pattern=None))
async def del_antichannel(event):
    if event.is_private:
        return
    msg = str(event.text)
    sender = event.get_sender()
    sender = str(sender)
    chat_id = event.chat_id
    is_antichannel = sql.is_antichannel(chat_id)
    if not is_antichannel:
        return
    else:
        if sender.startswith("-"):
            msg = f"Channel Spotted, antichannel is activated, deleting the message."
            bot_reply = await event.respond(msg)
            await asyncio.sleep(6)
            await event.delete()
            

ADD_ANTICHANNEL_HANDLER = CommandHandler("addantichannel", add_antichannel, run_async=True)
REMOVE_ANTICHANNEL_HANDLER = CommandHandler("rmantichannel", rem_antichannel, run_async=True)
LIST_ANTICHANNEL_CHATS_HANDLER = CommandHandler(
    "antichannelchats", list_antichannel_chats, filters=CustomFilters.dev_filter, run_async=True)


dispatcher.add_handler(ADD_ANTICHANNEL_HANDLER)
dispatcher.add_handler(REMOVE_ANTICHANNEL_HANDLER)
dispatcher.add_handler(LIST_ANTICHANNEL_CHATS_HANDLER)


__handlers__ = [
    ADD_ANTICHANNEL_HANDLER,
    REMOVE_ANTICHANNEL_HANDLER,
    LIST_ANTICHANNEL_CHATS_HANDLER
]

__help__ = """
*Anti-Channel*
 ✮ /addantichannel*:* Activates Anti-Channel filter on your group.
 ✮ /rmantichannel*:* De-Activates Anti-Channel filter on your group.
 
Anti-Channel is used to protect your groups from Channel spamming, which cannot be muted or banned by the bots. Destiny can delete the messages incoming from channels.
Contact @unmei_support for more queries.
"""

__mod_name__ = "Anti-Channel"
