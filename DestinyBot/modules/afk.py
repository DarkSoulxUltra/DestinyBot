
import random, html

from DestinyBot import dispatcher
from DestinyBot.modules.disable import (
    DisableAbleCommandHandler,
    DisableAbleMessageHandler,
)
from DestinyBot.modules.sql import afk_sql as sql
from DestinyBot.modules.users import get_user_id
from telegram import MessageEntity, Update
from telegram.error import BadRequest
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
    run_async,
)

AFK_GROUP = 7
AFK_REPLY_GROUP = 8


def afk(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user

    if not user:  # ignore channels
        return

    if user.id in [777000, 1087968824]:
        return

    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 100:
            reason = reason[:100]
            notice = "\nYour afk reason was shortened to 100 characters."
    else:
        reason = ""

    
    sql.set_afk(update.effective_user.id, reason)
    fname = update.effective_user.first_name
    random_afk_msg = (
        "Naruhodo! Watching porn again?",
        "Yeah sleep already.",
        "Haah! Maybe doing something lewd behind my back.",
        "Okay, updating your ask status, be grateful to me.",
        "I know you are reading..... May be Doujins",
        "I don't think you got a girl that you are ignoring this precious chat, so what are you upto?",
        "Wakatta! Sayonara",
        "Wtf, going already? Not like I care about it.",
        "Do you know what it feels like in lava? Just go and sink in it 🔥",
        "Bye bye!!! Cum back soon",
        "Do you know anything about a Thigh massage Job? Oops my bad, I meant Thai* Massage Jobs.",
        "Mind if I come along with you? Only if you are not thinking something lewd.",
        "Hmmmmmmmm. Wanking off?",
        "Yeah, Go away Horny."
    )
    afk_msg = random.choice(random_afk_msg)
    try:
        update.effective_message.reply_text("{} is now away!{}.\n{}".format(fname, notice,afk_msg))
    except BadRequest:
        pass


def no_longer_afk(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message

    if not user:  # ignore channels
        return

    res = sql.rm_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                "{} arrived! I saw you were stocking in this chat! aren't you?",
                "Hehe, {} is back now, how tf you were even busy?",
                "Guys, {} got a girlfried, that's why he was busy.",
                "{}, chotto matte!! you came out of no where!!",
                "{}, Spammer D2 arrived, lemme grab my ban hammer.",
                "{}, go back to sleep!!!",
                "Were you playing Poker, {}? A Strip Poker, hehe!!!",
                "Yeah, pro like {} arrived again, beware of some noobs!!!",
                "Dear {}, Are you a BTS Lover. I know you were watching it?",
                "{}, I know were watching something dirty, that's why you were away.",
                "Why came back, {}? Girls are away from chat already.",
                "Okairinasai {} Nii-Chan!!",
                "Where is {}?\nIn the chat!",
                "{}, were you doing something lewd?\nI just saw a white stain on your T-shirt."
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_text(chosen_option.format(firstname))
        except:
            return


def reply_afk(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type != MessageEntity.MENTION:
                return

            user_id = get_user_id(message.text[ent.offset : ent.offset + ent.length])
            if not user_id:
                # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                return

            if user_id in chk_users:
                return
            chk_users.append(user_id)

            try:
                chat = bot.get_chat(user_id)
            except BadRequest:
                print("Error: Could not fetch userid {} for AFK module".format(user_id))
                return
            fst_name = chat.first_name

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)
        if int(userc_id) == int(user_id):
            return
        if not user.reason:
            res = "{} is afk".format(fst_name)
            update.effective_message.reply_text(res)
        else:
            res = "{} is afk.\nReason: <code>{}</code>".format(
                html.escape(fst_name), html.escape(user.reason)
            )
            update.effective_message.reply_text(res, parse_mode="html")


AFK_HANDLER = DisableAbleCommandHandler("afk", afk, run_async=True)
AFK_REGEX_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"^(?i)brb(.*)$"), afk, friendly="afk", run_async=True
)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.chat_type.groups, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.chat_type.groups, reply_afk)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

__mod_name__ = "Afk​"
__command_list__ = ["afk"]
__handlers__ = [
    (AFK_HANDLER, AFK_GROUP),
    (AFK_REGEX_HANDLER, AFK_GROUP),
    (NO_AFK_HANDLER, AFK_GROUP),
    (AFK_REPLY_HANDLER, AFK_REPLY_GROUP),
]
