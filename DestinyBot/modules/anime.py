import datetime
import re
from DestinyBot import telethn as tbot
from DestinyBot.modules.helper_funcs.tools import post_to_telegraph
from DestinyBot.modules.helper_funcs.jikan import (
    weekdays,
    get_anime_schedule,
    get_filler_episodes,
    search_in_animefiller,
)

# from hentai import Hentai, Utils
# from natsort import natsorted
import html
import textwrap

client = tbot
import asyncio
import os
import time

# from DestinyBot.utils.pluginhelper import edit_or_reply
# from datetime import datetime
from DestinyBot import TEMP_DOWNLOAD_DIRECTORY as path
from DestinyBot import TEMP_DOWNLOAD_DIRECTORY
from datetime import datetime
from DestinyBot.events import register
from DestinyBot.modules.helper_funcs.managers import edit_delete, edit_or_reply
from platform import python_version as py_ver
from telegram import __version__ as tg_ver
from pyrogram import __version__ as pyro_ver
from telethon import __version__ as teleth_ver
from telegram import TelegramError
import bs4
import jikanpy
from jikanpy import Jikan
from jikanpy.exceptions import APIException
import requests
from googlesearch import search
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown
from DestinyBot.modules.helper_funcs.extraction import (
    extract_user,
    extract_user_and_text,
)
from DestinyBot.modules.helper_funcs.string_handling import extract_time
from DestinyBot import DEV_USERS, OWNER_ID, DRAGONS, dispatcher, REQUEST_CHAT_ID, LOGGER
from DestinyBot.modules.disable import DisableAbleCommandHandler
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    Message,
)
from telegram.ext import CallbackContext, CallbackQueryHandler

info_btn = "More Information"
kaizoku_btn = "Kaizoku ☠️"
kayo_btn = "Kayo 🏴‍☠️"
prequel_btn = "⬅️ Prequel"
sequel_btn = "Sequel ➡️"
close_btn = "Close ❌"

jikan = Jikan()


def shorten(description, info="anilist.co"):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + "...."
        msg += f"\n*Description*: _{description}_[Read More]({info})"
    else:
        msg += f"\n*Description*:_{description}_"
    return msg


# time formatter from uniborg
def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Days, ") if days else "")
        + ((str(hours) + " Hours, ") if hours else "")
        + ((str(minutes) + " Minutes, ") if minutes else "")
        + ((str(seconds) + " Seconds, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]


airing_query = """
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        siteUrl
        episodes
        title {
          romaji
          english
          native
        }
        nextAiringEpisode {
           airingAt
           timeUntilAiring
           episode
        }
      }
    }
    """

fav_query = """
query ($id: Int) { 
      Media (id: $id, type: ANIME) { 
        id
        title {
          romaji
          english
          native
        }
     }
}
"""

anime_query = """
   query ($id: Int,$search: String) { 
      Media (id: $id, type: ANIME,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site 
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
"""
character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               image {
                        large
               }
               description
        }
    }
"""

manga_query = """
query ($id: Int,$search: String) { 
      Media (id: $id, type: MANGA,search: $search) { 
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""

AWAKE_MSG = f"""✮ ɪ ᴀᴍ ᴜɴᴍᴇɪ, ᴀ ᴘᴏᴡᴇʀꜰᴜʟ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ʙᴏᴛ. ✮

┏━━━━━━━━━━━━━━━━━━
┣✧ Python Version: 『 {py_ver()} 』
┣✧ Library Version: 『 {tg_ver} 』
┣✧ Telethon Version: 『 {teleth_ver} 』
┣✧ Pyrogram Version: 『 {pyro_ver} 』
┗━━━━━━━━━━━━━━━━━━

 ♡💞 ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ 💞♡
"""

url = "https://graphql.anilist.co"


def extract_arg(message: Message):
    split = message.text.split(" ", 1)
    if len(split) > 1:
        return split[1]
    reply = message.reply_to_message
    if reply is not None:
        return reply.text
    return None


@register(pattern=r"^/fillers ?(.*)")
async def get_anime(event):
    input_str = event.pattern_match.group(1)
    reply = await event.get_reply_message()
    if not input_str:
        if reply:
            input_str = reply.text
        else:
            return await edit_delete(
                event, "__What should i search ? Gib me Something to Search__"
            )
    anime = re.findall(r"-n\d+", input_str)
    try:
        anime = anime[0]
        anime = anime.replace("-n", "")
        input_str = input_str.replace("-n" + anime, "")
        anime = int(anime)
    except IndexError:
        anime = 0
    input_str = input_str.strip()
    result = await search_in_animefiller(input_str)
    if len(result) == 1:
        response = await get_filler_episodes(result[list(result.keys())[0]])
        msg = ""
        msg += f"**Fillers for anime** `{list(result.keys())[0]}`**"
        msg += "\n\n• Manga Canon episodes:**`\n"
        msg += str(response.get("total_ep"))
        msg += "\n\n`**• Mixed/Canon fillers:**`\n"
        msg += str(response.get("mixed_ep"))
        msg += "\n\n`**• Fillers:**\n`"
        msg += str(response.get("filler_episodes"))
        if response.get("anime_canon_episodes") is not None:
            msg += "\n\n`**• Anime Canon episodes:**\n`"
            msg += str(response.get("anime_canon_episodes"))
        msg += "`"
        return await edit_or_reply(event, msg)
    if anime == 0:
        msg = f"**More than 1 result found for {input_str}. so try as** `/fillers -n<number> {input_str}`\n\n"
        for i, an in enumerate(list(result.keys()), start=1):
            msg += f"{i}. {an}\n"
        return await edit_or_reply(event, msg)
    response = await get_filler_episodes(result[list(result.keys())[anime - 1]])

    msg = ""
    msg += f"**Fillers for anime** `{list(result.keys())[anime-1]}`**"
    msg += "\n\n• Manga Canon episodes:**`\n"
    msg += str(response.get("total_ep"))
    msg += "\n\n`**• Mixed/Canon fillers:**`\n"
    msg += str(response.get("mixed_ep"))
    msg += "\n\n`**• Fillers:**\n`"
    msg += str(response.get("filler_episodes"))
    if response.get("anime_canon_episodes") is not None:
        msg += "\n\n`**• Anime Canon episodes:**\n`"
        msg += str(response.get("anime_canon_episodes"))
    msg += "`"
    await edit_or_reply(event, msg)
    if len(result) == 0:
        return await edit_or_reply(
            event, f"**No filler episodes for the given anime**` {input_str}`"
        )


@register(pattern=r"^/schedule ?(.*)")
@register(pattern=r"^/aschedule ?(.*)")
async def aschedule_fetch(event):
    input_str = event.pattern_match.group(1) or datetime.now().weekday()
    # input_str = input_str.lower()
    if input_str in weekdays:
        input_str = weekdays[input_str]
    try:
        input_str = int(input_str)
    except ValueError:
        return await edit_delete(event, "`You have given and invalid weekday`", 7)
    if input_str not in [0, 1, 2, 3, 4, 5, 6]:
        return await edit_delete(event, "`You have given and invalid weekday`", 7)
    result = await get_anime_schedule(input_str)
    await edit_or_reply(event, result[0])


def airing(update: Update, context: CallbackContext):
    message = update.effective_message
    search_str = extract_arg(message)
    if not search_str:
        update.effective_message.reply_text(
            "Tell Anime Name :) ( /airing <anime name>)",
        )
        return
    variables = {"search": search_str}
    response = requests.post(
        url,
        json={"query": airing_query, "variables": variables},
    ).json()["data"]["Media"]
    msg = f"*Name*: *{response['title']['romaji']}*(`{response['title']['native']}`)\n*ID*: `{response['id']}`"
    if response["nextAiringEpisode"]:
        time = response["nextAiringEpisode"]["timeUntilAiring"] * 1000
        time = t(time)
        msg += f"\n*Episode*: `{response['nextAiringEpisode']['episode']}`\n*Airing In*: `{time}`"
    else:
        msg += f"\n*Episode*:{response['episodes']}\n*Status*: `N/A`"
    update.effective_message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)


def anime(update: Update, context: CallbackContext):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        update.effective_message.reply_text("Format : /anime < anime name >")
        return
    else:
        search = search[1]
    variables = {"search": search}
    json = requests.post(
        url, json={"query": anime_query, "variables": variables}
    ).json()
    if "errors" in json.keys():
        update.effective_message.reply_text("Anime not found")
        return
    if json:
        json = json["data"]["Media"]
        msg = f"*{json['title']['romaji']}*(`{json['title']['native']}`)\n*Type*: {json['format']}\n*Status*: {json['status']}\n*Episodes*: {json.get('episodes', 'N/A')}\n*Duration*: {json.get('duration', 'N/A')} Per Ep.\n*Score*: {json['averageScore']}\n*Genres*: `"
        for x in json["genres"]:
            msg += f"{x}, "
        msg = msg[:-2] + "`\n"
        msg += "*Studios*: `"
        for x in json["studios"]["nodes"]:
            msg += f"{x['name']}, "
        msg = msg[:-2] + "`\n"
        info = json.get("siteUrl")
        trailer = json.get("trailer", None)
        # anime_id = json['id']
        if trailer:
            trailer_id = trailer.get("id", None)
            site = trailer.get("site", None)
            if site == "youtube":
                trailer = "https://youtu.be/" + trailer_id
        description = (
            json.get("description", "N/A")
            .replace("<i>", "")
            .replace("</i>", "")
            .replace("<br>", "")
        )
        msg += shorten(description, info)
        image = json.get("bannerImage", None)
        if trailer:
            buttons = [
                [
                    InlineKeyboardButton("More Info", url=info),
                    InlineKeyboardButton("Trailer 🎬", url=trailer),
                ]
            ]
        else:
            buttons = [[InlineKeyboardButton("More Info", url=info)]]
        if image:
            try:
                update.effective_message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except:
                msg += f" [〽️]({image})"
                update.effective_message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        else:
            update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )


def character(update: Update, context: CallbackContext):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        update.effective_message.reply_text("Format : /character < character name >")
        return
    search = search[1]
    variables = {"query": search}
    json = requests.post(
        url, json={"query": character_query, "variables": variables}
    ).json()
    if "errors" in json.keys():
        update.effective_message.reply_text("Character not found")
        return
    if json:
        json = json["data"]["Character"]
        msg = f"*{json.get('name').get('full')}*(`{json.get('name').get('native')}`)\n"
        description = f"{json['description']}"
        site_url = json.get("siteUrl")
        msg += shorten(description, site_url)
        image = json.get("image", None)
        if image:
            image = image.get("large")
            update.effective_message.reply_photo(
                photo=image,
                caption=msg.replace("<b>", "</b>"),
                parse_mode=ParseMode.MARKDOWN,
            )
        else:
            update.effective_message.reply_text(
                msg.replace("<b>", "</b>"), parse_mode=ParseMode.MARKDOWN
            )


def manga(update: Update, context: CallbackContext):
    message = update.effective_message
    search = message.text.split(" ", 1)
    if len(search) == 1:
        update.effective_message.reply_text("Format : /manga < manga name >")
        return
    search = search[1]
    variables = {"search": search}
    json = requests.post(
        url, json={"query": manga_query, "variables": variables}
    ).json()
    msg = ""
    if "errors" in json.keys():
        update.effective_message.reply_text("Manga not found")
        return
    if json:
        json = json["data"]["Media"]
        title, title_native = json["title"].get("romaji", False), json["title"].get(
            "native", False
        )
        start_date, status, score = (
            json["startDate"].get("year", False),
            json.get("status", False),
            json.get("averageScore", False),
        )
        if title:
            msg += f"*{title}*"
            if title_native:
                msg += f"(`{title_native}`)"
        if start_date:
            msg += f"\n*Start Date* - `{start_date}`"
        if status:
            msg += f"\n*Status* - `{status}`"
        if score:
            msg += f"\n*Score* - `{score}`"
        msg += "\n*Genres* - "
        for x in json.get("genres", []):
            msg += f"{x}, "
        msg = msg[:-2]
        info = json["siteUrl"]
        buttons = [[InlineKeyboardButton("More Info", url=info)]]
        image = json.get("bannerImage", False)
        msg += f"_{json.get('description', None)}_"
        if image:
            try:
                update.effective_message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            except:
                msg += f" [〽️]({image})"
                update.effective_message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        else:
            update.effective_message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons),
            )


def awake(update: Update, context: CallbackContext):
    message = update.effective_message
    IMAGE = "https://telegra.ph/file/02f23680b59d520875c4a.mp4"
    msg = ""
    msg += f"{AWAKE_MSG}"
    support = "t.me/unmei_support"
    owner = "t.me/yameteee_yamete_kudasai"
    buttons = [
        [
            InlineKeyboardButton("『 ⚡ Support ⚡ 』", url=support),
            InlineKeyboardButton("『 ♥ Maestro ♥ 』", url=owner),
        ]
    ]
    update.effective_message.reply_animation(
        IMAGE,
        caption=msg,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    # progress_message.delete()


def gsearch(update: Update, context: CallbackContext):
    message = update.effective_message
    bot, args = context.bot, context.args
    rtmid = message.message_id
    chat_id = update.effective_chat.id
    query = str(message.text.split(" ", 1))
    gresults = []
    searched_qry_msg = "`Chotto-Matte, Searching for results...`"
    replying = bot.send_message(
        chat_id, searched_qry_msg, reply_to_message_id=rtmid, parse_mode="Markdown"
    )
    for j in search(
        query,
        tld="com",
        tbs="0",
        safe="off",
        num=10,
        start=0,
        stop=10,
        pause=2.0,
        country="India",
        extra_params=None,
        user_agent=None,
        verify_ssl=True,
    ):
        gresults.append(j)
    if len(gresults) > 0:
        replying.edit_text(
            "Found Some results, be grateful to me for searching this, you lazy A$$.."
        )
        time.sleep(2)
    else:
        replying.edit_text("Gomenne, can't get any results here..")
        return
    sendMessage = ""
    for entry_no in range(len(gresults)):
        if entry_no == 10:
            break
        sendMessage += str(entry_no + 1) + ". " + str(gresults[entry_no]) + "\n"

    replying.edit_text(
        sendMessage, parse_mode="Markdown", disable_web_page_preview=True
    )


def user(update: Update, context: CallbackContext):
    message = update.effective_message
    args = message.text.strip().split(" ", 1)

    try:
        search_query = args[1]
    except:
        if message.reply_to_message:
            search_query = message.reply_to_message.text
        else:
            update.effective_message.reply_text("Format : /user <username>")
            return

    jikan = jikanpy.jikan.Jikan()

    try:
        user = jikan.user(search_query)
    except jikanpy.APIException:
        update.effective_message.reply_text("Username not found.")
        return

    progress_message = update.effective_message.reply_text("Searching.... ")

    date_format = "%Y-%m-%d"
    if user["image_url"] is None:
        img = "https://cdn.myanimelist.net/images/questionmark_50.gif"
    else:
        img = user["image_url"]

    try:
        user_birthday = datetime.datetime.fromisoformat(user["birthday"])
        user_birthday_formatted = user_birthday.strftime(date_format)
    except:
        user_birthday_formatted = "Unknown"

    user_joined_date = datetime.datetime.fromisoformat(user["joined"])
    user_joined_date_formatted = user_joined_date.strftime(date_format)

    for entity in user:
        if user[entity] is None:
            user[entity] = "Unknown"

    about = user["about"].split(" ", 60)

    try:
        about.pop(60)
    except IndexError:
        pass

    about_string = " ".join(about)
    about_string = about_string.replace("<br>", "").strip().replace("\r\n", "\n")

    caption = ""

    caption += textwrap.dedent(
        f"""
    *Username*: [{user['username']}]({user['url']})
    *Gender*: `{user['gender']}`
    *Birthday*: `{user_birthday_formatted}`
    *Joined*: `{user_joined_date_formatted}`
    *Days wasted watching anime*: `{user['anime_stats']['days_watched']}`
    *Days wasted reading manga*: `{user['manga_stats']['days_read']}`
    """
    )

    caption += f"*About*: {about_string}"

    buttons = [
        [InlineKeyboardButton(info_btn, url=user["url"])],
        [
            InlineKeyboardButton(
                close_btn, callback_data=f"anime_close, {message.from_user.id}"
            )
        ],
    ]

    update.effective_message.reply_photo(
        photo=img,
        caption=caption,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=False,
    )
    progress_message.delete()


def request(update: Update, context: CallbackContext):
    message = update.effective_message
    # args = context.args
    # log_message = ""
    IMAGE = "https://telegra.ph/file/5a6c8550a81576df19be9.jpg"
    reqChannelLink = "t.me/+0laY9Q97Djo3OTg1"
    tasLink = "t.me/tas_support"
    chat = update.effective_chat
    ANIME_NAME = message.text.split(" ", 1)
    user = update.effective_user
    bot = context.bot
    buttons = [
        [InlineKeyboardButton("⏱️ Anime Request Queue ⏱️", url=reqChannelLink)],
        [InlineKeyboardButton("🚀 Escalate to Uploaders 🚀", url=tasLink)],
    ]
    try:
        chat_id = REQUEST_CHAT_ID
    except TypeError:
        update.effective_message.reply_text(
            "Bruh, this will work like `/request <anime name>`, don't comedy me.."
        )
    to_send = " ".join(ANIME_NAME)
    # req_by = f"<b>Requested By:</b> {mention_html(member.user.id, html.escape(member.user.first_name))}"
    to_send = to_send.replace("/", "#")
    to_send = to_send.replace("!request", "#request")
    to_send = to_send.replace("@Destiny_x_Bot", "")

    if len(to_send.split(" ")) >= 2:
        try:
            msg = "Request Submitted successfully, please have some patience.\n If your request not processed yet, check the below:\n"
            to_send = f"{to_send}\nRequester: @{user.username}\nRequester ID: {user.id}\n\nFrom Chat: {chat.title}\nChat Username: @{chat.username}\nChat ID: {chat.id}\n"
            update.effective_message.reply_photo(
                IMAGE,
                caption=msg,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text(
                "Couldn't send the message. Perhaps I'm not part of the request group?"
            )
    else:
        # to_send = f"{to_send}\n Requested By : {mention_html(user.id, html.escape(user.first_name))}\n From Chat: <b>{html.escape(chat.title)}:</b>\n"
        update.effective_message.reply_text(
            "Format is incorrect, use `/request <anime_name>` to request an anime."
        )


def upcoming(update: Update, context: CallbackContext):
    jikan = jikanpy.jikan.Jikan()
    upcoming = jikan.top("anime", page=1, subtype="upcoming")

    upcoming_list = [entry["title"] for entry in upcoming["top"]]
    upcoming_message = ""

    for entry_num in range(len(upcoming_list)):
        if entry_num == 10:
            break
        upcoming_message += f"{entry_num + 1}. {upcoming_list[entry_num]}\n"

    update.effective_message.reply_text(upcoming_message)


def button(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    message = query.message
    data = query.data.split(", ")
    query_type = data[0]
    original_user_id = int(data[1])

    user_and_admin_list = [original_user_id, OWNER_ID] + DRAGONS + DEV_USERS

    bot.answer_callback_query(query.id)
    if query_type == "anime_close":
        if query.from_user.id in user_and_admin_list:
            message.delete()
        else:
            query.answer("You are not allowed to use this.")
    elif query_type in ("anime_anime", "anime_manga"):
        mal_id = data[2]
        if query.from_user.id == original_user_id:
            message.delete()
            progress_message = bot.sendMessage(message.chat.id, "Searching.... ")
            caption, buttons, image = get_anime_manga(
                mal_id, query_type, original_user_id
            )
            bot.sendPhoto(
                message.chat.id,
                photo=image,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(buttons),
                disable_web_page_preview=False,
            )
            progress_message.delete()
        else:
            query.answer("You are not allowed to use this.")


"""
@register(pattern=r"^/doujin ?(.*)")
@register(pattern=r"^/nhentai ?(.*)")
async def nhentai(event):
    message_id = event.message.id
    input_str = event.pattern_match.group(1)
    code = input_str
    if "nhentai" in input_str:
        link_regex = r"(?:https?://)?(?:www\.)?nhentai\.net/g/(\d+)"
        match = re.match(link_regex, input_str)
        code = match.group(1)
    if input_str == "random":
        code = Utils.get_random_id()
    if input_str == None or input_str == "" or input_str = " ":
        return await event.reply("No doujin code was provided :-(, so sending some random cultured stuff.")
        await event.delete()
        code = Utils.get_random_id()
    try:
        doujin = Hentai(code)
    except BaseException as n_e:
        if "404" in str(n_e):
            return await event.reply(
                f"No doujin found for `{code}`. You shouldn't use nhentai :-("
            )

    msg = ""
    imgs = "".join(f"<img src='{url}'/>" for url in doujin.image_urls)
    imgs = f"&#8205; {imgs}"
    title = doujin.title()
    graph_link = await post_to_telegraph(title, imgs)
    msg += f"[{title}]({graph_link})"
    msg += f"\n**Source :**\n[{code}]({doujin.url})"
    if doujin.parody:
        msg += "\n**Parodies :**"
        parodies = [
            "#" + parody.name.replace(" ", "_").replace("-", "_")
            for parody in doujin.parody
        ]

        msg += "\n" + " ".join(natsorted(parodies))
    if doujin.character:
        msg += "\n**Characters :**"
        charas = [
            "#" + chara.name.replace(" ", "_").replace("-", "_")
            for chara in doujin.character
        ]

        msg += "\n" + " ".join(natsorted(charas))
    if doujin.tag:
        msg += "\n**Tags :**"
        tags = [
            "#" + tag.name.replace(" ", "_").replace("-", "_") for tag in doujin.tag
        ]

        msg += "\n" + " ".join(natsorted(tags))
    if doujin.artist:
        msg += "\n**Artists :**"
        artists = [
            "#" + artist.name.replace(" ", "_").replace("-", "_")
            for artist in doujin.artist
        ]

        msg += "\n" + " ".join(natsorted(artists))
    if doujin.language:
        msg += "\n**Languages :**"
        languages = [
            "#" + language.name.replace(" ", "_").replace("-", "_")
            for language in doujin.language
        ]

        msg += "\n" + " ".join(natsorted(languages))
    if doujin.category:
        msg += "\n**Categories :**"
        categories = [
            "#" + category.name.replace(" ", "_").replace("-", "_")
            for category in doujin.category
        ]

        msg += "\n" + " ".join(natsorted(categories))
    msg += f"\n**Pages :**\n{doujin.num_pages}"
    await event.reply(msg)	
"""


def site_search(update: Update, context: CallbackContext, site: str):
    message = update.effective_message
    args = message.text.strip().split(" ", 1)
    more_results = True

    try:
        search_query = args[1]
    except IndexError:
        message.reply_text("Give something to search")
        return

    if site == "kaizoku":
        search_url = f"https://animekaizoku.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "post-title"})

        if search_result:
            result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>: \n"
            for entry in search_result:
                post_link = "https://animekaizoku.com/" + entry.a["href"]
                post_name = html.escape(entry.text)
                result += f"• <a href='{post_link}'>{post_name}</a>\n"
        else:
            more_results = False
            result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKaizoku</code>"

    elif site == "kayo":
        search_url = f"https://animekayo.com/?s={search_query}"
        html_text = requests.get(search_url).text
        soup = bs4.BeautifulSoup(html_text, "html.parser")
        search_result = soup.find_all("h2", {"class": "title"})

        result = f"<b>Search results for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>: \n"
        for entry in search_result:

            if entry.text.strip() == "Nothing Found":
                result = f"<b>No result found for</b> <code>{html.escape(search_query)}</code> <b>on</b> <code>AnimeKayo</code>"
                more_results = False
                break

            post_link = entry.a["href"]
            post_name = html.escape(entry.text.strip())
            result += f"• <a href='{post_link}'>{post_name}</a>\n"

    buttons = [[InlineKeyboardButton("See all results", url=search_url)]]

    if more_results:
        message.reply_text(
            result,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
            disable_web_page_preview=True,
        )
    else:
        message.reply_text(
            result, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )


def kaizoku(update: Update, context: CallbackContext):
    site_search(update, context, "kaizoku")


def kayo(update: Update, context: CallbackContext):
    site_search(update, context, "kayo")


__help__ = """
 ──「 Anime search 」──                           
✮ /anime <anime>: returns information about the anime.
✮ /fillers -n{index} <Anime Name>: returns a list of canons, mixed (filler-canons), fillers of that searched anime)
Note:
   1. You can check index by simply searching by /fillers <anime name>
   2. By simply running `/fillers` will return a file with a list of all Anime containing fillers.
   3. For example, by running `/fillers Naruto`, it will reply user to search one of the 7 results as per index.
   Next you can search for one of them, e.g. `/fillers -n4 Naruto`

✮ /character <character>: returns information about the character.
✮ /manga <manga>: returns information about the manga.
✮ /user <user>: returns information about a MyAnimeList user.
✮ /upcoming: returns a list of new anime in the upcoming seasons.
✮ /airing <anime>: returns anime airing info.
✮ /kaizoku <anime>: search an anime on animekaizoku.com
✮ /kayo <anime>: search an anime on animekayo.com

 「 Anime Quotes 」
✮ /animequotes: for anime quotes randomly as photos.
✮ /quote: send quotes randomly as text

──「 Request Anime 」──
✮ /request <anime>: Triggers a request for anime to our channel.
Anime will be posted on [The Channel](https://t.me/trending_anime_series) then the request is marked as completed.
"""

REQUEST_HANDLER = DisableAbleCommandHandler("request", request, run_async=True)
# ASCHEDULE_HANDLER = DisableAbleCommandHandler(("aschedule"), aschedule, run_async=True)
G_HANDLER = DisableAbleCommandHandler("google", gsearch, run_async=True)
check_handler = DisableAbleCommandHandler("alive", awake, run_async=True)
ANIME_HANDLER = DisableAbleCommandHandler("anime", anime, run_async=True)
AIRING_HANDLER = DisableAbleCommandHandler("airing", airing, run_async=True)
CHARACTER_HANDLER = DisableAbleCommandHandler("character", character, run_async=True)
MANGA_HANDLER = DisableAbleCommandHandler("manga", manga, run_async=True)
USER_HANDLER = DisableAbleCommandHandler("user", user, run_async=True)
UPCOMING_HANDLER = DisableAbleCommandHandler("upcoming", upcoming, run_async=True)
KAIZOKU_SEARCH_HANDLER = DisableAbleCommandHandler("kaizoku", kaizoku, run_async=True)
KAYO_SEARCH_HANDLER = DisableAbleCommandHandler("kayo", kayo, run_async=True)
BUTTON_HANDLER = CallbackQueryHandler(button, pattern="anime_.*")

dispatcher.add_handler(REQUEST_HANDLER)
# dispatcher.add_handler(ASCHEDULE_HANDLER)
dispatcher.add_handler(G_HANDLER)
dispatcher.add_handler(check_handler)
dispatcher.add_handler(BUTTON_HANDLER)
dispatcher.add_handler(ANIME_HANDLER)
dispatcher.add_handler(CHARACTER_HANDLER)
dispatcher.add_handler(MANGA_HANDLER)
dispatcher.add_handler(AIRING_HANDLER)
dispatcher.add_handler(USER_HANDLER)
dispatcher.add_handler(KAIZOKU_SEARCH_HANDLER)
dispatcher.add_handler(KAYO_SEARCH_HANDLER)
dispatcher.add_handler(UPCOMING_HANDLER)

__mod_name__ = "Anime"
__command_list__ = [
    "anime",
    "manga",
    "character",
    "user",
    "upcoming",
    "kaizoku",
    "airing",
    "kayo",
    "alive",
    "request",
    "gsearch",
]
__handlers__ = [
    ANIME_HANDLER,
    CHARACTER_HANDLER,
    MANGA_HANDLER,
    USER_HANDLER,
    UPCOMING_HANDLER,
    KAIZOKU_SEARCH_HANDLER,
    KAYO_SEARCH_HANDLER,
    BUTTON_HANDLER,
    AIRING_HANDLER,
    REQUEST_HANDLER,
    G_HANDLER,
]
