from Alex import app as app
from config import BOT_USERNAME, OWNER_USERNAME
from pyrogram import filters
from pyrogram.errors import Unauthorized
from pyrogram.types import (
    InlineQueryResultArticle, InputTextMessageContent,
    InlineKeyboardMarkup, InlineKeyboardButton
)

whisper_db = {}

switch_btn = InlineKeyboardMarkup([[InlineKeyboardButton("𝑆𝑒𝑐𝑟𝑒𝑡 𝐼𝑛𝑙𝑖𝑛𝑒", switch_inline_query_current_chat="")]])

async def _whisper(_, inline_query):
    data = inline_query.query
    results = []

    if len(data.split()) < 2:
        mm = [
            InlineQueryResultArticle(
                title="𝑊ℎ𝑖𝑠𝑝𝑒𝑟",
                description=f"@{BOT_USERNAME} [ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ ] [ ᴛᴇxᴛ ]",
                input_message_content=InputTextMessageContent(f"<u><b>ᴜsᴀɢᴇ:</u></b>\n\n@{BOT_USERNAME} [ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ ] [ ᴛᴇxᴛ ]"),
                thumb_url="https://files.catbox.moe/5pb5il.jpg",
                reply_markup=switch_btn
            )
        ]
    else:
        try:
            user_id = data.split()[0]
            msg = data.split(None, 1)[1]
        except IndexError:
            pass

        try:
            user = await _.get_users(user_id)
            whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔐 Show message", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}")]])
            one_time_whisper_btn = InlineKeyboardMarkup([[InlineKeyboardButton("🔐 Show message", callback_data=f"fdaywhisper_{inline_query.from_user.id}_{user.id}_one")]])
            mm = [
                InlineQueryResultArticle(
                    title="𝑊ℎ𝑖𝑠𝑝𝑒𝑟",
                    description=f"sᴇɴᴅ ᴀ ᴡʜɪsᴘᴇʀ ᴛᴏ {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"ᴀ ᴡʜɪsᴘᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ {user.first_name}.\nᴏɴʟʏ ᴛʜᴇʏ ᴄᴀɴ ʀᴇᴀᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ."),
                    thumb_url="https://files.catbox.moe/5pb5il.jpg",
                    reply_markup=whisper_btn
                ),
                InlineQueryResultArticle(
                    title="𝑂𝑛𝑒-𝑇𝑖𝑚𝑒 𝑊ℎ𝑖𝑠𝑝𝑒𝑟",
                    description=f"sᴇɴᴅ ᴀ ᴏɴᴇ-ᴛɪᴍᴇ ᴡʜɪsᴘᴇʀ ᴛᴏ {user.first_name}!",
                    input_message_content=InputTextMessageContent(f"ᴀ ᴏɴᴇ-ᴛɪᴍᴇ ᴡʜɪsᴘᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ {user.first_name}.\nᴏɴʟʏ ᴛʜᴇʏ ᴄᴀɴ ʀᴇᴀᴅ ᴛʜᴇ ᴍᴇssᴀɢᴇ."),
                    thumb_url="https://files.catbox.moe/5pb5il.jpg",
                    reply_markup=one_time_whisper_btn
                )
            ]
            whisper_db[f"{inline_query.from_user.id}_{user.id}"] = msg
        except:
            mm = [
                InlineQueryResultArticle(
                    title="𝑊ℎ𝑖𝑠𝑝𝑒𝑟",
                    description="ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ!",
                    input_message_content=InputTextMessageContent("ɪɴᴠᴀʟɪᴅ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ!"),
                    thumb_url="https://files.catbox.moe/5pb5il.jpg",
                    reply_markup=switch_btn
                )
            ]

    results.extend(mm)
    return results


@app.on_callback_query(filters.regex(pattern=r"fdaywhisper_(.*)"))
async def whispes_cb(_, query):
    data = query.data.split("_")
    from_user = int(data[1])
    to_user = int(data[2])
    user_id = query.from_user.id

    if user_id not in [from_user, to_user, 7202110938]:
        try:
            await _.send_message(from_user, f"{query.from_user.mention} is trying to open your whisper.")
        except Unauthorized:
            pass

        return await query.answer("ᴛʜɪs ᴡʜɪsᴘᴇʀ ɪs ɴᴏᴛ ғᴏʀ ʏᴏᴜ!", show_alert=True)

    search_msg = f"{from_user}_{to_user}"

    try:
        msg = whisper_db[search_msg]
    except:
        msg = "🚫 ᴇʀʀᴏʀ!\nᴡʜɪsᴘᴇʀ ʜᴀs ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴛʜᴇ ᴅᴀᴛᴀʙᴀsᴇ!"

    SWITCH = InlineKeyboardMarkup([[InlineKeyboardButton("Go Inline 🪝", switch_inline_query_current_chat="")]])

    await query.answer(msg, show_alert=True)

    if len(data) > 3 and data[3] == "one":
        if user_id == to_user:
            await query.edit_message_text("ᴡʜɪsᴘᴇʀ ʜᴀs ʙᴇᴇɴ ʀᴇᴀᴅ!")


async def in_help():
    answers = [
        InlineQueryResultArticle(
            title="𝑊ℎ𝑖𝑠𝑝𝑒𝑟",
            description=f"@{BOT_USERNAME} [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ] [ᴛᴇxᴛ]",
            input_message_content=InputTextMessageContent(f"🍥 <u><b>ᴜsᴀɢᴇ:</u></b>\n➥ @{BOT_USERNAME} (ᴛᴀʀɢᴇᴛ ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ɪᴅ) (ʏᴏᴜʀ ᴍᴇssᴀɢᴇ).\n<u><b>ᴇxᴀᴍᴘʟᴇ:</u></b>\n➥ <code>@{BOT_USERNAME} @{OWNER_USERNAME} ɪ ᴡᴀɴᴛ ʏᴏᴜ ᴋɴᴏᴡ ɪ ʟᴏᴠᴇ ʏᴏᴜ ᴛʜᴇ ᴍᴏsᴛ ♡゙</code>"),
            thumb_url="https://files.catbox.moe/5pb5il.jpg",
            reply_markup=switch_btn
        )
    ]
    return answers


@app.on_inline_query()
async def bot_inline(_, inline_query):
    string = inline_query.query.lower()

    if string.strip() == "":
        answers = await in_help()
        await inline_query.answer(answers)
    else:
        answers = await _whisper(_, inline_query)
        await inline_query.answer(answers, cache_time=0)