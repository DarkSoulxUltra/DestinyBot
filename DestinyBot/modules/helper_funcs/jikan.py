import json
import re
import textwrap
import time
from io import BytesIO, StringIO
import bs4
import jikanpy
import requests
from aiohttp import ClientSession
from jikanpy import Jikan

jikan = Jikan()

anilisturl = "https://graphql.anilist.co"
animnefillerurl = "https://www.animefillerlist.com/shows/"
# Anime Helper

weekdays = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}

def get_weekday(dayid):
    for key, value in weekdays.items():
        if value == dayid:
            return key

async def get_anime_schedule(weekid):
    "get anime schedule"
    dayname = get_weekday(weekid)
    result = f"🎀 **Scheduled animes for {dayname.title()} are: **\n\n"
    async with jikanpy.AioJikan() as animesession:
        sr_no = 0
        scheduled_list = (await animesession.schedule(day=dayname)).get(dayname)
        for a_name in scheduled_list:
            result += f"{sr_no + 1}. [{a_name['title']}]({a_name['url']})\n"
    return result, dayname

