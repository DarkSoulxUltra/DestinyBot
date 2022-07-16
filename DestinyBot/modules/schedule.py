"""
Copyright 2021 Nksama

Permission is hereby granted, free of charge,
to any person obtaining a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""


from pyrogram.types.bots_and_keyboards.inline_keyboard_button import (
    InlineKeyboardButton,
)
from pyrogram.types.bots_and_keyboards.inline_keyboard_markup import (
    InlineKeyboardMarkup,
)
from requests import get
import time, datetime
from pyrogram import Client, filters
from datetime import datetime, tzinfo
import pytz
from DestinyBot import pbot as bot


def call_back_in_filter(data):
    return filters.create(lambda flt, _, query: flt.data in query.data, data=data)


def latest():
    url = "https://subsplease.org/api/?f=schedule&h=true&tz=UTC"
    res = get(url).json()
    k = None
    for x in res["schedule"]:
        title = x["title"]
        time = x["time"]
        aired = bool(x["aired"])
        title = (
            f"**[{title}](https://subsplease.org/shows/{x['page']})**"
            if not aired
            else f"**~~[{title}](https://subsplease.org/shows/{x['page']})~~**"
        )
        data = f"{title} :: `{time}`"
        if k:
            k = f"{k}\n{data}"
        else:
            k = data
    return k


@bot.on_message(filters.command("latest"))
def lates(_, message):
    mm = latest()
    TIME_IN_UTC = datetime.now(tz=pytz.UTC).strftime("%H:%M")
    message.reply_text(
        f"Today's Schedule:\nTZ: UTC\nCurrent Time: {TIME_IN_UTC} UTC\n\n{mm}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Refresh", callback_data="fk")]]
        ),
    )


@bot.on_callback_query(call_back_in_filter("fk"))
def callbackk(_, query):
    if query.data == "fk":
        mm = latest()
        TIME_IN_UTC = datetime.now(tz=pytz.UTC).strftime("%H:%M")
        time_ = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M")
        try:
            query.message.edit(
                f"Today's Schedule:\nTZ: UTC\nCurrent Time: {TIME_IN_UTC} UTC\n\n{mm}",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Refresh", callback_data="fk")]]
                ),
            )
            query.answer("Refreshed!")
        except:
            query.answer("Refreshed!")


__mod_name__ = "✧Schedule✧"

__help__ = """
To check the scheduled Anime for the current day from URL: https://subsplease.org/
 ✮ `/latest`*:* to see latest anime episode

To check the scheduled Anime by days from MAL
 ✮ `/aschedule`*:* to see today's scheduled anime.
 ✮ `/aschedule <monday/tuesday/.../sunday>`*:* to see animes schedule on that particular day of the week.
    e.g. /aschedule friday

Note:
1. To ease it up, you can also use /schedule instead of /aschedule for now.
2. For /latest command, Timezone is set to UTC by default, as IST was showing incorrect results in the API.
"""
