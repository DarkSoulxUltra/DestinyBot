import os
from PIL import Image, ImageDraw, ImageFont
from DestinyBot.events import register
from DestinyBot.modules.helper_funcs.managers import edit_delete, edit_or_reply


@register(pattern=r"^/write ?(.*)")
async def writer(e):
    if e.reply_to:
        reply = await e.get_reply_message()
        text = reply.message
    elif e.pattern_match.group(1):
        text = e.text.split(maxsplit=1)[1]
    else:
        return await edit_delete(e, "`Give me something to write..`")
    await edit_delete(e, "`Matte-Kudasai, writing....`")
    img = Image.open("DestinyBot/resources/template.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DestinyBot/resources/fonts/assfont.ttf", 30)
    x, y = 150, 140
    line_height = font.getsize("hg")[1]
    draw.text((x, y), text, fill=(1, 22, 55), font=font)
    y = y + line_height - 5
    file = "pic.jpg"
    img.save(file)
    await e.reply(file=file)
    os.remove(file)


__mod_name__ = "Write"

__help__ = """
*Write Text*
 ✮ /write <text>*:* To get image of handwriting text mentioned infront or replied to.
 ✮ /write (reply this to some text)*:* Reply it to some text to get a page of handwritten text.
"""
