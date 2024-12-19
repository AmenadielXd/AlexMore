import re
from Alex import app
from config import BOT_USERNAME
from utils.lucy_ban import admin_filter
from Alex.mongo.filtersdb import *
from utils.filters_func import GetFIlterMessage, get_text_reason, SendFilterMessage
from utils.yumidb import user_admin
from utils.yumidb import *
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("filter") & admin_filter)
@user_admin
async def _filter(client, message):

    chat_id = message.chat.id 
    if (
        message.reply_to_message
        and not len(message.command) == 2
    ):
        await message.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ɢɪᴠᴇ ᴛʜᴇ ғɪʟᴛᴇʀ ᴀ ɴᴀᴍᴇ!")  
        return 

    filter_name, filter_reason = get_text_reason(message)
    if (
        message.reply_to_message
        and not len(message.command) >=2
    ):
        await message.reply("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ɢɪᴠᴇ ᴛʜᴇ ғɪʟᴛᴇʀ sᴏᴍᴇ ᴄᴏɴᴛᴇɴᴛ!")
        return

    content, text, data_type = await GetFIlterMessage(message)
    await add_filter_db(chat_id, filter_name=filter_name, content=content, text=text, data_type=data_type)
    await message.reply(
        f"Saved filter '<code>{filter_name}</code>'."
    )


@app.on_message(~filters.bot & filters.group, group=4)
async def FilterCheckker(client, message):
    if not message.text:
        return
    text = message.text
    chat_id = message.chat.id
    if (
        len(await get_filters_list(chat_id)) == 0
    ):
        return

    ALL_FILTERS = await get_filters_list(chat_id)
    for filter_ in ALL_FILTERS:

        if (
            message.command
            and message.command[0] == 'filter'
            and len(message.command) >= 2
            and message.command[1] ==  filter_
        ):
            return

        pattern = r"( |^|[^\w])" + re.escape(filter_) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            filter_name, content, text, data_type = await get_filter(chat_id, filter_)
            await SendFilterMessage(
                message=message,
                filter_name=filter_,
                content=content,
                text=text,
                data_type=data_type
            )

@app.on_message(filters.command('filters') & filters.group)
async def _filters(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    if message.chat.type == 'private':
        chat_title = 'local'
    FILTERS = await get_filters_list(chat_id)

    if len(FILTERS) == 0:
        await message.reply(
            f'No filters in {chat_title}.'
        )
        return

    filters_list = f'List of filters in {chat_title}:\n'

    for filter_ in FILTERS:
        filters_list += f'- <code>{filter_}</code>\n'

    await message.reply(
        filters_list
    )


@app.on_message(filters.command('stopall') & admin_filter)
async def stopall(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    user = await client.get_chat_member(chat_id,message.from_user.id)
    if not user.status == ChatMemberStatus.OWNER :
        return await message.reply_text("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!!") 

    KEYBOARD = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='Delete all filters', callback_data='custfilters_stopall')],
        [InlineKeyboardButton(text='Cancel', callback_data='custfilters_cancel')]]
    )

    await message.reply(
        text=(f'ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴏᴘ <b>ᴀʟʟ</b> ғɪʟᴛᴇʀs ɪɴ {chat_title}? ᴛʜɪs ᴀᴄᴛɪᴏɴ ɪs ɪʀʀᴇᴠᴇʀsɪʙʟᴇ.'),
        reply_markup=KEYBOARD
    )


@app.on_callback_query(filters.regex("^custfilters_"))
async def stopall_callback(client, callback_query: CallbackQuery):  
    chat_id = callback_query.message.chat.id 
    query_data = callback_query.data.split('_')[1]  

    user = await client.get_chat_member(chat_id, callback_query.from_user.id)

    if not user.status == ChatMemberStatus.OWNER :
        return await callback_query.answer("ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs!!") 

    if query_data == 'stopall':
        await stop_all_db(chat_id)
        await callback_query.edit_message_text(text="ɪ'ᴠᴇ ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴄʜᴀᴛ ғɪʟᴛᴇʀs.")

    elif query_data == 'cancel':
        await callback_query.edit_message_text(text='Cancelled.')



@app.on_message(filters.command('stop') & admin_filter)
@user_admin
async def stop(client, message):
    chat_id = message.chat.id
    if not (len(message.command) >= 2):
        await message.reply('ᴜsᴇ ʜᴇʟᴘ ᴛᴏ ᴋɴᴏᴡ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴜsᴀɢᴇ')
        return

    filter_name = message.command[1]
    if (filter_name not in await get_filters_list(chat_id)):
        await message.reply("ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴀᴠᴇᴅ ᴀɴʏ ғɪʟᴛᴇʀs ᴏɴ ᴛʜɪs ᴡᴏʀᴅ ʏᴇᴛ!")
        return

    await stop_db(chat_id, filter_name)
    await message.reply(f"ɪ'ᴠᴇ sᴛᴏᴘᴘᴇᴅ <code>{filter_name}</code>.")