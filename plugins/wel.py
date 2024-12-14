import asyncio
import os
from re import findall
from datetime import datetime, timedelta
from random import shuffle

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    UserNotParticipant,
)
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.types import (
    Chat,
    ChatPermissions,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    User,
)

from config import BOT_USERNAME, SUDOERS, WELCOME_DELAY_KICK_SEC, app
from Alex.core.decorators.errors import capture_err
from Alex.core.decorators.permissions import adminsOnly
from utils.keyboard import ikb
from Alex.modules.notes import extract_urls
from wbb.utils.dbfeds import check_banned_user, get_fed_id
from wbb.utils.dbfunctions import (
    captcha_off,
    captcha_on,
    del_welcome,
    get_captcha_cache,
    get_welcome,
    has_solved_captcha_once,
    is_captcha_on,
    is_gbanned_user,
    save_captcha_solved,
    set_welcome,
    update_captcha_cache,
)
from utils.filter_groups import welcome_captcha_group
from utils.functions import (
    check_format,
    extract_text_and_keyb,
    generate_captcha,
)

__MODULE__ = "Greetings"
__HELP__ = """
/captcha [ENABLE|DISABLE] - Enable/Disable captcha.

/set_welcome - Reply this to a message containing correct
format for a welcome message, check end of this message.

/del_welcome - Delete the welcome message.
/get_welcome - Get the welcome message.

**SET_WELCOME ->**

**To set a photo or gif as welcome message. Add your welcome message as caption to the photo or gif. The caption muse be in the format given below.**

For text welcome message just send the text. Then reply with the command 

The format should be something like below.

```
**Hi** {name} [{id}] Welcome to {chat}

~ #This separater (~) should be there between text and buttons, remove this comment also

button=[Duck, https://duckduckgo.com]
button2=[Github, https://github.com]
```

**NOTES ->**

Checkout /markdownhelp to know more about formattings and other syntax.
"""

answers_dicc = []
loop = asyncio.get_running_loop()


async def get_initial_captcha_cache():
    global answers_dicc
    answers_dicc = await get_captcha_cache()
    return answers_dicc


loop.create_task(get_initial_captcha_cache())


async def handle_new_member(member, chat):
    global answers_dicc

    # Get cached answers from mongodb in case of bot's been restarted or crashed.
    answers_dicc = await get_captcha_cache()

    # Mute new member and send message with button
    try:
        if member.id in SUDOERS:
            return  # Ignore sudo users
        fed_id = await get_fed_id(chat.id)
        if fed_id:
            check_user = await check_banned_user(fed_id, member.id)
            if check_user:
                reason = check_user["reason"]
                date = check_user["date"]
                await chat.ban_member(member.id)
                return await app.send_message(
                    chat.id,
                    f"**User {member.mention} was Fed Banned.\n\nReason: {reason}.\nDate: {date}.**",
                )
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"{member.mention} was globally banned, and got removed,"
                + " if you think this is a false gban, you can appeal"
                + " for this ban in support chat.",
            )
            return
        if member.is_bot:
            return  # Ignore bots
        if not await is_captcha_on(chat.id):
            return await send_welcome_message(
                chat, member.id
            )

        # Ignore user if he has already solved captcha in this group
        # someday
        if await has_solved_captcha_once(chat.id, member.id):
            return

        await chat.restrict_member(member.id, ChatPermissions())
        text = (
            f"{(member.mention())} Are you human?\n"
            f"Solve this captcha in {WELCOME_DELAY_KICK_SEC} "
            "seconds and 4 attempts or you'll be kicked."
        )
    except ChatAdminRequired:
        return

    # Generate a captcha image, answers, and some wrong answers
    captcha = generate_captcha()
    captcha_image = captcha[0]
    captcha_answer = captcha[1]
    wrong_answers = captcha[2]  # This consists of 8 wrong answers
    correct_button = InlineKeyboardButton(
        f"{captcha_answer}",
        callback_data=f"pressed_button {captcha_answer} {member.id}",
    )
    temp_keyboard_1 = [correct_button]  # Button row 1
    temp_keyboard_2 = []  # Botton row 2
    temp_keyboard_3 = []
    for i in range(2):
        temp_keyboard_1.append(
            InlineKeyboardButton(
                f"{wrong_answers[i]}",
                callback_data=f"pressed_button {wrong_answers[i]} {member.id}",
            )
        )
    for i in range(2, 5):
        temp_keyboard_2.append(
            InlineKeyboardButton(
                f"{wrong_answers[i]}",
                callback_data=f"pressed_button {wrong_answers[i]} {member.id}",
            )
        )
    for i in range(5, 8):
        temp_keyboard_3.append(
            InlineKeyboardButton(
                f"{wrong_answers[i]}",
                callback_data=f"pressed_button {wrong_answers[i]} {member.id}",
            )
        )

    shuffle(temp_keyboard_1)
    keyboard = [temp_keyboard_1, temp_keyboard_2, temp_keyboard_3]
    shuffle(keyboard)
    verification_data = {
        "chat_id": chat.id,
        "user_id": member.id,
        "answer": captcha_answer,
        "keyboard": keyboard,
        "attempts": 0,
    }
    keyboard = InlineKeyboardMarkup(keyboard)
    # Append user info, correct answer, and
    answers_dicc.append(verification_data)
    # keyboard for later use with callback query
    button_message = await app.send_photo(
        chat_id=chat.id,
        photo=captcha_image,
        caption=text,
        reply_markup=keyboard,
    )
    os.remove(captcha_image)

    # Save captcha answers etc in mongodb in case the bot gets crashed or restarted.
    await update_captcha_cache(answers_dicc)

    asyncio.create_task(
        kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, button_message, member
        )
    )
    await asyncio.sleep(0.5)



@app.on_chat_member_updated(filters.group, group=welcome_captcha_group)
@capture_err
async def welcome(_, user: ChatMemberUpdated):
    if not (
        user.new_chat_member
        and user.new_chat_member.status not in {CMS.RESTRICTED, CMS.BANNED}
        and not user.old_chat_member
    ):
        return

    member = user.new_chat_member.user if user.new_chat_member else user.from_user
    chat = user.chat
    return await handle_new_member(member, chat)


async def send_welcome_message(chat: Chat, user_id: int, delete: bool = False):
    welcome, raw_text, file_id = await get_welcome(chat.id)

    if not raw_text:
        return
    text = raw_text
    keyb = None
    if findall(r"\[.+\,.+\]", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)

    if "{chat}" in text:
        text = text.replace("{chat}", chat.title)
    if "{name}" in text:
        text = text.replace("{name}", (await app.get_users(user_id)).mention)
    if "{id}" in text:
        text = text.replace("{id}", f"`{user_id}`")

    async def _send_wait_delete():
        if welcome == "Text":
            m = await app.send_message(
                chat.id,
                text=text,
                reply_markup=keyb,
                disable_web_page_preview=True,
            )
        elif welcome == "Photo":
            m = await app.send_photo(
                chat.id,
                photo=file_id,
                caption=text,
                reply_markup=keyb,
            )
        else:
            m = await app.send_animation(
                chat.id,
                animation=file_id,
                caption=text,
                reply_markup=keyb,
            )
        await asyncio.sleep(300)
        await m.delete()

    asyncio.create_task(_send_wait_delete())


@app.on_callback_query(filters.regex("pressed_button"))
async def callback_query_welcome_button(_, callback_query):
    """After the new member presses the correct button,
    set his permissions to chat permissions,
    delete button message and join message.
    """
    global answers_dicc
    data = callback_query.data
    pressed_user_id = callback_query.from_user.id
    pending_user_id = int(data.split(None, 2)[2])
    button_message = callback_query.message
    answer = data.split(None, 2)[1]

    correct_answer = None
    keyboard = None

    if len(answers_dicc) != 0:
        for i in answers_dicc: