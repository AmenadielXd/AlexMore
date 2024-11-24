import requests
import asyncio
from pyrogram import filters
from pyrogram.types import Message,InlineKeyboardButton,InlineKeyboardMarkup
from pyrogram.enums import ChatAction
from pyrogram.enums import ChatType
from Alex import app
from strings import get_string, helpers
from config import BOT_USERNAME

LUCY = [
    [
        InlineKeyboardButton(text="ᴀᴅᴅ ᴍᴇ ʙᴀʙʏ", url=f"https://t.me/novauibot?startgroup=true"),
    ],
]

@app.on_message(filters.command("cosplay"))
async def cosplay(_,msg):
    img = requests.get("https://waifu-api.vercel.app").json()
    await msg.reply_photo(img, caption=f"<b>⬤ ᴄᴏsᴘʟᴀʏ ʙʏ ➠ {app.mention}</b>", reply_markup=InlineKeyboardMarkup(LUCY),)



@app.on_message(filters.command("ncosplay"))
async def ncosplay(_,msg):
    if msg.chat.type != ChatType.PRIVATE:
      await msg.reply_text("❍ sᴏʀʀʏ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ᴡɪᴛʜ ʙᴏᴛ",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("ɢᴏ ᴘᴍ",url=f"https://t.me/{app.me.username}?start=True")]
            ]
        ))
    else:
       ncosplay = requests.get("https://waifu-api.vercel.app/items/1").json()

       await msg.reply_photo(ncosplay, caption=f"<b>⬤ ᴄᴏsᴘʟᴀʏ ʙʏ ➠ {app.mention}</b>", reply_markup=InlineKeyboardMarkup(LUCY),)


@app.on_message(filters.command("nude"))
async def nude(_, msg):
    if msg.chat.type != ChatType.PRIVATE:
        await msg.reply_text(
            "❍ sᴏʀʀʏ ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ɪɴ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ᴡɪᴛʜ ʙᴏᴛ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton("ɢᴏ ᴘᴍ", url=f"https://t.me/{app.me.username}?start=True")]
                ]
            )
        )
    else:
        # Fetch data from Night API
        try:
            response = requests.get(
                "https://api.night-api.com/images/nsfw",
                headers={"authorization": "pUieNWJRIs-2Q073qw9dddUcM3Vncmn-eusGidDCIw"}
            )
            data = response.json()
            nude_image_url = data.get("content", {}).get("url")  # Ensure correct key structure

            if nude_image_url:
                sent_message = await msg.reply_photo(
                    nude_image_url,
                    caption=f"<b>⬤ ɴᴜᴅᴇ ᴘɪᴄs ʙʏ ➠ {app.mention}</b>",
                    reply_markup=InlineKeyboardMarkup(LUCY)
                )

                # Delete the message after 5 minutes
                await asyncio.sleep(300)  # 300 seconds = 5 minutes
                await sent_message.delete()

            else:
                await msg.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ɴ*ᴅᴇ ɪᴍᴀɢᴇ. ᴘʟᴇᴀsᴇ ᴛʀʏ ᴀɢᴀɪɴ ʟᴀᴛᴇʀ.")
        except Exception as e:
            await msg.reply_text(f"<b>ᴇʀʀᴏʀ:</b> {str(e)}")