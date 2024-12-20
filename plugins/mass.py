import asyncio
import config
from time import time
import os
import sys
from pyrogram import Client, enums
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from Alex import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.errors import MessageDeleteForbidden, RPCError
from config import OWNER_ID, BANNED_USERS
from Alex.misc import SUDOERS



# Helper function to check if the user is bot owner or group owner
async def is_authorized(client, chat_id, user_id):
    chat_member = await client.get_chat_member(chat_id, user_id)
    return user_id == OWNER_ID or chat_member.status == enums.ChatMemberStatus.OWNER

@app.on_message(filters.command(["unbanall"], prefixes=["/", "!", "."]))
async def unbanall_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Check if the user is either the bot owner or the group owner
    if await is_authorized(client, chat_id, user_id):
        # Send confirmation message with buttons
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ᴀᴘᴘʀᴏᴠᴇ", callback_data="approve_unbanall"),
                    InlineKeyboardButton("ᴅᴇᴄʟɪɴᴇ", callback_data="decline_unbanall")
                ]
            ]
        )
        await message.reply_text(
            "ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴʙᴀɴ ᴀʟʟ ʙᴀɴɴᴇᴅ ᴜsᴇʀs? ᴏɴʟʏ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs ᴀᴄᴛɪᴏɴ.",
            reply_markup=reply_markup
        )
    else:
        await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")

# Callback query handler for button clicks
@app.on_callback_query(filters.regex("approve_unbanall|decline_unbanall"))
async def callback_handler(client, callback_query):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id

    # Check if the user who clicked is either the bot owner or the group owner
    if await is_authorized(client, chat_id, user_id):
        approver_name = callback_query.from_user.first_name  # Fetch approver's name

        if callback_query.data == "approve_unbanall":
            # If approved, start the unban process
            await callback_query.message.edit_text("<b>ᴜɴʙᴀɴᴀʟʟ ꜱᴛᴀʀᴛɪɴɢ ...</b>")

            bot = await client.get_chat_member(chat_id, client.me.id)
            bot_permission = bot.privileges.can_restrict_members

            if bot_permission:
                unban_count = 0  # Counter for unbanned members
                async for member in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
                    try:
                        await client.unban_chat_member(chat_id, member.user.id)
                        unban_count += 1  # Increment counter for each successful unban
                    except Exception:
                        pass

                # Final message with the approver's name
                await callback_query.message.edit_text(
                    f"<u><b>⬤ ᴜɴʙᴀɴ ᴄᴏᴍᴘʟᴇᴛᴇᴅ!</u></b>\n\n<b>● ᴛᴏᴛᴀʟ ᴜsᴇʀs ➠</b> {unban_count}\n<b>● ᴜɴʙᴀɴɴᴇᴅ ʙʏ ➠</b> {approver_name}"
                )
            else:
                await callback_query.message.edit_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ᴜɴʙᴀɴ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs.")
        elif callback_query.data == "decline_unbanall":
            # If declined, send a cancellation message
            await callback_query.message.edit_text("ᴜʙᴀɴᴀʟʟ ᴄᴏᴍᴍᴀɴᴅ ᴡᴀs ᴅᴇᴄʟɪɴᴇᴅ.")
    else:
        # If an unauthorized user tries to click the button
        await callback_query.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴏʀ ᴅᴇᴄʟɪɴᴇ ᴛʜɪs ᴀᴄᴛɪᴏɴ.", show_alert=True)

# ------------------------------------------------ #

@app.on_message(filters.command(["banall"], prefixes=["/", "!", ".", ","]))
async def banall_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # Get the status of the user in the group (owner or not)
    chat_member = await client.get_chat_member(chat_id, user_id)

    # Check if the user is either the bot owner or the group owner
    if user_id == OWNER_ID or chat_member.status == enums.ChatMemberStatus.OWNER:
        # Send approval request with buttons
        await message.reply_text(
            "ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ᴅᴀɴᴀʟʟ ᴘʀᴏᴄᴇss? ᴏɴʟʏ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs ᴀᴄᴛɪᴏɴ.",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("ᴀᴘᴘʀᴏᴠᴇ", callback_data="approve_banall"),
                    InlineKeyboardButton("ᴅᴇᴄʟɪɴᴇ", callback_data="decline_banall")
                ]]
            )
        )
    else:
        await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")

@app.on_callback_query(filters.regex("approve_banall"))
async def approve_banall(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.first_name

    # Get the status of the user to check if they are authorized
    chat_member = await client.get_chat_member(chat_id, user_id)

    if user_id == OWNER_ID or chat_member.status == enums.ChatMemberStatus.OWNER:
        await callback_query.message.edit_text(f"ʙᴀɴᴀʟʟ ꜱᴛᴀʀᴛɪɴɢ ... ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ {user_name}.")

        bot = await client.get_chat_member(chat_id, client.me.id)
        bot_permission = bot.privileges.can_restrict_members

        if bot_permission:
            ban_count = 0  # Initialize ban count
            async for member in client.get_chat_members(chat_id):
                try:
                    await client.ban_chat_member(chat_id, member.user.id)
                    ban_count += 1  # Increment ban count for each ban
                except Exception:
                    pass
            await callback_query.message.edit_text(f"<b><u>⬤ ʙᴀɴᴀʟʟ ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇᴅ!</b></u>\n\n<b>● ᴛᴏᴛᴀʟ ᴜsᴇʀs ➠</b> {ban_count}\n<b>● ʙᴀɴɴᴇᴅ ʙʏ ➠</b> {user_name}")
        else:
            await callback_query.message.edit_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs.")
    else:
        await callback_query.message.edit_text(f"{user_name}, ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs ᴀᴄᴛɪᴏɴ.")

@app.on_callback_query(filters.regex("decline_banall"))
async def decline_banall(client, callback_query: CallbackQuery):
    user_name = callback_query.from_user.first_name
    await callback_query.message.edit_text(f"</b>ʙᴀɴᴀʟʟ ᴘʀᴏᴄᴇss ʜᴀs ʙᴇᴇɴ ᴄᴀɴᴄᴇʟᴇᴅ ʙʏ</b> {user_name}.")

# ------------------------------------------------ #

# Mute All command
@app.on_message(filters.command(["muteall"], prefixes=["/", "!", ".", ","]))
async def mute_all_users(client, message):
    chat_id = message.chat.id
    issuer = message.from_user  # The user issuing the mute command

    # Ensure the user issuing the command is either the bot owner or the group owner
    if issuer.id != OWNER_ID:
        issuer_member = await client.get_chat_member(chat_id, issuer.id)
        if issuer_member.status != ChatMemberStatus.OWNER:
            await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")
            return

    # Send confirmation message with buttons
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("ᴀᴘᴘʀᴏᴠᴇ", callback_data="approve_mute"),
            InlineKeyboardButton("ᴅᴇᴄʟɪɴᴇ", callback_data="decline_mute")
        ]]
    )
    await message.reply_text("ᴅᴏ ʏᴏᴜ ʀᴇᴀʟʟʏ ᴡᴀɴᴛ ᴛᴏ ᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀs?", reply_markup=buttons)


# Callback for Mute All Approval
@app.on_callback_query(filters.regex("approve_mute"))
async def approve_mute(client, callback_query: CallbackQuery):
    message = callback_query.message
    chat_id = message.chat.id

    # Check if user has the right to approve
    issuer = callback_query.from_user
    if issuer.id != OWNER_ID:
        issuer_member = await client.get_chat_member(chat_id, issuer.id)
        if issuer_member.status != ChatMemberStatus.OWNER:
            await callback_query.answer("ᴏɴʟʏ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ᴏʀ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs.", show_alert=True)
            return

    # Mute all non-admin members
    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.edit_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴍᴜᴛᴇ ᴜsᴇʀs.")
        return

    starting_message = await message.edit_text("<b>ᴍᴜᴛᴇᴀʟʟ sᴛᴀʀᴛɪɴɢ . . .</b>")
    muted_count = 0

    async for member in client.get_chat_members(chat_id):
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER] and member.user.id != OWNER_ID:
            try:
                await client.restrict_chat_member(
                    chat_id,
                    member.user.id,
                    permissions=ChatPermissions(can_send_messages=False)
                )
                muted_count += 1
            except Exception as e:
                await message.reply_text(f"Failed to mute {member.user.first_name}: {str(e)}")

    await starting_message.edit_text(f"ᴍᴜᴛᴇᴅ {muted_count} ɴᴏɴ-ᴀᴅᴍɪɴ ᴍᴇᴍʙᴇʀs sᴜᴄᴄᴇssғᴜʟʟʏ.")
    await callback_query.answer()


# Callback for Decline
@app.on_callback_query(filters.regex("decline_mute"))
async def decline_mute(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("ᴍᴜᴛᴇ ᴏᴘᴇʀᴀᴛɪᴏɴ ʜᴀs ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ.")
    await callback_query.answer()

# ------------------------------------------------ #

@app.on_message(filters.command(["unmuteall"], prefixes=["/", "!", ".", ","]))
async def unmute_all_users(client, message):
    chat_id = message.chat.id
    issuer = message.from_user  # The user issuing the unmute command

    # Ensure the user issuing the command is either the bot owner or the group owner
    if issuer.id != OWNER_ID:
        issuer_member = await client.get_chat_member(chat_id, issuer.id)
        if issuer_member.status != ChatMemberStatus.OWNER:
            await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")
            return

    # Send confirmation message with buttons
    buttons = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("ᴀᴘᴘʀᴏᴠᴇ", callback_data="approve_unmute"),
            InlineKeyboardButton("ᴅᴇᴄʟɪɴᴇ", callback_data="decline_unmute")
        ]]
    )
    await message.reply_text("ᴅᴏ ʏᴏᴜ ʀᴇᴀʟʟʏ ᴡᴀɴᴛ ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴀʟʟ ᴍᴇᴍʙᴇʀs?", reply_markup=buttons)


# Callback for Unmute All Approval
@app.on_callback_query(filters.regex("approve_unmute"))
async def approve_unmute(client, callback_query: CallbackQuery):
    message = callback_query.message
    chat_id = message.chat.id

    # Check if user has the right to approve
    issuer = callback_query.from_user
    if issuer.id != OWNER_ID:
        issuer_member = await client.get_chat_member(chat_id, issuer.id)
        if issuer_member.status != ChatMemberStatus.OWNER:
            await callback_query.answer("ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴀᴘᴘʀᴏᴠᴇ ᴛʜɪs.", show_alert=True)
            return

    # Unmute all non-admin members
    bot = await client.get_chat_member(chat_id, client.me.id)
    if not bot.privileges.can_restrict_members:
        await message.edit_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴜɴᴍᴜᴛᴇ ᴜsᴇʀs.")
        return

    starting_message = await message.edit_text("<b>ᴜɴᴍᴜᴛᴇᴀʟʟ sᴛᴀʀᴛɪɴɢ . . .</b>")
    unmuted_count = 0

    async for member in client.get_chat_members(chat_id):
        if member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            try:
                await client.restrict_chat_member(
                    chat_id,
                    member.user.id,
                    permissions=ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_polls=True,
                        can_add_web_page_previews=True,
                        can_change_info=True,
                        can_invite_users=True,
                        can_pin_messages=True
                    )
                )
                unmuted_count += 1
            except Exception as e:
                await message.reply_text(f"Failed to unmute {member.user.first_name}: {str(e)}")

    await starting_message.edit_text(f"ᴜɴᴍᴜᴛᴇᴇᴅ {unmuted_count} ɴᴏɴ-ᴀᴅᴍɪɴ ᴍᴇᴍʙᴇʀs sᴜᴄᴄᴇssғᴜʟʟʏ.")
    await callback_query.answer()


# Callback for Decline
@app.on_callback_query(filters.regex("decline_unmute"))
async def decline_unmute(client, callback_query: CallbackQuery):
    await callback_query.message.edit_text("ᴜɴᴍᴜᴛᴇ ᴏᴘᴇʀᴀᴛɪᴏɴ ʜᴀs ʙᴇᴇɴ ᴅᴇᴄʟɪɴᴇᴅ.")
    await callback_query.answer()

# ------------------------------------------------ #

# kickall with approve/decline buttons, restricted to bot owner or group owner
@app.on_message(filters.command("cac") & ~filters.private & ~BANNED_USERS)
async def kick_all_func(_, message: Message):
    user_id = message.from_user.id

    # Check if the user is the bot owner or the group owner
    chat_member = await app.get_chat_member(message.chat.id, user_id)
    if user_id not in SUDOERS and chat_member.status != ChatMemberStatus.OWNER:
        return await message.reply_text("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.")

    # Create inline keyboard for approval
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ᴀᴘᴘʀᴏᴠᴇ", callback_data="approve_kickall"),
                InlineKeyboardButton("ᴅᴇᴄʟɪɴᴇ", callback_data="decline_kickall")
            ]
        ]
    )

    # Send confirmation message with buttons
    await message.reply_text(
        "⚠️ ᴀʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴋɪᴄᴋ ᴀʟʟ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ ᴛʜɪs ᴄʜᴀᴛ?",
        reply_markup=buttons
    )

# Callback query handler for approve/decline
@app.on_callback_query(filters.regex("^(approve_kickall|decline_kickall)$"))
async def handle_kickall_confirmation(client, callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    chat_member = await client.get_chat_member(callback_query.message.chat.id, user_id)

    # Check if the user is the bot owner or the group owner
    if user_id not in SUDOERS and chat_member.status != ChatMemberStatus.OWNER:
        await callback_query.answer("❌ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴛᴏ ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ. ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜsᴇ ᴛʜɪs.", show_alert=True)
        return

    if callback_query.data == "approve_kickall":
        await callback_query.message.edit_text("<b>ᴋɪᴄᴋɪɴɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs . . .</b>")
        kicked_count = 0
        failed_count = 0

        async for member in app.get_chat_members(callback_query.message.chat.id):
            user_id = member.user.id
            # Skip if user is the bot itself, an admin, or a SUDOER
            if user_id == app.id or user_id in SUDOERS or member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
                continue

            try:
                await callback_query.message.chat.ban_member(user_id)
                await asyncio.sleep(0.5)  # Add small delay to avoid flood limits
                await callback_query.message.chat.unban_member(user_id)
                kicked_count += 1
            except Exception:
                failed_count += 1

        await callback_query.message.edit_text(
            f"<b>sᴜᴄᴄᴇssғᴜʟʟʏ ᴋɪᴄᴋᴇᴅ <u>{kicked_count}</u> ᴜsᴇʀs\nғᴀɪʟᴇᴅ ᴛᴏ ᴋɪᴄᴋ <u>{failed_count}</u> ᴜsᴇʀs</b>"
        )
    elif callback_query.data == "decline_kickall":
        await callback_query.message.edit_text("<b>ᴋɪᴄᴋᴀʟʟ ᴏᴘᴇʀᴀᴛɪᴏɴ ᴄᴀɴᴄᴇʟʟᴇᴅ . . .</b>")