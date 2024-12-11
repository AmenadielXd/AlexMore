import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPrivileges, ChatPrivileges
from pyrogram.errors import RPCError
from Alex import app

# manually adminstrator
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

temporary_permissions = {}
temporary_messages = {}

@app.on_message(filters.command('admin') & filters.group)
async def promote_user(client, message):
    chat_id = message.chat.id
    bot_user = await client.get_me()

    try:
        bot_member = await client.get_chat_member(chat_id, bot_user.id)
        if not bot_member.privileges.can_promote_members:
            await client.send_message(chat_id, "ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇᴍʙᴇʀꜱ.")
            return
    except Exception as e:
        await client.send_message(chat_id, f"Error retrieving bot status: {e}")
        logger.error(f"Error retrieving bot status: {e}")
        return

    user_member = await client.get_chat_member(chat_id, message.from_user.id)

    if not user_member.privileges:
        await client.send_message(chat_id, "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ.")
        return

    if not user_member.privileges.can_promote_members:
        await client.send_message(chat_id, "ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴅᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛ.")
        return

    target_user_id = await get_target_user_id(client, chat_id, message)
    if target_user_id is None:
        return

    if target_user_id not in temporary_permissions:
        temporary_permissions[target_user_id] = initialize_permissions(bot_member.privileges)

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🕹 ᴘᴇʀᴍɪꜱꜱɪᴏɴꜱ", callback_data=f"admin|permissions|{target_user_id}"),
         InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data=f"admin|close|{target_user_id}")]
    ])

    await client.send_message(chat_id, "Select an option:", reply_markup=markup)

@app.on_callback_query(filters.regex(r"admin\|permissions\|"))
async def show_permissions(client, callback_query: CallbackQuery):
    user_member = await client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)

    if not user_member.privileges or not user_member.privileges.can_promote_members:
        await callback_query.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴜꜱᴇʀ ᴘʀᴏᴍᴏᴛɪɴɢ ʀɪɢʜᴛ.", show_alert=True)
        return

    target_user_id = int(callback_query.data.split("|")[-1])
    chat_id = callback_query.message.chat.id

    target_member = await client.get_chat_member(chat_id, target_user_id)
    target_user_name = target_member.user.first_name or target_member.user.username or "User"
    group_name = (await client.get_chat(chat_id)).title

    bot_user = await client.get_me()
    bot_member = await client.get_chat_member(chat_id, bot_user.id)
    bot_privileges = bot_member.privileges  # Get the bot's privileges

    markup = await create_permission_markup(target_user_id, bot_privileges, callback_query)

    await callback_query.message.edit_text(
        f"👤 {target_user_name} [{target_user_id}]\n👥 {group_name}",
        reply_markup=markup
    )
    await callback_query.answer()

@app.on_callback_query(filters.regex(r"admin\|"))
async def handle_permission_toggle(client, callback_query: CallbackQuery):
    data = callback_query.data.split("|")

    if len(data) < 3:
        await callback_query.answer("Invalid callback data. Please try again.", show_alert=True)
        logger.error(f"Invalid callback data received: {callback_query.data}")
        return

    action = data[1]
    target_user_id = int(data[-1])

    user_member = await callback_query._client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
    if not user_member.privileges or not user_member.privileges.can_promote_members:
        await callback_query.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴜꜱᴇʀ ᴘʀᴏᴍᴏᴛɪɴɢ ʀɪɢʜᴛ.", show_alert=True)
        return

    if action == "toggle":
        await toggle_permission(callback_query, target_user_id, data[2])
    elif action == "save":
        await save_permissions(callback_query._client, callback_query, target_user_id)
    elif action == "close":
        await close_permission_selection(callback_query)

# set title
@app.on_message(filters.command(["title"], prefixes=["!", "/", "."]) & filters.group)
async def set_admin_title(client, message):
    chat_id = message.chat.id
    bot_user = await client.get_me()

    try:
        # Check if the bot has the privilege to change admin titles
        bot_member = await client.get_chat_member(chat_id, bot_user.id)
        if not bot_member.privileges.can_promote_members:
            await message.reply("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ᴀᴅᴍɪɴ ꜱᴛᴀᴛᴜꜱ ᴏʀ ᴛɪᴛʟᴇꜱ.")
            return
    except Exception as e:
        await message.reply(f"Error retrieving bot status: {e}")
        return

    # Check if the user who sent the command has the right to promote members
    user_member = await client.get_chat_member(chat_id, message.from_user.id)
    if not user_member.privileges or not user_member.privileges.can_promote_members:
        await message.reply("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴄʜᴀɴɢᴇ ᴀᴅᴍɪɴ ᴛɪᴛʟᴇꜱ.")
        return

    # Parse the title from the command
    if len(message.command) < 2:
        await message.reply("ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴛɪᴛʟᴇ ꜰᴏʀ ᴛʜᴇ ᴀᴅᴍɪɴ.")
        return

    title = " ".join(message.command[1:])
    if len(title) > 16:
        await message.reply("ᴛʜᴇ ᴛɪᴛʟᴇ ᴄᴀɴ'ᴛ ʙᴇ ᴍᴏʀᴇ ᴛʜᴀɴ 16 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ.")
        return

    # Check if the command is a reply to a user
    if not message.reply_to_message:
        await message.reply("ᴘʟᴇᴀꜱᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ᴀᴅᴍɪɴ ᴛᴏ ꜱᴇᴛ ᴛʜᴇɪʀ ᴛɪᴛʟᴇ.")
        return

    target_user_id = message.reply_to_message.from_user.id

    try:
        # Set the admin's custom title
        await client.set_administrator_title(chat_id, target_user_id, title)
        await message.reply(f"ᴛɪᴛʟᴇ ᴄʜᴀɴɢᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴛᴏ: <b>{title}</b>")
    except RPCError as e:
        await message.reply(f"ꜰᴀɪʟᴇᴅ ᴛᴏ ꜱᴇᴛ ᴛɪᴛʟᴇ: {str(e)}")