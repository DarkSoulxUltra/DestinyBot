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
    if not is_nsfw:
        msg.reply_text("Antichannel Filter is already Deactivated")
        return ""
    else:
        sql.rem_antichannel(chat.id)
        msg.reply_text("Antichannel Filter Deactivated! Be aware of channel spammers")
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
            sql.rem_nsfw(*chat)
        except Unauthorized:
            sql.rem_nsfw(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")


@tbot.on(events.NewMessage(pattern=None))
async def del_antichannel(event):
    if event.is_private:
        return
    msg = str(event.text)
    sender = event.get_sender()
    chat_id = event.chat_id
    is_antichannel = sql.is_antichannel(chat_id)
    if not is_antichannel:
        return
    else:
        if sender == "136817688":
            msg = f"Channel Spotted, antichannel is activated, deleting the message."
            bot_reply = await event.respond(msg)
            await asyncio.sleep(6)
            await event.delete()
