import os
import urllib
import random
import aiohttp
import requests
from pyrogram import filters
from DestinyBot import pbot

MemesReddit = [
    "Animemes",
    "lostpause",
    "LoliMemes",
    "cleananimemes",
    "animememes",
    "goodanimemes",
    "AnimeFunny",
    "dankmemes",
    "teenagers",
    "shitposting",
    "Hornyjail",
    "wholesomememes",
    "cursedcomments",
]


@pbot.on_message(filters.command("meme"))
async def meme(client, message):
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(
            "https://meme-api.herokuapp.com/gimme/wholesomememes"
        ) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])


@pbot.on_message(filters.command("cursed"))
async def cursedmemes(client, message):
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(
            "https://meme-api.herokuapp.com/gimme/cursedcomments"
        ) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])


@pbot.on_message(filters.command("shitpost"))
async def shitpost(client, message):
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(
            "https://meme-api.herokuapp.com/gimme/shitposting"
        ) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])


@pbot.on_message(filters.command("fbi"))
async def fbi(client, message):
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(
            "https://meme-api.herokuapp.com/gimme/FBI_Memes"
        ) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])


@pbot.on_message(filters.command("teenmemes|teenagers"))
async def teenagers(client, message):
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(
            "https://meme-api.herokuapp.com/gimme/teenagers"
        ) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])


@pbot.on_message(filters.command("hmeme"))
async def hmemes(client, message):
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(
            "https://meme-api.herokuapp.com/gimme/hornyresistance"
        ) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])


@pbot.on_message(filters.command("pewds"))
async def pewds(client, message):
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(
            "https://meme-api.herokuapp.com/gimme/PewdiepieSubmissions"
        ) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])


@pbot.on_message(filters.command("memes"))
async def memes(client, message):
    memereddit = random.choice(MemesReddit)
    meme_link = f"https://meme-api.herokuapp.com/gimme/{memereddit}"
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(meme_link) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])


@pbot.on_message(filters.command("hornyjail"))
async def hornyjail(client, message):
    async with aiohttp.ClientSession() as destiny_session:
        async with destiny_session.get(
            "https://meme-api.herokuapp.com/gimme/Hornyjail"
        ) as resp:
            r = await resp.json()
            await message.reply_photo(r["url"], caption=r["title"])
