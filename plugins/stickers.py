import base64
import textwrap
import imghdr
from httpx import AsyncClient, Timeout
import os
from pyrogram import filters
from asyncio import gather
from config import BOT_USERNAME
from Alex import app
from pyrogram import Client, filters
import pyrogram
from uuid import uuid4
from pyrogram.types import Message InlineKeyboardButton,InlineKeyboardMarkup
from io import BytesIO
from traceback import format_exc
from PIL import Image, ImageDraw, ImageFont
from pyrogram.errors import (
    PeerIdInvalid,
    ShortnameOccupyFailed,
    StickerEmojiInvalid,
    StickerPngDimensions,
    StickerPngNopng,
    UserIsBlocked,
)
from utils.error import capture_err
from utils.files import (
    get_document_from_file_id,
    resize_file_to_sticker_size,
    upload_document,
)
from Alex.utils.stickerset import (
    add_sticker_to_set,
    create_sticker,
    create_sticker_set,
    get_sticker_set_by_name,
)

# -----------

MAX_STICKERS = (
    120  # would be better if we could fetch this limit directly from telegram
)
SUPPORTED_TYPES = ["jpeg", "png", "webp"]
# ------------------------------------------
@app.on_message(filters.command("get_sticker"))
@capture_err
async def sticker_image(_, message: Message):
    r = message.reply_to_message

    if not r:
        return await message.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ.")

    if not r.sticker:
        return await message.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ.")

    m = await message.reply("sᴇɴᴅɪɴɢ . . .")
    f = await r.download(f"{r.sticker.file_unique_id}.png")

    await gather(
        *[
            message.reply_photo(f),
            message.reply_document(f),
        ]
    )

    await m.delete()
    os.remove(f)
#----------------
@app.on_message(filters.command("kang"))
@capture_err
async def kang(client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴏʀ ɪᴍᴀɢᴇ ᴛᴏ ᴋᴀɴɢ ɪᴛ.")
    if not message.from_user:
        return await message.reply_text(
            "ɴᴏᴜ ᴀʀᴇ ᴀɴᴏɴ ᴀᴅᴍɪɴ, ᴋᴀɴɢ sᴛɪᴄᴋᴇʀs ɪɴ ᴍʏ ᴘᴍ."
        )
    msg = await message.reply_text("<b>ᴋᴀɴɢɪɴɢ sᴛɪᴄᴋᴇʀ . . .</b>")

    # Find the proper emoji
    args = message.text.split()
    if len(args) > 1:
        sticker_emoji = str(args[1])
    elif (
        message.reply_to_message.sticker
        and message.reply_to_message.sticker.emoji
    ):
        sticker_emoji = message.reply_to_message.sticker.emoji
    else:
        sticker_emoji = "🙂"

    # Get the corresponding fileid, resize the file if necessary
    doc = message.reply_to_message.photo or message.reply_to_message.document
    try:
        if message.reply_to_message.sticker:
            sticker = await create_sticker(
                await get_document_from_file_id(
                    message.reply_to_message.sticker.file_id
                ),
                sticker_emoji,
            )
        elif doc:
            if doc.file_size > 10000000:
                return await msg.edit("ғɪʟᴇ sɪᴢᴇ ᴛᴏᴏ ʟᴀʀɢᴇ.")

            temp_file_path = await app.download_media(doc)
            image_type = imghdr.what(temp_file_path)
            if image_type not in SUPPORTED_TYPES:
                return await msg.edit(
                    "ғᴏʀᴍᴀᴛ ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ! ({})".format(image_type)
                )
            try:
                temp_file_path = await resize_file_to_sticker_size(
                    temp_file_path
                )
            except OSError as e:
                await msg.edit_text("Something wrong happened.")
                raise Exception(
                    f"Something went wrong while resizing the sticker (at {temp_file_path}); {e}"
                )
            sticker = await create_sticker(
                await upload_document(client, temp_file_path, message.chat.id),
                sticker_emoji,
            )
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
        else:
            return await msg.edit("Nope, can't kang that.")
    except ShortnameOccupyFailed:
        await message.reply_text("Change Your Name Or Username")
        return

    except Exception as e:
        await message.reply_text(str(e))
        e = format_exc()
        return print(e)
#-------
    packnum = 0
    packname = "f" + str(message.from_user.id) + "_by_" + BOT_USERNAME
    limit = 0
    try:
        while True:
            # Prevent infinite rules
            if limit >= 50:
                return await msg.delete()

            stickerset = await get_sticker_set_by_name(client, packname)
            if not stickerset:
                stickerset = await create_sticker_set(
                    client,
                    message.from_user.id,
                    f"{message.from_user.first_name[:32]}'s kang pack",
                    packname,
                    [sticker],
                )
            elif stickerset.set.count >= MAX_STICKERS:
                packnum += 1
                packname = (
                    "f"
                    + str(packnum)
                    + "_"
                    + str(message.from_user.id)
                    + "_by_"
                    + BOT_USERNAME
                )
                limit += 1
                continue
            else:
                try:
                    await add_sticker_to_set(client, stickerset, sticker)
                except StickerEmojiInvalid:
                    return await msg.edit("[ERROR]: INVALID_EMOJI_IN_ARGUMENT")
            limit += 1
            break

        await msg.edit(
    f"<b>sᴛɪᴄᴋᴇʀ ᴀᴅᴅᴇᴅ ᴛᴏ <a href='t.me/addstickers/{packname}'>ᴘᴀᴄᴋ</a></b>\n"
    f"<b>ᴇᴍᴏJɪ</b>: {sticker_emoji}"
)
    except (PeerIdInvalid, UserIsBlocked):
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Start", url=f"t.me/{BOT_USERNAME}")]]
        )
        await msg.edit(
            "ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ sᴛᴀʀᴛ ᴀ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ᴡɪᴛʜ ᴍᴇ.",
            reply_markup=keyboard,
        )
    except StickerPngNopng:
        await message.reply_text(
            "sᴛɪᴄᴋᴇʀs ᴍᴜsᴛ ʙᴇ ᴘɴɢ ғɪʟᴇs ʙᴜᴛ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ɪᴍᴀɢᴇ ᴡᴀs ɴᴏᴛ ᴀ ᴘɴɢ"
        )
    except StickerPngDimensions:
        await message.reply_text("ᴛʜᴇ sᴛɪᴄᴋᴇʀ ᴘɴɢ ᴅɪᴍᴇɴsɪᴏɴs ᴀʀᴇ ɪɴᴠᴀʟɪᴅ.")


######### sticker id

@app.on_message(filters.command("st"))
def generate_sticker(client, message):
    if len(message.command) == 2:
        sticker_id = message.command[1]
        try:
            client.send_sticker(message.chat.id, sticker=sticker_id)
        except Exception as e:
            message.reply_text(f"Error: {e}")
    else:
        message.reply_text("Please provide a sticker ID after /st command.")


#---------

@app.on_message(filters.command("packkang"))
async def _packkang(app :app,message):  
    txt = await message.reply_text("<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
    if not message.reply_to_message:
        await txt.edit('ʀᴇᴘʟʏ ᴛᴏ ᴍᴇssᴀɢᴇ')
        return
    if not message.reply_to_message.sticker:
        await txt.edit('ʀᴇᴘʟʏ ᴛᴏ sᴛɪᴄᴋᴇʀ')
        return
    if message.reply_to_message.sticker.is_animated or  message.reply_to_message.sticker.is_video:
        return await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ɴᴏɴ-ᴀɴɪᴍᴀᴛᴇᴅ sᴛɪᴄᴋᴇʀ")
    if len(message.command) < 2:
        pack_name =  f'{message.from_user.first_name}_sticker_pack_by_@{BOT_USERNAME}'
    else :
        pack_name = message.text.split(maxsplit=1)[1]
    short_name = message.reply_to_message.sticker.set_name
    stickers = await app.invoke(
        pyrogram.raw.functions.messages.GetStickerSet(
            stickerset=pyrogram.raw.types.InputStickerSetShortName(
                short_name=short_name),
            hash=0))
    shits = stickers.documents
    sticks = []

    for i in shits:
        sex = pyrogram.raw.types.InputDocument(
                id=i.id,
                access_hash=i.access_hash,
                file_reference=i.thumbs[0].bytes
            )

        sticks.append(
            pyrogram.raw.types.InputStickerSetItem(
                document=sex,
                emoji=i.attributes[1].alt
            )
        )

    try:
        short_name = f'stikcer_pack_{str(uuid4()).replace("-","")}_by_{app.me.username}'
        user_id = await app.resolve_peer(message.from_user.id)
        await app.invoke(
            pyrogram.raw.functions.stickers.CreateStickerSet(
                user_id=user_id,
                title=pack_name,
                short_name=short_name,
                stickers=sticks,
            )
        )
        await txt.edit(f"<b>ʜᴇʀᴇ ɪs ʏᴏᴜʀ ᴋᴀɴɢᴇᴅ ʟɪɴᴋ</b>!\n<b>ᴛᴏᴛᴀʟ sᴛɪᴄᴋᴇʀ </b>: {len(sticks)}",reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴘᴀᴄᴋ ʟɪɴᴋ",url=f"http://t.me/addstickers/{short_name}")]]))
    except Exception as e:
        await message.reply(str(e))


###### sticker id =
@app.on_message(filters.command(["stickerid","stid"]))
async def sticker_id(app: app, msg):
    if not msg.reply_to_message:
        await msg.reply_text("Reply to a sticker")        
    elif not msg.reply_to_message.sticker:
        await msg.reply_text("Reply to a sticker")        
    st_in = msg.reply_to_message.sticker
    await msg.reply_text(f"""
<u><b>sᴛɪᴄᴋᴇʀ ɪɴғᴏ</b></u>
<b>● sᴛɪᴄᴋᴇʀ ɪᴅ ➠</b> <code>{st_in.file_id}</code>\n
<b>● sᴛɪᴄᴋᴇʀ ᴜɴɪǫᴜᴇ ɪᴅ ➠</b> <code>{st_in.file_unique_id}</code>
""")


#####




@app.on_message(filters.command("mmf"))
async def mmf(_, message: Message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message

    if len(message.text.split()) < 2:
        await message.reply_text("<b>ɢɪᴠᴇ ᴍᴇ ᴛᴇxᴛ ᴀғᴛᴇʀ /mmf ᴛᴏ ᴍᴇᴍɪғʏ.</b>")
        return

    msg = await message.reply_text("<b>ᴍᴇᴍɪғʏɪɴɢ ᴛʜɪs ɪᴍᴀɢᴇ!</b>")
    text = message.text.split(None, 1)[1]
    file = await app.download_media(reply_message)

    meme = await drawText(file, text)
    await app.send_document(chat_id, document=meme)

    await msg.delete()

    os.remove(meme)


async def drawText(image_path, text):
    img = Image.open(image_path)

    os.remove(image_path)

    i_width, i_height = img.size

    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "./Alex/assets/default.ttf"

    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    draw = ImageDraw.Draw(img)

    current_h, pad = 10, 5

    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)

            draw.text(
                xy=(((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)

            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    image_name = "memify.webp"

    webp_file = os.path.join(image_name)

    img.save(webp_file, "webp")

    return webp_file


fetch = AsyncClient(
    http2=True,
    verify=False,
    headers={
        "Accept-Language": "id-ID",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edge/107.0.1418.42",
    },
    timeout=Timeout(20),
)
# ------------------------------------------------------------------------
class QuotlyException(Exception):
    pass
# --------------------------------------------------------------------------
async def get_message_sender_id(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_sender_name:
            return 1
        elif ctx.forward_from:
            return ctx.forward_from.id
        elif ctx.forward_from_chat:
            return ctx.forward_from_chat.id
        else:
            return 1
    elif ctx.from_user:
        return ctx.from_user.id
    elif ctx.sender_chat:
        return ctx.sender_chat.id
    else:
        return 1
# -----------------------------------------------------------------------------------------
async def get_message_sender_name(ctx: Message):
    if ctx.forward_date:
        if ctx.forward_sender_name:
            return ctx.forward_sender_name
        elif ctx.forward_from:
            return (
                f"{ctx.forward_from.first_name} {ctx.forward_from.last_name}"
                if ctx.forward_from.last_name
                else ctx.forward_from.first_name
            )
# ---------------------------------------------------------------------------------------------------
        elif ctx.forward_from_chat:
            return ctx.forward_from_chat.title
        else:
            return ""
    elif ctx.from_user:
        if ctx.from_user.last_name:
            return f"{ctx.from_user.first_name} {ctx.from_user.last_name}"
        else:
            return ctx.from_user.first_name
    elif ctx.sender_chat:
        return ctx.sender_chat.title
    else:
        return ""
# ---------------------------------------------------------------------------------------------------
async def get_custom_emoji(ctx: Message):
    if ctx.forward_date:
        return (
            ""
            if ctx.forward_sender_name
            or not ctx.forward_from
            and ctx.forward_from_chat
            or not ctx.forward_from
            else ctx.forward_from.emoji_status.custom_emoji_id
        )

    return ctx.from_user.emoji_status.custom_emoji_id if ctx.from_user else ""

# ---------------------------------------------------------------------------------------------------
async def get_message_sender_username(ctx: Message):
    if ctx.forward_date:
        if (
            not ctx.forward_sender_name
            and not ctx.forward_from
            and ctx.forward_from_chat
            and ctx.forward_from_chat.username
        ):
            return ctx.forward_from_chat.username
        elif (
            not ctx.forward_sender_name
            and not ctx.forward_from
            and ctx.forward_from_chat
            or ctx.forward_sender_name
            or not ctx.forward_from
        ):
            return ""
        else:
            return ctx.forward_from.username or ""
    elif ctx.from_user and ctx.from_user.username:
        return ctx.from_user.username
    elif (
        ctx.from_user
        or ctx.sender_chat
        and not ctx.sender_chat.username
        or not ctx.sender_chat
    ):
        return ""
    else:
        return ctx.sender_chat.username
# ------------------------------------------------------------------------
async def get_message_sender_photo(ctx: Message):
    if ctx.forward_date:
        if (
            not ctx.forward_sender_name
            and not ctx.forward_from
            and ctx.forward_from_chat
            and ctx.forward_from_chat.photo
        ):
            return {
                "small_file_id": ctx.forward_from_chat.photo.small_file_id,
                "small_photo_unique_id": ctx.forward_from_chat.photo.small_photo_unique_id,
                "big_file_id": ctx.forward_from_chat.photo.big_file_id,
                "big_photo_unique_id": ctx.forward_from_chat.photo.big_photo_unique_id,
            }
        elif (
            not ctx.forward_sender_name
            and not ctx.forward_from
            and ctx.forward_from_chat
            or ctx.forward_sender_name
            or not ctx.forward_from
        ):
            return ""
        else:
            return (
                {
                    "small_file_id": ctx.forward_from.photo.small_file_id,
                    "small_photo_unique_id": ctx.forward_from.photo.small_photo_unique_id,
                    "big_file_id": ctx.forward_from.photo.big_file_id,
                    "big_photo_unique_id": ctx.forward_from.photo.big_photo_unique_id,
                }
                if ctx.forward_from.photo
                else ""
            )
# ---------------------------------------------------------------------------------
    elif ctx.from_user and ctx.from_user.photo:
        return {
            "small_file_id": ctx.from_user.photo.small_file_id,
            "small_photo_unique_id": ctx.from_user.photo.small_photo_unique_id,
            "big_file_id": ctx.from_user.photo.big_file_id,
            "big_photo_unique_id": ctx.from_user.photo.big_photo_unique_id,
        }
    elif (
        ctx.from_user
        or ctx.sender_chat
        and not ctx.sender_chat.photo
        or not ctx.sender_chat
    ):
        return ""
    else:
        return {
            "small_file_id": ctx.sender_chat.photo.small_file_id,
            "small_photo_unique_id": ctx.sender_chat.photo.small_photo_unique_id,
            "big_file_id": ctx.sender_chat.photo.big_file_id,
            "big_photo_unique_id": ctx.sender_chat.photo.big_photo_unique_id,
        }
# ---------------------------------------------------------------------------------------------------
async def get_text_or_caption(ctx: Message):
    if ctx.text:
        return ctx.text
    elif ctx.caption:
        return ctx.caption
    else:
        return ""
# ---------------------------------------------------------------------------------------------------
async def pyrogram_to_quotly(messages, is_reply):
    if not isinstance(messages, list):
        messages = [messages]
    payload = {
        "type": "quote",
        "format": "png",
        "backgroundColor": "#1b1429",
        "messages": [],
    }
# ------------------------------------------------------------------------------------------------------------
    for message in messages:
        the_message_dict_to_append = {}
        if message.entities:
            the_message_dict_to_append["entities"] = [
                {
                    "type": entity.type.name.lower(),
                    "offset": entity.offset,
                    "length": entity.length,
                }
                for entity in message.entities
            ]
        elif message.caption_entities:
            the_message_dict_to_append["entities"] = [
                {
                    "type": entity.type.name.lower(),
                    "offset": entity.offset,
                    "length": entity.length,
                }
                for entity in message.caption_entities
            ]
        else:
            the_message_dict_to_append["entities"] = []
        the_message_dict_to_append["chatId"] = await get_message_sender_id(message)
        the_message_dict_to_append["text"] = await get_text_or_caption(message)
        the_message_dict_to_append["avatar"] = True
        the_message_dict_to_append["from"] = {}
        the_message_dict_to_append["from"]["id"] = await get_message_sender_id(message)
        the_message_dict_to_append["from"]["name"] = await get_message_sender_name(
            message
        )
        the_message_dict_to_append["from"][
            "username"
        ] = await get_message_sender_username(message)
        the_message_dict_to_append["from"]["type"] = message.chat.type.name.lower()
        the_message_dict_to_append["from"]["photo"] = await get_message_sender_photo(
            message
        )
        if message.reply_to_message and is_reply:
            the_message_dict_to_append["replyMessage"] = {
                "name": await get_message_sender_name(message.reply_to_message),
                "text": await get_text_or_caption(message.reply_to_message),
                "chatId": await get_message_sender_id(message.reply_to_message),
            }
        else:
            the_message_dict_to_append["replyMessage"] = {}
        payload["messages"].append(the_message_dict_to_append)
    r = await fetch.post("https://bot.lyo.su/quote/generate.png", json=payload)
    if not r.is_error:
        return r.read()
    else:
        raise QuotlyException(r.json())
# ------------------------------------------------------------------------------------------

def isArgInt(txt) -> list:
    count = txt
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]

# ---------------------------------------------------------------------------------------------------
@app.on_message(filters.command(["q", "r"]) & filters.reply)
async def msg_quotly_cmd(self: app, ctx: Message):
    is_reply = False
    if ctx.command[0].endswith("r"):
        is_reply = True
    if len(ctx.text.split()) > 1:
        check_arg = isArgInt(ctx.command[1])
        if check_arg[0]:
            if check_arg[1] < 2 or check_arg[1] > 10:
                return await ctx.reply_msg("Invalid range", del_in=6)
            try:
                messages = [
                    i
                    for i in await self.get_messages(
                        chat_id=ctx.chat.id,
                        message_ids=range(
                            ctx.reply_to_message.id,
                            ctx.reply_to_message.id + (check_arg[1] + 5),
                        ),
                        replies=-1,
                    )
                    if not i.empty and not i.media
                ]
            except Exception:
                return await ctx.reply_text("🤷🏻‍♂️")
            try:
                make_quotly = await pyrogram_to_quotly(messages, is_reply=is_reply)
                bio_sticker = BytesIO(make_quotly)
                bio_sticker.name = "misskatyquote_sticker.webp"
                return await ctx.reply_sticker(bio_sticker)
            except Exception:
                return await ctx.reply_msg("🤷🏻‍♂️")
    try:
        messages_one = await self.get_messages(
            chat_id=ctx.chat.id, message_ids=ctx.reply_to_message.id, replies=-1
        )
        messages = [messages_one]
    except Exception:
        return await ctx.reply_msg("🤷🏻‍♂️")
    try:
        make_quotly = await pyrogram_to_quotly(messages, is_reply=is_reply)
        bio_sticker = BytesIO(make_quotly)
        bio_sticker.name = "misskatyquote_sticker.webp"
        return await ctx.reply_sticker(bio_sticker)
    except Exception as e:
        return await ctx.reply_msg(f"ERROR: {e}")
# ---------------------------------------------------------------------------------