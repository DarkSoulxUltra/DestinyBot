import datetime
from telegram import TelegramError
from DestinyBot import dispatcher, SUPPORT_CHAT_ID, LOGGER
from DestinyBot.modules.disable import DisableAbleCommandHandler
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update, Message)
from telegram.ext import CallbackContext, CallbackQueryHandler

def bug(update: Update, context: CallbackContext):
    message = update.effective_message
    IMAGE = "https://telegra.ph/file/0ec3d2fadf05511e819c1.jpg"
    #args = context.args
    #log_message = ""
    bugChannelLink = "t.me/+Q3UyHDVMVUdhY2Fl"
    supportLink = "t.me/unmei_support"
    chat = update.effective_chat
    BUG_DETAILS = message.text.split(' ', 1)
    user = update.effective_user
    bot = context.bot
    try:
        chat_id = SUPPORT_CHAT_ID
    except TypeError:
        update.effective_message.reply_text("Bruh, this will work like `/bug <report about a bug>`, don't comedy me..")
    to_send = " ".join(BUG_DETAILS)
    #req_by = f"<b>Requested By:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    to_send = to_send.replace("/","#")
    to_send = to_send.replace("@Destiny_x_Bot","")
    buttons = [
        [InlineKeyboardButton("Check Bugs Queue?", url=bugChannelLink)],
        [InlineKeyboardButton("Escalate it to Support?", url=supportLink)]
    ]

    msg = f"Bug details Submitted successfully.\n"
    if len(to_send.split(" ")) >= 2:
        try:
            to_send = f"{to_send}\nRequester: @{user.username}\nRequester ID: {user.id}\n\nFrom Chat: {chat.title}\nChat Username: @{chat.username}\nChat ID: {chat.id}\n"
            update.effective_message.reply_photo(
	        IMAGE,
                caption=msg,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of the request group?"
            )
    else:
        #to_send = f"{to_send}\n Requested By : {mention_html(user.id, html.escape(user.first_name))}\n From Chat: <b>{html.escape(chat.title)}:</b>\n"
        update.effective_message.reply_text("Bruh, this will work like `/bug <report about a bug>`, don't comedy me..")



__help__ = """

 ──「 Bug Report 」──                           

✮ `/bug <report text>`: Sends a string containing the bot issues directly to Unmei's support private channel.

Note: This command will also collect the details about the user like telegram ID and username, if someone
tried to spam it, they might suffer a gban.

Reach out to @unmei_support for any queries.

"""

BUG_HANDLER = DisableAbleCommandHandler("bug", bug, run_async=True)

dispatcher.add_handler(BUG_HANDLER)

__mod_name__ = "Bug Report"
__command_list__ = [
    "bug"
]
__handlers__ = [
    BUG_HANDLER
]
