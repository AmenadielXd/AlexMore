import os
import re

import requests
import yt_dlp
from pykeyboard import InlineKeyboard
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import (InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaVideo,
                            Message)

from config import BANNED_USERS, SONG_DOWNLOAD_DURATION_LIMIT, LOGGER_ID
from Alex import YouTube, app
from Alex.utils.decorators.language import language, languageCB
from Alex.utils.inline.song import song_markup


@app.on_message(
    filters.command(["video"])
    & filters.group
    & ~BANNED_USERS
)
@language
async def video_command_group(client, message: Message, _):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["P_B_5"],
                    url=f"https://t.me/{app.username}?start=video",
                ),
            ]
        ]
    )
    await message.reply_text(_["video_1"], reply_markup=upl)


@app.on_message(
    filters.command(["video"])
    & filters.private
    & ~BANNED_USERS
)
@language
async def video_command_private(client, message: Message, _):
    await message.delete()
    url = await YouTube.url(message)
    if url:
        if not await YouTube.exists(url):
            return await message.reply_text(_["video_5"])
        mystic = await message.reply_text(_["play_1"])
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(url)
        if str(duration_min) == "None":
            return await mystic.edit_text(_["video_3"])
        if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
            return await mystic.edit_text(
                _["play_4"].format(
                    SONG_DOWNLOAD_DURATION_LIMIT, duration_min
                )
            )
        buttons = song_markup(_, vidid)
        await mystic.delete()
        return await message.reply_photo(
            thumbnail,
            caption=_["video_4"].format(title),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["video_2"])
    mystic = await message.reply_text(_["play_1"])
    query = message.text.split(None, 1)[1]
    try:
        (
            title,
            duration_min,
            duration_sec,
            thumbnail,
            vidid,
        ) = await YouTube.details(query)
    except:
        return await mystic.edit_text(_["play_3"])
    if str(duration_min) == "None":
        return await mystic.edit_text(_["video_3"])
    if int(duration_sec) > SONG_DOWNLOAD_DURATION_LIMIT:
        return await mystic.edit_text(
            _["play_6"].format(SONG_DOWNLOAD_DURATION_LIMIT, duration_min)
        )
    buttons = song_markup(_, vidid)
    await mystic.delete()
    return await message.reply_photo(
        thumbnail,
        caption=_["video_4"].format(title),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_back") & ~BANNED_USERS
)
@languageCB
async def video_back_helper(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    buttons = song_markup(_, vidid)
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(buttons)
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_helper") & ~BANNED_USERS
)
@languageCB
async def video_helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, vidid = callback_request.split("|")
    try:
        await CallbackQuery.answer(_["video_6"], show_alert=True)
    except:
        pass
    try:
        formats_available, link = await YouTube.formats(vidid, True)
    except Exception as e:
        print(e)
        return await CallbackQuery.edit_message_text(_["video_7"])
    keyboard = InlineKeyboard()
    done = [160, 133, 134, 135, 136, 137, 298, 299, 264, 304, 266]
    for x in formats_available:
        check = x["format"]
        if x["filesize"] is None:
            continue
        if int(x["format_id"]) not in done:
            continue
        sz = convert_bytes(x["filesize"])
        ap = check.split("-")[1]
        to = f"{ap} = {sz}"
        keyboard.row(
            InlineKeyboardButton(
                text=to,
                callback_data=f"song_download {stype}|{x['format_id']}|{vidid}",
            )
        )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data=f"song_back {stype}|{vidid}",
        ),
        InlineKeyboardButton(
            text=_["CLOSE_BUTTON"], callback_data=f"close"
        ),
    )
    return await CallbackQuery.edit_message_reply_markup(
        reply_markup=keyboard
    )


@app.on_callback_query(
    filters.regex(pattern=r"song_download") & ~BANNED_USERS
)
@languageCB
async def video_download_cb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Downloading")
    except:
        pass
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    stype, format_id, vidid = callback_request.split("|")
    mystic = await CallbackQuery.edit_message_text(_["video_8"])
    yturl = f"https://www.youtube.com/watch?v={vidid}"

    # Specify the path to your cookies file
    cookie_file_path = "alexa.txt"  # Update this to your actual cookies file path

    # Add the cookie file to yt-dlp options
    ydl_opts = {
        "quiet": True,
        "cookiefile": cookie_file_path,  # Include cookies here
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ytdl:
        x = ytdl.extract_info(yturl, download=False)

    title = (x["title"]).title()
    title = re.sub("\W+", " ", title)
    thumb_image_path = await CallbackQuery.message.download()
    duration = x["duration"]

    thumb_image_path = await CallbackQuery.message.download()
    width = CallbackQuery.message.photo.width
    height = CallbackQuery.message.photo.height
    try:
        file_path = await YouTube.download(
            yturl,
            mystic,
            songvideo=True,
            format_id=format_id,
            title=title,
        )
    except Exception as e:
        return await mystic.edit_text(_["video_9"].format(e))

    med = InputMediaVideo(
        media=file_path,
        duration=duration,
        width=width,
        height=height,
        thumb=thumb_image_path,
        caption=title,
        supports_streaming=True,
    )

    await mystic.edit_text(_["video_11"])
    await app.send_chat_action(
        chat_id=CallbackQuery.message.chat.id,
        action=ChatAction.UPLOAD_VIDEO,
    )
    try:
        await CallbackQuery.edit_message_media(media=med)
    except Exception as e:
        print(e)
        return await mystic.edit_text(_["video_10"])
    os.remove(file_path)

import os
import requests
from pyrogram import Client, filters
from Alex import app

def fetch_song(song_name):
    url = f"https://song-teleservice.vercel.app/song?songName={song_name.replace(' ', '%20')}"
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 and "downloadLink" in response.json() else None
    except Exception as e:
        print(f"API Error: {e}")
        return None

@app.on_message(filters.command(["song"], prefixes=["/", "!", ".", ""]))
async def handle_song(client, message):
    song_name = message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    if not song_name:
        return await message.reply("<b>ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ sᴏɴɢ ɴᴀᴍᴇ . . .</b>")

    song_info = fetch_song(song_name)
    if not song_info:
        return await message.reply(f"sᴏʀʀʏ, ɪ ᴄᴏᴜʟᴅɴ'ᴛ ғɪɴᴅ ᴛʜᴇ sᴏɴɢ '{song_name}'.")

    filename = f"{song_info['trackName']}.mp3"
    download_url = song_info['downloadLink']

    # Download and save the file
    with requests.get(download_url, stream=True) as r, open(filename, "wb") as file:
        for chunk in r.iter_content(1024):
            if chunk:
                file.write(chunk)

    # Caption removed
    caption = ""

    # Send audio and clean up
    await message.reply_audio(audio=open(filename, "rb"), caption=caption)
    os.remove(filename)



@app.on_message(filters.command(["insta", "ig", "instagram", "reel"], prefixes=["!", "/", "."]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "<b>ᴘᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴍᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ᴜʀʟ</b>"
        )
        return
    url = message.text.split()[1]
    if not re.match(
        re.compile(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$"), url
    ):
        return await message.reply_text(
            "ᴛʜᴇ <b>ɪɴsᴛᴀɢʀᴀᴍ ᴜʀʟ</b> ʏᴏᴜ ʜᴀᴠᴇ ᴘʀᴏᴠɪᴅᴇᴅ  ɪsɴ'ᴛ ᴍᴀᴛᴄʜɪɴɢ ᴛʜᴇ <b>ɪɴsᴛᴀɢʀᴀᴍ ᴜʀʟ</b>"
        )
    a = await message.reply_text("<b>ᴘʀᴏᴄᴇssɪɴɢ . . .</b>")
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    response = requests.get(api_url)
    try:
        result = response.json()
        data = result["result"]
    except Exception as e:
        f = f"<b>ᴇʀʀᴏʀ :</b>\n{e}"
        try:
            await a.edit(f)
        except Exception:
            await message.reply_text(f)
            return await app.send_message(LOGGER_ID, f)
        return await app.send_message(LOGGER_ID, f)
    if not result["error"]:
        video_url = data["url"]
        duration = data["duration"]
        quality = data["quality"]
        type = data["extension"]
        size = data["formattedSize"]
        caption = f"<b>ᴅᴜʀᴀᴛɪᴏɴ :</> {duration}\n<b>ǫᴜᴀʟɪᴛʏ :</b> {quality}\n<b>ᴛʏᴘᴇ :</b> {type}\n<b>sɪᴢᴇ :</b> {size}"
        await a.delete()
        await message.reply_video(video_url, caption=caption)
    else:
        try:
            return await a.edit("ᴅᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ")
        except Exception:
            return await message.reply_text("ᴅᴏᴡɴʟᴏᴀᴅ ғᴀɪʟᴇᴅ")