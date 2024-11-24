import os 
import random
from datetime import datetime 
from telegraph import upload_file
from PIL import Image, ImageDraw
from pyrogram import *
from pyrogram.enums import *

# BOT FILE NAME
from Alex import app as app

def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    dt_list = dt_string.split(" ")
    return dt_list


def dt_tom():
    a = (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/"
        + dt()[0].split("/")[1]
        + "/"
        + dt()[0].split("/")[2]
    )
    return a

tomorrow = str(dt_tom())
today = str(dt()[0])

@app.on_message(filters.command(["couples", "couple"], prefixes=["/", "!", ".", "@"]))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        await message.reply_text("⬤ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.")
        await message.delete()
        return
    
    try:
        msg = await message.reply_text("<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
        # GET LIST OF USERS
        list_of_users = []

        async for i in app.get_chat_members(message.chat.id, limit=50):
            if not i.user.is_bot:
                list_of_users.append(i.user.id)

        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c1_id = random.choice(list_of_users)

        photo1 = (await app.get_chat(c1_id)).photo
        photo2 = (await app.get_chat(c2_id)).photo

        N1 = (await app.get_users(c1_id)).mention 
        N2 = (await app.get_users(c2_id)).mention

        try:
            p1 = await app.download_media(photo1.big_file_id, file_name="pfp.png")
        except Exception:
            p1 = "Alex/assets/upic.png"
        try:
            p2 = await app.download_media(photo2.big_file_id, file_name="pfp1.png")
        except Exception:
            p2 = "Alex/assets/upic.png"

        img1 = Image.open(f"{p1}")
        img2 = Image.open(f"{p2}")

        img = Image.open("Alex/assets/COUPLES2.PNG")

        img1 = img1.resize((595, 595))
        img2 = img2.resize((595, 595))

        mask = Image.new('L', img1.size, 0)
        draw = ImageDraw.Draw(mask) 
        draw.ellipse((0, 0) + img1.size, fill=290)

        mask1 = Image.new('L', img2.size, 0)
        draw = ImageDraw.Draw(mask1) 
        draw.ellipse((0, 0) + img2.size, fill=290)

        img1.putalpha(mask)
        img2.putalpha(mask1)

        draw = ImageDraw.Draw(img)

        img.paste(img1, (96, 239), img1)
        img.paste(img2, (1220, 239), img2)

        img.save(f'test_{cid}.png')

        TXT = f"""
<blockquote>ㅤ   ◦•●◉✿ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ  ✿◉●•◦</blockquote>
▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱

 {N1} + {N2} = ♥︎

⬤ ɴᴇxᴛ ᴄᴏᴜᴘʟᴇ sᴇʟᴇᴄᴛᴇᴅ ᴏɴ {tomorrow}
▰▱▰▱▰▱▰▱▰▱▰▱▰▱▰▱
"""

        await message.reply_photo(f"test_{cid}.png", caption=TXT)
        await msg.delete()
        await message.delete()  # Delete user command message
        a = upload_file(f"test_{cid}.png")
        for x in a:
            img = "https://graph.org/" + x

    except Exception as e:
        print(str(e))
    try:
        os.remove(f"./downloads/pfp1.png")
        os.remove(f"./downloads/pfp2.png")
        os.remove(f"test_{cid}.png")
    except Exception:
        pass