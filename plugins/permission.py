import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ChatPrivileges, ChatPrivileges
from pyrogram.errors import RPCError
from Alex import app
from config import OWNER_ID
from pyrogram.enums import ChatMembersFilter


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

async def get_target_user_id(client, chat_id, message):
    if message.reply_to_message:
        return message.reply_to_message.from_user.id

    if len(message.command) > 1:
        target_identifier = message.command[1]
        if target_identifier.isdigit():
            return int(target_identifier)

        try:
            target_user = await client.get_chat_member(chat_id, target_identifier.replace('@', ''))
            return target_user.user.id
        except Exception:
            await client.send_message(chat_id, "ᴜꜱᴇʀ ɴᴏᴛ ꜰᴏᴜɴᴅ ᴏʀ ɴᴏᴛ ᴀ ᴍᴇᴍʙᴇʀ ᴏꜰ ᴛʜɪꜱ ɢʀᴏᴜᴘ.")
            logger.warning(f"User not found for identifier: {target_identifier}")
            return None
    else:
        await client.send_message(chat_id, "ᴘʟᴇᴀꜱᴇ ꜱᴘᴇᴄɪꜰʏ ᴀ ᴜꜱᴇʀ ᴛᴏ ᴘʀᴏᴍᴏᴛᴇ ʙʏ ᴜꜱᴇʀɴᴀᴍᴇ, ᴜꜱᴇʀ ɪᴅ, ᴏʀ ʀᴇᴘʟʏɪɴɢ ᴛᴏ ᴛʜᴇɪʀ ᴍᴇꜱꜱᴀɢᴇ..")
        return None

def initialize_permissions(bot_privileges):
    return {
        "can_change_info": False,
        "can_invite_users": False,
        "can_delete_messages": False,
        "can_restrict_members": False,
        "can_pin_messages": False,
        "can_promote_members": False,
        "can_manage_chat": False,
        "can_manage_video_chats": False,
    }

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

    # Fetch the bot's privileges
    bot_user = await client.get_me()
    bot_member = await client.get_chat_member(chat_id, bot_user.id)
    bot_privileges = bot_member.privileges  # Get the bot's privileges

    # Pass the callback_query as the third argument
    markup = await create_permission_markup(target_user_id, bot_privileges, callback_query)

    await callback_query.message.edit_text(
        f"👤 {target_user_name} [{target_user_id}]\n👥 {group_name}",
        reply_markup=markup
    )
    await callback_query.answer()

async def create_permission_markup(target_user_id, bot_privileges, callback_query):
    buttons = []
    button_names = {
        "can_change_info": "ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ɪɴꜰᴏ",
        "can_invite_users": "ɪɴᴠɪᴛᴇ ᴜꜱᴇʀꜱ",
        "can_delete_messages": "ᴅᴇʟᴇᴛᴇ ᴍᴇꜱꜱᴀɢᴇꜱ",
        "can_restrict_members": "ʙᴀɴ ᴜꜱᴇʀꜱ",
        "can_pin_messages": "ᴘɪɴ ᴍᴇꜱꜱᴀɢᴇꜱ",
        "can_promote_members": "ᴀᴅᴅ ɴᴇᴡ ᴍᴇᴍʙᴇʀꜱ",
        "can_manage_chat": "ᴍᴀɴᴀɢᴇ ꜱᴛᴏʀɪᴇꜱ",
        "can_manage_video_chats": "ᴍᴀɴᴀɢᴇ ʟɪᴠᴇ ꜱᴛʀᴇᴀᴍꜱ",
    }

    # Retrieve the admin's privileges
    admin_member = await callback_query._client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
    admin_privileges = admin_member.privileges

    for perm, state in temporary_permissions[target_user_id].items():
        # Check if bot has the permission to grant this privilege
        bot_can_grant = getattr(bot_privileges, perm, False)

        # Check if the admin performing the action has the privilege to toggle this permission
        admin_can_grant = getattr(admin_privileges, perm, False)

        # Determine the icon based on conditions
        if not bot_can_grant:
            icon = "🔐"  # Bot lacks permission
        elif not admin_can_grant:
            icon = "🔒"  # Admin lacks permission
        elif state:
            icon = "✅"  # Permission is enabled
        else:
            icon = "❌"  # Permission is disabled

        # Button label
        button_label = button_names.get(perm, perm.replace('can_', '').replace('_', ' ').capitalize())
        callback_data = f"admin|toggle|{perm}|{target_user_id}"
        buttons.append(InlineKeyboardButton(f"{button_label} {icon}", callback_data=callback_data))

    # Add save and close buttons
    save_button = InlineKeyboardButton("ꜱᴀᴠᴇ", callback_data=f"admin|save|{target_user_id}")
    close_button = InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data=f"admin|close|{target_user_id}")

    # Arrange buttons in rows
    button_rows = [buttons[i:i + 1] for i in range(0, len(buttons))]
    button_rows.append([save_button, close_button])

    return InlineKeyboardMarkup(button_rows)

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

async def toggle_permission(callback_query, target_user_id, perm_code):
    chat_id = callback_query.message.chat.id
    client = callback_query._client

    # Fetch bot and admin privileges
    bot_member = await client.get_chat_member(chat_id, client.me.id)
    admin_member = await client.get_chat_member(chat_id, callback_query.from_user.id)

    bot_privileges = bot_member.privileges
    admin_privileges = admin_member.privileges

    # Check if bot has the permission
    bot_can_grant = getattr(bot_privileges, perm_code, False)

    # Check if admin has the permission
    admin_can_grant = getattr(admin_privileges, perm_code, False)

    # Handle different cases for icons
    if not bot_can_grant:
        await callback_query.answer("I don't have this permission.", show_alert=True)
        return

    if not admin_can_grant:
        await callback_query.answer("You don't have this permission.", show_alert=True)
        return

    # Toggle the permission for the user
    if target_user_id in temporary_permissions:
        permissions_dict = temporary_permissions[target_user_id]
        permissions_dict[perm_code] = not permissions_dict[perm_code]

        # Refresh the markup with updated icons
        markup = await create_permission_markup(target_user_id, bot_privileges, callback_query)
        await callback_query.message.edit_reply_markup(markup)
        await callback_query.answer(f"{perm_code.replace('can_', '').replace('_', ' ').capitalize()} toggled.")
    else:
        await callback_query.answer("No permissions found for this user.", show_alert=True)

async def get_chat_privileges(callback_query):
    user_member = await callback_query._client.get_chat_member(callback_query.message.chat.id, callback_query.from_user.id)
    return user_member.privileges

async def save_permissions(client, callback_query, target_user_id):
    if target_user_id in temporary_permissions:
        permissions = temporary_permissions.pop(target_user_id)
        privileges = ChatPrivileges(**permissions)

        chat_id = callback_query.message.chat.id
        try:
            await client.promote_chat_member(chat_id, target_user_id, privileges=privileges)
            updated_member = await client.get_chat_member(chat_id, target_user_id)
            user_name = updated_member.user.first_name or updated_member.user.username or "User"
            await callback_query.message.delete()
            await callback_query.answer(f"{user_name} ʜᴀꜱ ʙᴇᴇɴ ᴘʀᴏᴍᴏᴛᴇᴅ.", show_alert=True)

            if target_user_id in temporary_messages:
                await temporary_messages[target_user_id].delete()
                del temporary_messages[target_user_id]

        except Exception as e:
            await callback_query.answer(f"Failed to promote user: {str(e)}", show_alert=True)
            logger.error(f"Error promoting user {target_user_id} with privileges {privileges}: {e}")
    else:
        await callback_query.answer("No permissions found for this user.", show_alert=True)

async def close_permission_selection(callback_query):
    await callback_query.message.delete()
    target_user_id = int(callback_query.data.split("|")[-1])

    if target_user_id in temporary_messages:
        await temporary_messages[target_user_id].delete()
        del temporary_messages[target_user_id]

    await callback_query.answer("ᴘᴇʀᴍɪꜱꜱɪᴏɴ ꜱᴇʟᴇᴄᴛɪᴏɴ ᴄʟᴏꜱᴇᴅ.", show_alert=True)

async def cleanup_temporary_permissions():
    pass

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


# Check if user has admin rights
async def is_administrator(user_id: int, message, client):
    admin = False
    administrators = []
    async for m in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)
    for user in administrators:
        if user.user.id == user_id:
            admin = True
            break
    return admin


# Promote function
@app.on_message(filters.command(["promote", "fullpromote"], prefixes=["/", "!", ".",","]))
async def promoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif len(message.command) > 1:
            user = message.text.split(None, 1)[1]
            if not user.startswith("@"):  # Ensure the username is in correct format
                user = "@" + user
        else:
            await message.reply("Invalid command usage.")
            return

        user_data = await client.get_users(user)  # Fetch user details
        umention = user_data.mention  # Mention of the user being promoted
        group_name = message.chat.title  # Get the group name
        promoter_mention = message.from_user.mention  # Mention of the person promoting
    except Exception as e:
        await message.reply(f"Invalid ID or user not found. Error: {e}")
        return

    if not user:
        await message.reply("User not found.")
        return

    # Check if bot has promotion rights
    bot_member = await client.get_chat_member(message.chat.id, client.me.id)
    bot_privileges = bot_member.privileges

    if not bot_privileges or not bot_privileges.can_promote_members:
        await message.reply("I don't have the permission to promote members.")
        return

    # Check if the owner is promoting themselves
    if int(user_data.id) == int(message.from_user.id):
        if message.from_user.id == OWNER_ID:
            # Owner can promote themselves without any restrictions
            pass  # Allow the owner to promote themselves
        else:
            await message.reply("You cannot promote yourself unless you're the owner.")
            return

    # For promoting others, check if the promoter (owner) is an admin
    if int(user_data.id) != int(message.from_user.id) and message.from_user.id == OWNER_ID:
        # Owner is allowed to promote others only if they are an admin in the group
        is_admin = await is_administrator(message.from_user.id, message, client)
        if not is_admin:
            await message.reply("As the owner, you need to be an admin to promote others.")
            return

    # Check if non-owners are trying to promote
    if message.from_user.id != OWNER_ID:
        is_admin = await is_administrator(message.from_user.id, message, client)
        if not is_admin:
            await message.reply("You need to be an admin to promote others.")
            return

    try:
        if message.command[0] == "fullpromote":
            await message.chat.promote_member(
                user_id=user_data.id,
                privileges=ChatPrivileges(
                    can_change_info=bot_privileges.can_change_info,
                    can_invite_users=bot_privileges.can_invite_users,
                    can_delete_messages=bot_privileges.can_delete_messages,
                    can_restrict_members=bot_privileges.can_restrict_members,
                    can_pin_messages=bot_privileges.can_pin_messages,
                    can_promote_members=bot_privileges.can_promote_members,
                    can_manage_chat=bot_privileges.can_manage_chat,
                    can_manage_video_chats=bot_privileges.can_manage_video_chats,
                ),
            )
            await message.reply(f"</b>⬤ ғᴜʟʟᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ ➠</b> {group_name}\n\n<b>● ᴘʀᴏᴍᴏᴛᴇᴅ ᴜsᴇʀ ➠</b> {umention}\n<b>● ᴩʀᴏᴍᴏᴛᴇʀ ʙʏ ➠</b> {promoter_mention}")
        else:
            await message.chat.promote_member(
                user_id=user_data.id,
                privileges=ChatPrivileges(
                    can_change_info=False,
                    can_invite_users=bot_privileges.can_invite_users,
                    can_delete_messages=bot_privileges.can_delete_messages,
                    can_restrict_members=False,
                    can_pin_messages=bot_privileges.can_pin_messages,
                    can_promote_members=False,
                    can_manage_chat=bot_privileges.can_manage_chat,
                    can_manage_video_chats=bot_privileges.can_manage_video_chats,
                ),
            )
            await message.reply(f"<b>⬤ ᴩʀᴏᴍᴏᴛɪɴɢ ᴀ ᴜsᴇʀ ɪɴ ➠</b> {group_name}\n\n<b>● ᴩʀᴏᴍᴏᴛᴇᴅ ᴜsᴇʀ ➠</b> {umention}\n<b>● ᴩʀᴏᴍᴏᴛᴇʀ ʙʏ ➠</b> {promoter_mention}")
    except Exception as err:
        await message.reply(f"An error occurred: {err}")


# Demote function
@app.on_message(filters.command(["demote"], prefixes=["/", "!", ".",","]))
async def demoteFunc(client, message):
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user.id
        elif not message.reply_to_message and len(message.command) > 1:
            user = message.text.split(None, 1)[1]
            if not user.startswith("@"):  # Ensure the username is in correct format
                user = "@" + user
        else:
            await message.reply("<u><b>ᴜsᴇʀ ɴᴏᴛ ғᴏᴜɴᴅ.</u></b>\nᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ /{command_name} ᴍᴜsᴛ ʙᴇ ᴜsᴇᴅ sᴘᴇᴄɪғʏɪɴɢ ᴜsᴇʀ <b>ᴜsᴇʀɴᴀᴍᴇ/ɪᴅ/ᴍᴇɴᴛɪᴏɴ ᴏʀ ʀᴇᴘʟʏɪɴɢ</b> ᴛᴏ ᴏɴᴇ ᴏғ ᴛʜᴇɪʀ ᴍᴇssᴀɢᴇs.")
            return

        user_data = await client.get_users(user)  # Fetch user details
        umention = user_data.mention  # Mention of the user being demoted
        group_name = message.chat.title  # Get the group name
        promoter_mention = message.from_user.mention  # Mention of the person demoting
    except Exception as e:
        await message.reply(f"Invalid ID or user not found. Error: {e}")
        return

    bot_member = await client.get_chat_member(message.chat.id, client.me.id)
    bot_privileges = bot_member.privileges

    if not bot_privileges or not bot_privileges.can_promote_members:
        await message.reply("I don't have the permission to demote members.")
        return

    # Prevent self-demotion unless user is the owner
    if int(user_data.id) == int(message.from_user.id) and message.from_user.id != OWNER_ID:
        await message.reply("You cannot demote yourself unless you're the owner.")
        return

    if not await is_administrator(message.from_user.id, message, client):
        await message.reply("You do not have the permission to demote members.")
        return

    try:
        await message.chat.promote_member(
            user_id=user_data.id,
            privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            )
        )
        await message.reply(f"<b>⬤ sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇᴍᴏᴛᴇᴅ ᴀ ᴀᴅᴍɪɴ ɪɴ ➠</b> {group_name}\n\n<b>● ᴅᴇᴍᴏᴛᴇᴅ ᴜsᴇʀ ➠</b> {umention}\n● ᴩʀᴏᴍᴏᴛᴇʀ ʙʏ ➠</b> {promoter_mention}")
    except Exception as err:
        await message.reply(f"Error: {err}")