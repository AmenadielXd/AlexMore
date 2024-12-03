import random
from datetime import datetime

import pytz
from pyrogram import enums, filters

from Alex import app
from pyrogram.types import Message
from utils.error import capture_err
from Alex.utils.database import get_couple, save_couple

# Date and time
def dt():
    # Set the timezone to Indian Standard Time
    ist_timezone = pytz.timezone("Asia/Kolkata")

    # Get the current time in IST
    ist_now = datetime.now(ist_timezone)

    dt_string = ist_now.strftime("%d/%m/%Y %H:%M")
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


def today():
    return str(dt()[0])


def tomorrow():
    return str(dt_tom())


@app.on_message(filters.command(["couple", "couples", "shipping"], prefixes=[".", "/", "!"]))
@capture_err
async def couple(_, message: Message):
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ᴡᴏʀᴋs ɪɴ ɢʀᴏᴜᴘs.")

    m = await message.reply("<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")

    try:
        chat_id = message.chat.id
        is_selected = await get_couple(chat_id, today())
        if not is_selected:
            list_of_users = []
            async for i in app.get_chat_members(chat_id):
                if not i.user.is_bot and not i.user.is_deleted:
                    list_of_users.append(i.user.id)

            if len(list_of_users) < 2:
                return await m.edit("Not enough users")

            c1_id = random.choice(list_of_users)
            c2_id = random.choice(list_of_users)
            while c1_id == c2_id:
                c1_id = random.choice(list_of_users)

            c1_mention = (await app.get_users(c1_id)).mention
            c2_mention = (await app.get_users(c2_id)).mention

            couple_selection_message = f"""<b>ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ:</b>
{c1_mention} + {c2_mention} = ❤️

<i>ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴍᴀʏ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {tomorrow()}</i>"""
            edited_message = await m.edit(couple_selection_message)
            couple = {"c1_id": c1_id, "c2_id": c2_id}
            await save_couple(chat_id, today(), couple)

            # Pin the message
            await edited_message.pin(disable_notification=True)

        elif is_selected:
            c1_id = int(is_selected["c1_id"])
            c2_id = int(is_selected["c2_id"])
            c1_name = (await app.get_users(c1_id)).first_name
            c2_name = (await app.get_users(c2_id)).first_name
            couple_selection_message = f"""ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ʜᴀs ʙᴇᴇɴ ᴄʜᴏsᴇɴ:
<a href='tg://openmessage?user_id={c1_id}'>{c1_name}</a> + <a href='tg://openmessage?user_id={c2_id}'>{c2_name}</a> = ❤️

<i>ɴᴇᴡ ᴄᴏᴜᴘʟᴇ ᴏғ ᴛʜᴇ ᴅᴀʏ ᴍᴀʏ ʙᴇ ᴄʜᴏsᴇɴ ᴀᴛ 12AM {tomorrow()}</i>"""
            edited_message = await m.edit(couple_selection_message)

            # Pin the message
            await edited_message.pin(disable_notification=True)

    except Exception as e:
        print(f"Error: {e}")
        await message.reply_text(str(e))