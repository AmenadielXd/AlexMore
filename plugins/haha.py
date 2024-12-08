import asyncio
from pyrogram import filters, enums
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatPrivileges

from Alex import app
from Alex.misc import SUDOERS
from Alex.utils.database import get_assistant

links = {}


def get_keyboard(command):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data=f"{command}_yes"),
         InlineKeyboardButton("No", callback_data=f"{command}_no")]
    ])


@app.on_message(filters.command("deleteall"))
async def deleteall_command(client, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    assistant = await get_assistant(chat_id)
    assid = assistant.id

    LUCY = await message.reply_text(f"Hey {message.from_user.mention}, 'deleteall' checking...")
    await asyncio.sleep(5)

    bot = await app.get_chat_member(chat_id, app.me.id)
    if not (
        bot.privileges.can_delete_messages and 
        bot.privileges.can_promote_members and
        bot.privileges.can_invite_users
    ):
        await LUCY.edit(
            "ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴇɴᴏᴜɢʜ ᴘᴇʀᴍɪssɪᴏɴs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴍᴀss ᴅᴇʟᴇᴛɪᴏɴ.\n"
            "<b>ᴘᴇʀᴍɪssɪᴏɴs ʀᴇǫᴜɪʀᴇᴅ:</b>\n"
            "● ᴅᴇʟᴇᴛᴇ ᴍᴇssᴀɢᴇs\n"
            "● ᴘʀᴏᴍᴏᴛᴇ ᴍᴇᴍʙᴇʀs\n"
            "● ɪɴᴠɪᴛᴇ ᴜsᴇʀs"
        )
        return
    await asyncio.sleep(5)
    await LUCY.delete()
    confirm_msg = await message.reply(
        f"{message.from_user.mention}, are you sure you want to delete all group messages?",
        reply_markup=get_keyboard("deleteall")
    )


@app.on_callback_query(filters.regex(r"^deleteall_(yes|no)$"))
async def handle_callback(client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    user_id = callback_query.from_user.id
    assistant = await get_assistant(chat_id)
    assid = assistant.id

    # Check if the user is the group owner or a sudo user
    async for admin in client.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if admin.status == ChatMemberStatus.OWNER:
            owner_id = admin.user.id
    if user_id != owner_id and user_id not in SUDOERS:
        await callback_query.answer("<b>ᴏɴʟʏ ᴛʜᴇ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄᴏɴғɪʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ.</b>", show_alert=True)
        return

    # If "Yes" is selected
    if callback_query.data == "deleteall_yes":
        await callback_query.answer("<b>ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴘʀᴏᴄᴇss sᴛᴀʀᴛᴇᴅ . . .</b>", show_alert=True)

        # Invite assistant if not already in the group
        try:
            await app.get_chat_member(chat_id, assid)
        except UserNotParticipant:
            try:
                chat = await app.get_chat(chat_id)
                if chat.username:
                    # Public group
                    await assistant.join_chat(f"https://t.me/{chat.username}")
                else:
                    # Private group, generate invite link
                    if chat_id in links:
                        invitelink = links[chat_id]
                    else:
                        try:
                            invitelink = await app.export_chat_invite_link(chat_id)
                        except ChatAdminRequired:
                            await callback_query.message.edit("I need invite permission to add the assistant.")
                            return
                        links[chat_id] = invitelink
                    await assistant.join_chat(invitelink)
            except InviteRequestSent:
                try:
                    await app.approve_chat_join_request(chat_id, assid)
                except Exception as e:
                    return await callback_query.message.edit(f"Error approving invite: {str(e)}")
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await callback_query.message.edit(f"Error inviting assistant: {str(e)}")

        # Promote the assistant with the required privileges
        await app.promote_chat_member(chat_id, assid, privileges=ChatPrivileges(
            can_manage_chat=False,
            can_delete_messages=True,
            can_manage_video_chats=False,
            can_restrict_members=False,
            can_change_info=False,
            can_invite_users=False,
            can_pin_messages=False,
            can_promote_members=False,
        ))

        try:
            async for msg in assistant.get_chat_history(chat_id):
                try:
                    await assistant.delete_messages(chat_id, msg.id)
                except Exception as e:
                    print(f"Failed to delete message {msg.id}: {e}")
                    continue
            await callback_query.answer("ᴀʟʟ ᴍᴇssᴀɢᴇs ᴅᴇʟᴇᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.", show_alert=False)
        except Exception as e:
            await callback_query.answer(f"An error occurred: {str(e)}", show_alert=False)

    # If "No" is selected
    elif callback_query.data == "deleteall_no":
        await callback_query.message.edit("ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴘʀᴏᴄᴇss ᴄᴀɴᴄᴇʟᴇᴅ.")
