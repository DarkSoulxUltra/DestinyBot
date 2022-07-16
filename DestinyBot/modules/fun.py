import html
import random
import time

import DestinyBot.modules.fun_strings as fun_strings
from DestinyBot import dispatcher
from DestinyBot.modules.disable import DisableAbleCommandHandler
from DestinyBot.modules.helper_funcs.chat_status import is_user_admin
from DestinyBot.modules.helper_funcs.extraction import extract_user
from telegram import ChatPermissions, ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext

GIF_ID = [
    "CgACAgQAAx0CSVUvGgAC7KpfWxMrgGyQs-GUUJgt-TSO8cOIDgACaAgAAlZD0VHT3Zynpr5nGxsE",
    "CgACAgQAAx0CXiWt4wACjEhiEKov41CQtbplxIQFDizay69cpQACKQMAAtZGtFLemSECQkC3_SME",
    "CgACAgQAAx0CXiWt4wACjE1iEKq3tMLVnF6K1t-Od35gO3GwVAAC7wIAAmwttFIkCuHvMkle_CME",
    "CgACAgQAAx0CXiWt4wACjE5iEKq7AtYlCaDGgoP5VR7s7sZZ7gACFgMAAq3GzFJXsgPyMtGIEyME",
    "CgACAgQAAx0CXiWt4wACjE9iEKrBCDgQng6sVbqmU-LxGkFbsQAC3AIAAiudtFIUgy45-_1c2iME",
]

BOT_FLIRTED = (
    "Ohh my, trying to hitting on me with my powers?",
    "If you try something on me, I'll feel weird.🥵",
    "Haah! Better you should use it on someone else. I will only fall for my Maestro.",
    "Wait, are you really flirting with the Robot?",
    "Aaah, you found no girl, that's why hitting on me.",
    "Fine, if you say so. But it's not like I like you and all. I'm just being generous to you. Be grateful to me.",
    "Nope, I only like Maestro. Don't try to seduce me.",
    "Hell no, I won't fall for the likes of you.",
    "Okay! You can flirt with me, but don't think anything would happen between us",
    "B.. Baka, don't flirt with me out of nowhere, I feel little bit shy.",
    "I always thought of you as my Onii-Chan, you sure wanna ruin our relationship?",
    "Ara Ara! My kouhai is trying to flirt with me, O Kawaii Kotto.",
    "Urusei, leave me alone, find some partner already to flirt with.",
)


def runs(update: Update, context: CallbackContext):
    temp = random.choice(fun_strings.RUN_STRINGS)
    if update.effective_user.id == 1170714920:
        temp = "Run everyone, they just dropped a bomb 💣💣"
    update.effective_message.reply_text(temp)


def sanitize(update: Update, context: CallbackContext):
    message = update.effective_message
    TEMP = random.choice(GIF_ID)
    name = (
        message.reply_to_message.from_user.first_name
        if message.reply_to_message
        else message.from_user.first_name
    )
    reply_animation = (
        message.reply_to_message.reply_animation
        if message.reply_to_message
        else message.reply_animation
    )
    reply_animation(TEMP, caption=f"*Sanitizes {name}*")


def slap(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    reply_text = (
        message.reply_to_message.reply_text
        if message.reply_to_message
        else message.reply_text
    )

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.SLAP_SAITAMA_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False),
                )
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)

    if update.effective_user.id == 1096215023:
        temp = "@NeoTheKitty scratches {user2}"

    reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)


def sigma(update: Update, context: CallbackContext):
    update.effective_message.reply_video(random.choice(fun_strings.SIGMA))


def semx(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    reply_text = (
        message.reply_to_message.reply_text
        if message.reply_to_message
        else message.reply_text
    )

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.ATTEMPT_WITH_BOT)
        user1 = curr_user
        reply = temp.format(user1=user1)
        reply_text(reply, parse_mode=ParseMode.HTML)
        return

    if user_id:
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = curr_user
        temp = random.choice(fun_strings.SAVAGE_BOT)
        reply = temp.format(user1=user1)
        reply_text(reply, parse_mode=ParseMode.HTML)
        return

    temp = random.choice(fun_strings.WRECKED_TEMPLATES)

    reply = temp.format(user1=user1, user2=user2)

    reply_text(reply, parse_mode=ParseMode.HTML)


def pat(update: Update, context: CallbackContext):
    bot = context.bot
    args = context.args
    message = update.effective_message

    reply_to = message.reply_to_message if message.reply_to_message else message

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id:
        patted_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(patted_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    pat_type = random.choice(("Text", "Gif", "Sticker"))
    if pat_type == "Gif":
        try:
            temp = random.choice(fun_strings.PAT_GIFS)
            reply_to.reply_animation(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Sticker":
        try:
            temp = random.choice(fun_strings.PAT_STICKERS)
            reply_to.reply_sticker(temp)
        except BadRequest:
            pat_type = "Text"

    if pat_type == "Text":
        temp = random.choice(fun_strings.PAT_TEMPLATES)
        reply = temp.format(user1=user1, user2=user2)
        reply_to.reply_text(reply, parse_mode=ParseMode.HTML)


def aniflirt(update: Update, context: CallbackContext):
    temp = random.choice(fun_strings.ANIME_FLIRT_LINES)
    bottemp = random.choice(BOT_FLIRTED)
    message = update.effective_message
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)

    reply_text = (
        message.reply_to_message.reply_text
        if message.reply_to_message
        else message.reply_text
    )
    if user_id == bot.id:
        reply_text(bottemp, parse_mode=ParseMode.HTML)
    else:
        reply_text(temp, parse_mode=ParseMode.HTML)


def roll(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(range(1, 7)))


def shout(update: Update, context: CallbackContext):
    args = context.args
    text = " ".join(args)
    result = []
    result.append(" ".join(list(text)))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + " " + "  " * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")


def toss(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(fun_strings.TOSS))


def shrug(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    reply_text(r"¯\_(ツ)_/¯")


def bluetext(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = (
        msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    )
    reply_text(
        "/BLUE /TEXT\n/MUST /CLICK\n/I /AM /A /STUPID /ANIMAL /THAT /IS /ATTRACTED /TO /COLORS",
    )


def rlg(update: Update, context: CallbackContext):
    eyes = random.choice(fun_strings.EYES)
    mouth = random.choice(fun_strings.MOUTHS)
    ears = random.choice(fun_strings.EARS)

    if len(eyes) == 2:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]
    else:
        repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]
    update.message.reply_text(repl)


def decide(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.DECIDE))


def eightball(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.EIGHTBALL))


def table(update: Update, context: CallbackContext):
    reply_text = (
        update.effective_message.reply_to_message.reply_text
        if update.effective_message.reply_to_message
        else update.effective_message.reply_text
    )
    reply_text(random.choice(fun_strings.TABLE))


normiefont = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
weebyfont = [
    "卂",
    "乃",
    "匚",
    "刀",
    "乇",
    "下",
    "厶",
    "卄",
    "工",
    "丁",
    "长",
    "乚",
    "从",
    "𠘨",
    "口",
    "尸",
    "㔿",
    "尺",
    "丂",
    "丅",
    "凵",
    "リ",
    "山",
    "乂",
    "丫",
    "乙",
]


def weebify(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    string = ""

    if message.reply_to_message:
        string = message.reply_to_message.text.lower().replace(" ", "  ")

    if args:
        string = "  ".join(args).lower()

    if not string:
        message.reply_text("Usage is `/weebify <text>`", parse_mode=ParseMode.MARKDOWN)
        return

    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)

    if message.reply_to_message:
        message.reply_to_message.reply_text(string)
    else:
        message.reply_text(string)


__help__ = """
✮ /runs*:* reply a random string from an array of replies
✮ /slap*:* slap a user, or get slapped if not a reply
✮ /shrug*:* get shrug XD
✮ /table*:* get flip/unflip :v
✮ /decide*:* Randomly answers yes/no/maybe
✮ /toss*:* Tosses A coin
✮ /bluetext*:* check urself :V
✮ /roll*:* Roll a dice
✮ /rlg*:* Join ears,nose,mouth and create an emo ;-;
✮ /shout <keyword>*:* write anything you want to give loud shout
✮ /weebify <text>*:* returns a weebified text
✮ /sanitize*:* always use this before /pat or any contact
✮ /pat*:* pats a user, or get patted
✮ /8ball*:* predicts using 8ball method
✮ /aniflirt*:* Sends cheesy anime pick-up lines.

- Animation
✮ /love 
✮ /hack 
✮ /bombs 

- Shippering
✮ /couples - get couples of today

- Here is the help for the Styletext module:

✮ /weebify <text>: weebify your text!
✮ /bubble <text>: bubble your text!
✮ /fbubble <text>: bubble-filled your text!
✮ /square <text>: square your text!
✮ /fsquare <text>: square-filled your text!
✮ /blue <text>: bluify your text!
✮ /latin <text>: latinify your text!
✮ /lined <text>: lined your text!
"""

SIGMA_HANDLER = DisableAbleCommandHandler("sigma", sigma, run_async=True)
ANIFLIRT_HANDLER = DisableAbleCommandHandler("aniflirt", aniflirt, run_async=True)
SANITIZE_HANDLER = DisableAbleCommandHandler("sanitize", sanitize, run_async=True)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs, run_async=True)
SEMX_HANDLER = DisableAbleCommandHandler(("sex", "fuck"), semx, run_async=True)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, run_async=True)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat, run_async=True)
ROLL_HANDLER = DisableAbleCommandHandler("roll", roll, run_async=True)
TOSS_HANDLER = DisableAbleCommandHandler("toss", toss, run_async=True)
SHRUG_HANDLER = DisableAbleCommandHandler("shrug", shrug, run_async=True)
BLUETEXT_HANDLER = DisableAbleCommandHandler("bluetext", bluetext, run_async=True)
RLG_HANDLER = DisableAbleCommandHandler("rlg", rlg, run_async=True)
DECIDE_HANDLER = DisableAbleCommandHandler("decide", decide, run_async=True)
EIGHTBALL_HANDLER = DisableAbleCommandHandler("8ball", eightball, run_async=True)
TABLE_HANDLER = DisableAbleCommandHandler("table", table, run_async=True)
SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, run_async=True)
WEEBIFY_HANDLER = DisableAbleCommandHandler("weebify", weebify, run_async=True)

dispatcher.add_handler(SIGMA_HANDLER)
dispatcher.add_handler(ANIFLIRT_HANDLER)
dispatcher.add_handler(SEMX_HANDLER)
dispatcher.add_handler(WEEBIFY_HANDLER)
dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(SANITIZE_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(ROLL_HANDLER)
dispatcher.add_handler(TOSS_HANDLER)
dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(BLUETEXT_HANDLER)
dispatcher.add_handler(RLG_HANDLER)
dispatcher.add_handler(DECIDE_HANDLER)
dispatcher.add_handler(EIGHTBALL_HANDLER)
dispatcher.add_handler(TABLE_HANDLER)

__mod_name__ = "Fun"
__command_list__ = [
    "runs",
    "slap",
    "roll",
    "toss",
    "shrug",
    "bluetext",
    "rlg",
    "decide",
    "table",
    "pat",
    "sanitize",
    "shout",
    "weebify",
    "8ball",
    "aniflirt",
    "sex",
    "sigma",
]
__handlers__ = [
    SIGMA_HANDLER,
    ANIFLIRT_HANDLER,
    RUNS_HANDLER,
    SLAP_HANDLER,
    PAT_HANDLER,
    ROLL_HANDLER,
    TOSS_HANDLER,
    SHRUG_HANDLER,
    BLUETEXT_HANDLER,
    RLG_HANDLER,
    DECIDE_HANDLER,
    TABLE_HANDLER,
    SANITIZE_HANDLER,
    SHOUT_HANDLER,
    WEEBIFY_HANDLER,
    EIGHTBALL_HANDLER,
    SEMX_HANDLER,
]
