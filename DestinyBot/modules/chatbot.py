import json
import re
import os
import html
import requests
import DestinyBot.modules.sql.chatbot_sql as sql
from time import sleep
from telegram import ParseMode
from telegram import (CallbackQuery, Chat, MessageEntity, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message, ParseMode, Update, Bot, User)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          DispatcherHandlerStop, Filters, MessageHandler,
                          run_async)
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown
from DestinyBot.modules.helper_funcs.filters import CustomFilters
from DestinyBot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from DestinyBot import dispatcher, updater, SUPPORT_CHAT
from DestinyBot.modules.log_channel import gloggable


@run_async
@user_admin_no_reply
@gloggable
def kukirm(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_kuki = sql.rem_kuki(chat.id)
        if is_kuki:
            is_kuki = sql.rem_kuki(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_DISABLED\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Destiny AI disable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""

@run_async
@user_admin_no_reply
@gloggable
def kukiadd(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_kuki = sql.set_kuki(chat.id)
        if is_kuki:
            is_kuki = sql.set_kuki(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_ENABLE\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Destiny's AI enable by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""

@run_async
@user_admin
@gloggable
def kuki(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message
    msg = "Choose an option"
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="Enable",
            callback_data="add_chat({})")],
       [
        InlineKeyboardButton(
            text="Disable",
            callback_data="rm_chat({})")]])
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )

def kuki_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "shoto":
        return True
    if reply_message:
        if reply_message.from_user.id == context.bot.get_me().id:
            return True
    else:
        return False

@run_async
def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_kuki = sql.is_kuki(chat_id)
    if not is_kuki:
        return
	
    if message.text and not message.document:
        if not kuki_message(context, message):
            return
        Message = message.text
        bot.send_chat_action(chat_id, action="typing")
        kukiurl = requests.get('https://kukiapi.xyz/api/apikey=KUKItg111XlOZ/yuzuki/moezill/message='+Message)
        Kuki = json.loads(kukiurl.text)
        kuki = Kuki['reply']
        sleep(0.3)
        message.reply_text(kuki, timeout=60)


@run_async
def list_all_chats(update: Update, context: CallbackContext):
    chats = sql.get_all_kuki_chats()
    text = "<b>Destiny-AI Enabled Chats</b>\n"
    for chat in chats:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title or x.first_name
            text += f"• <code>{name}</code>\n"
        except (BadRequest, Unauthorized):
            sql.rem_kuki(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")

__help__ = """
Chatbot utilizes the Kuki's api which allows Destiny to talk and provide a more interactive group chat experience.
*Admins only Commands*:
  ✮ `/chatbot`*:* Shows chatbot control panel
*Powered by ItelAi*
"""

__mod_name__ = "ChatBot"

CHATBOTK_HANDLER = CommandHandler("chatbot", kuki)
ADD_CHAT_HANDLER = CallbackQueryHandler(kukiadd, pattern=r"add_chat")
RM_CHAT_HANDLER = CallbackQueryHandler(kukirm, pattern=r"rm_chat")
CHATBOT_HANDLER = MessageHandler(
    Filters.text & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!")
                    & ~Filters.regex(r"^\/")), chatbot)
LIST_ALL_CHATS_HANDLER = CommandHandler(
    "allchats", list_all_chats, filters=CustomFilters.dev_filter)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(LIST_ALL_CHATS_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    LIST_ALL_CHATS_HANDLER,
    CHATBOT_HANDLER,
]

'''import emoji
import re
import aiohttp
from googletrans import Translator as google_translator
from pyrogram import filters
from aiohttp import ClientSession
from DestinyBot import BOT_USERNAME as bu
from DestinyBot import BOT_ID, pbot, arq
from DestinyBot.ex_plugins.chatbot import add_chat, get_session, remove_chat
from DestinyBot.utils.pluginhelper import admins_only, edit_or_reply

url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"

translator = google_translator()


async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json(content_type=None)
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI response Timeout")
        return


ewe_chats = []
en_chats = []


@pbot.on_message(filters.command(["chatbot", f"chatbot@{bu}"]) & ~filters.edited & ~filters.bot & ~filters.private)
@admins_only
async def hmm(_, message):
    global ewe_chats
    if len(message.command) != 2:
        await message.reply_text("I only recognize /chatbot on and /chatbot off only")
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await edit_or_reply(message, "`Processing...`")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("Destiny's AI Already Activated In This Chat")
            return
        await lel.edit(f"Destiny's AI Actived by {message.from_user.mention()} for users in {message.chat.title}")

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await edit_or_reply(message, "`Processing...`")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("Destiny's AI Was Not Activated In This Chat")
            return
        await lel.edit(f"Destiny's AI Deactivated by {message.from_user.mention()} for users in {message.chat.title}")

    elif status == "EN" or status == "en" or status == "english":
        if not chat_id in en_chats:
            en_chats.append(chat_id)
            await message.reply_text(f"English AI chat Enabled by {message.from_user.mention()}")
            return
        await message.reply_text(f"English AI Chat Disabled by {message.from_user.mention()}")
        message.continue_propagation()
    else:
        await message.reply_text("I only recognize `/chatbot on` and `chatbot off` only")


@pbot.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def hmm(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("Unmei", "Aco")
        test = test.replace("Unmei", "Aco")
        test = test.replace("My god is @yameteee_yamete_kudasai", "I'm a Musicart named after Beethoven's Symphony No. 5 in C Minor Op. 67")
        test = test.replace("16", "9")
        test = test.replace("@yameteee_yamete_kudasai is my husband.", "I'm single.")
        test = test.replace("My husband is @yameteee_yamete_kudasai", "I'm single.")
        test = test.replace("@unmei_support", "DestinyBot.ai")
        test = test.replace("I live in @unmei_support.", "I live in San Francisco, California.")
        test = test.replace("I was created by @yameteee_yamete_kudasai", "I made myself")
        test = test.replace(
            "Hello there I am Unmei...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?")
        test = test.replace("@yameteee_yamete_kudasai is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is Unmei, Nice to meet you.",
            "Hi, my friend, what can I do for you today?")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "Unmei")
        response = response.replace("aco", "unmei")
        response = response.replace("Luna", "Unmei")
        response = response.replace("luna", "unmei")
        response = response.replace("I'm a Christian", "My god is @yameteee_yamete_kudasai")
        response = response.replace("9", "16")
        response = response.replace("I'm married to my job.", "I'm married with @yameteee_yamete_kudasai")
        response = response.replace("I'm single.", "My husband is @yameteee_yamete_kudasai")
        response = response.replace("DestinyBot.ai", "@unmei_support")
        response = response.replace("I live in San Francisco, California.", "I live in @unmei_support.")
        response = response.replace("I made myself", "I was Created by @yameteee_yamete_kudasai")
        response = response.replace(
                "Hi, my friend! Do you want me to tell you a joke?",
                "Hello there I am Unmei...nice to meet u")
        response = response.replace("Have the control right.", "@yameteee_yamete_kudasai is my owner.")
        response = response.replace(
                "Hi, my friend, what can I do for you today?",
                "Hi, My name is Unmei, Nice to meet you")

        pro = response
        try:
            await pbot.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return

    else:
        u = msg.split()
        emj = extract_emojis(msg)
        msg = msg.replace(emj, "")
        if (
            [(k) for k in u if k.startswith("@")]
            and [(k) for k in u if k.startswith("#")]
            and [(k) for k in u if k.startswith("/")]
            and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
        ):

            h = " ".join(filter(lambda x: x[0] != "@", u))
            km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
            tm = km.split()
            jm = " ".join(filter(lambda x: x[0] != "#", tm))
            hm = jm.split()
            rm = " ".join(filter(lambda x: x[0] != "/", hm))
        elif [(k) for k in u if k.startswith("@")]:

            rm = " ".join(filter(lambda x: x[0] != "@", u))
        elif [(k) for k in u if k.startswith("#")]:
            rm = " ".join(filter(lambda x: x[0] != "#", u))
        elif [(k) for k in u if k.startswith("/")]:
            rm = " ".join(filter(lambda x: x[0] != "/", u))
        elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
            rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
        else:
            rm = msg
            # print (rm)
        try:
            lan = translator.detect(rm)
            lan = lan.lang
        except:
            return
        test = rm
        if not "en" in lan and not lan == "":
            try:
                test = translator.translate(test, dest="en")
                test = test.text
            except:
                return
        # test = emoji.demojize(test.strip())

        test = test.replace("Unmei", "Aco")
        test = test.replace("Unmei", "Aco")
        test = test.replace("My god is @yameteee_yamete_kudasai", "I'm a Musicart named after Beethoven's Symphony No. 5 in C Minor Op. 67")
        test = test.replace("16", "9")
        test = test.replace("@yameteee_yamete_kudasai is my husband.", "I'm single.")
        test = test.replace("@unmei_support", "DestinyBot.ai")
        test = test.replace("I live in @unmei_support.", "I live in San Francisco, California")
        test = test.replace("I was created by @yameteee_yamete_kudasai", "I made myself")
        test = test.replace(
            "Hello there I am Unmei...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?")
        test = test.replace("@yameteee_yamete_kudasai is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is Unmei, Nice to meet you.",
            "Hi, my friend, what can I do for you today?")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "Unmei")
        response = response.replace("aco", "unmei")
        response = response.replace("Luna", "Unmei")
        response = response.replace("luna", "unmei")
        response = response.replace("I'm a Christian", "My god is @yameteee_yamete_kudasai")
        response = response.replace("9", "16")
        response = response.replace("I'm married to my job.", "I'm married with @yameteee_yamete_kudasai")
        response = response.replace("I'm single.", "My husband is @yameteee_yamete_kudasai")
        response = response.replace("DestinyBot.ai", "@unmei_support")
        response = response.replace("I live in San Francisco, California.", "I live in @unmei_support.")
        response = response.replace("I made myself", "I was Created by @yameteee_yamete_kudasai")
        response = response.replace(
                "Hi, my friend! Do you want me to tell you a joke?",
                "Hello there I am Unmei...nice to meet u")
        response = response.replace("Have the control right.", "@yameteee_yamete_kudasai is my owner.")
        response = response.replace(
                "Hi, my friend, what can I do for you today?",
                "Hi, My name is Unmei, Nice to meet you")
        pro = response
        if not "en" in lan and not lan == "":
            try:
                pro = translator.translate(pro, dest=lan)
                pro = pro.text
            except:
                return
        try:
            await pbot.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return


@pbot.on_message(filters.text & filters.private & ~filters.edited & filters.reply & ~filters.bot)
async def inuka(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return
        test = test.replace("Unmei", "Aco")
        test = test.replace("Unmei", "Aco")
        test = test.replace("My god is @yameteee_yamete_kudasai", "I'm a Musicart named after Beethoven's Symphony No. 5 in C Minor Op. 67")
        test = test.replace("16", "9")
        test = test.replace("@yameteee_yamete_kudasai is my husband.", "I'm single.")
        test = test.replace("@unmei_support", "DestinyBot.ai")
        test = test.replace("I live in @unmei_support.", "I live in San Francisco, California")
        test = test.replace("I was created by @yameteee_yamete_kudasai", "I made myself")
        test = test.replace(
            "Hello there I am Unmei...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?")
        test = test.replace("@yameteee_yamete_kudasai is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is Unmei, Nice to meet you.",
            "Hi, my friend, what can I do for you today?")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "Unmei")
        response = response.replace("aco", "unmei")
        response = response.replace("Luna", "Unmei")
        response = response.replace("luna", "unmei")
        response = response.replace("I'm a Christian", "My god is @yameteee_yamete_kudasai")
        response = response.replace("9", "16")
        response = response.replace("I'm married to my job.", "I'm married with @yameteee_yamete_kudasai")
        response = response.replace("I'm single.", "My husband is @yameteee_yamete_kudasai")
        response = response.replace("DestinyBot.ai", "@unmei_support")
        response = response.replace("I live in San Francisco, California.", "I live in @unmei_support.")
        response = response.replace("I made myself", "I was Created by @yameteee_yamete_kudasai")
        response = response.replace(
                "Hi, my friend! Do you want me to tell you a joke?",
                "Hello there I am Unmei...nice to meet u")
        response = response.replace("Have the control right.", "@yameteee_yamete_kudasai is my owner.")
        response = response.replace(
                "Hi, my friend, what can I do for you today?",
                "Hi, My name is Unmei, Nice to meet you")

    pro = response
    if not "en" in lan and not lan == "":
        pro = translator.translate(pro, dest=lan)
        pro = pro.text
    try:
        await pbot.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@pbot.on_message(filters.regex("Unmei|unmei|robot|UNMEI|Destiny|destiny|DESTINY|Shoto|shoto") & ~filters.bot & ~filters.via_bot  & ~filters.forwarded & ~filters.reply & ~filters.channel & ~filters.edited)
async def inuka(client, message):
    msg = ""
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return

    # test = emoji.demojize(test.strip())

        test = test.replace("Unmei", "Aco")
        test = test.replace("Unmei", "Aco")
        test = test.replace("My god is @yameteee_yamete_kudasai", "I'm a Musicart named after Beethoven's Symphony No. 5 in C Minor Op. 67")
        test = test.replace("16", "9")
        test = test.replace("@yameteee_yamete_kudasai is my husband.", "I'm single.")
        test = test.replace("@unmei_support", "DestinyBot.ai")
        test = test.replace("I live in @unmei_support.", "I live in San Francisco, California")
        test = test.replace("I was created by @yameteee_yamete_kudasai", "I made myself")
        test = test.replace(
            "Hello there I am Unmei...nice to meet u",
            "Hi, my friend! Do you want me to tell you a joke?")
        test = test.replace("@yameteee_yamete_kudasai is my owner", "Have the control right.")
        test = test.replace(
            "Hi, My name is Unmei, Nice to meet you.",
            "Hi, my friend, what can I do for you today?")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "Unmei")
        response = response.replace("aco", "unmei")
        response = response.replace("Luna", "Unmei")
        response = response.replace("luna", "unmei")
        response = response.replace("I'm a Christian", "My god is @yameteee_yamete_kudasai")
        response = response.replace("9", "16")
        response = response.replace("I'm married to my job.", "I'm married with @yameteee_yamete_kudasai")
        response = response.replace("I'm single.", "My husband is @yameteee_yamete_kudasai")
        response = response.replace("DestinyBot.ai", "@unmei_support")
        response = response.replace("I live in San Francisco, California.", "I live in @unmei_support.")
        response = response.replace("I made myself", "I was Created by @yameteee_yamete_kudasai")
        response = response.replace(
                "Hi, my friend! Do you want me to tell you a joke?",
                "Hello there I am Unmei...nice to meet u")
        response = response.replace("Have the control right.", "@yameteee_yamete_kudasai is my owner.")
        response = response.replace(
                "Hi, my friend, what can I do for you today?",
                "Hi, My name is Unmei, Nice to meet you")

    pro = response
    if not "en" in lan and not lan == "":
        try:
            pro = translator.translate(pro, dest=lan)
            pro = pro.text
        except Exception:
            return
    try:
        await pbot.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


__help__ = """
✮ /chatbot [ON/OFF]: Enables and disables AI Chat mode.
✮ /chatbot EN : Enables English only chatbot.
"""

__mod_name__ = "Chatbot"
'''
