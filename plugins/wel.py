import datetime
import random
from re import findall

from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from Alex import app
from Alex.misc import SUDOERS
from .notes import extract_urls
from Alex.utils.database import is_gbanned_user
from Alex.utils import (
    del_goodbye,
    get_goodbye,
    set_goodbye,
    is_greetings_on,
    set_greetings_on,
    set_greetings_off,
)
from utils.error import capture_err
from utils.functions import check_format, extract_text_and_keyb
from utils.keyboard import ikb
from utils.permissions import adminsOnly


async def handle_left_member(member, chat):

    try:
        if member.id in SUDOERS:
            return
        if await is_gbanned_user(member.id):
            await chat.ban_member(member.id)
            await app.send_message(
                chat.id,
                f"{member.mention} ᴡᴀs ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ, ᴀɴᴅ ɢᴏᴛ ʀᴇᴍᴏᴠᴇᴅ,"
                + " ɪғ ʏᴏᴜ ᴛʜɪɴᴋ ᴛʜɪs ɪs ᴀ ғᴀʟsᴇ ɢʙᴀɴ, ʏᴏᴜ ᴄᴀɴ ᴀᴘᴘᴇᴀʟ"
                + " ғᴏʀ ᴛʜɪs ʙᴀɴ ɪɴ sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ",
            )
            return
        if member.is_bot:
            return
        return await send_left_message(chat, member.id)

    except ChatAdminRequired:
        return


@app.on_message(filters.left_chat_member & filters.group, group=6)
@capture_err
async def goodbye(_, m: Message):
    if m.from_user:
        member = await app.get_users(m.from_user.id)
        chat = m.chat
        return await handle_left_member(member, chat)


async def send_left_message(chat: Chat, user_id: int, delete: bool = False):
    is_on = await is_greetings_on(chat.id, "goodbye")

    if not is_on:
        return

    goodbye, raw_text, file_id = await get_goodbye(chat.id)
    print(f"Debug - Goodbye: {goodbye}, Raw Text: {raw_text}")  # Debug statement

    # Agar custom goodbye message na ho toh random default message select karein
    if not raw_text:
        default_messages = [
              "{NAME} will be missed.",
    "{mention} just went offline.",
    "{mention} has left the lobby.",
    "{mention} has left the clan.",
    "{mention} has left the game.",
    "{mention} has fled the area.",
    "{mention} is out of the running.",
    "Nice knowing ya, {mention}!",
    "It was a fun time {mention}.",
    "We hope to see you again soon, {mention}.",
    "I donut want to say goodbye, {mention}.",
    "Goodbye {mention}! Guess who's gonna miss you :')",
    "Goodbye {mention}! It's gonna be lonely without ya.",
    "Please don't leave me alone in this place, {mention}!",
    "Good luck finding better shit-posters than us, {mention}!",
    "You know we're gonna miss you {mention}. Right? Right? Right?",
    "Congratulations, {mention}! You're officially free of this mess.",
    "{mention}. You were an opponent worth fighting.",
    "You're leaving, {mention}? Yare Yare Daze.",
    "Bring him the photo",
    "Go outside!",
    "Ask again later",
    "Think for yourself",
    "Question authority",
    "You are worshiping a sun god",
    "Don't leave the house today",
    "Give up!",
    "Marry and reproduce",
    "Stay asleep",
    "Wake up",
    "Look to la luna",
    "Steven lives",
    "Meet strangers without prejudice",
    "A hanged man will bring you no luck today",
    "What do you want to do today?",
    "You are dark inside",
    "Have you seen the exit?",
    "Get a baby pet it will cheer you up.",
    "Your princess is in another castle.",
    "You are playing it wrong give me the controller",
    "Trust good people",
    "Live to die.",
    "When life gives you lemons reroll!",
    "Well, that was worthless",
    "I fell asleep!",
    "May your troubles be many",
    "Your old life lies in ruin",
    "Always look on the bright side",
    "It is dangerous to go alone",
    "You will never be forgiven",
    "You have nobody to blame but yourself",
    "Only a sinner",
    "Use bombs wisely",
    "Nobody knows the troubles you have seen",
    "You look fat you should exercise more",
    "Follow the zebra",
    "Why so blue?",
    "The devil in disguise",
    "Go outside",
    "Always your head in the clouds",
]
        raw_text = random.choice(default_messages)  # Random default message choose karein
        goodbye = "Text"  # Default ko "Text" type set karte hain
        file_id = None

    text = raw_text
    keyb = None

    if findall(r".+\,.+", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)

    u = await app.get_users(user_id)

    replacements = {
        "{mention}": u.mention,
        "{id}": f"`{user_id}`",
        "{first}": u.first_name,
        "{chatname}": chat.title,
        "{last}": u.last_name or "None",
        "{username}": u.username or "None",
        "{date}": datetime.datetime.now().strftime("%Y-%m-%d"),
        "{weekday}": datetime.datetime.now().strftime("%A"),
        "{time}": datetime.datetime.now().strftime("%H:%M:%S") + " UTC",
    }

    for placeholder, value in replacements.items():
        if placeholder in text:
            text = text.replace(placeholder, value)

    # Final send message section
    if goodbye == "Text":
        m = await app.send_message(
            chat.id,
            text=text,
            reply_markup=keyb,
            disable_web_page_preview=True,
        )
    elif goodbye == "Photo":
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


@app.on_message(filters.command("setgoodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def set_goodbye_func(_, message):
    usage = "Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ, ɢɪғ ᴏʀ ᴘʜᴏᴛᴏ ᴛᴏ sᴇᴛ ɪᴛ ᴀs ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ.\n\nᴏᴛᴇs: ᴄᴀᴘᴛɪᴏɴ ʀᴇǫᴜɪʀᴇᴅ ғᴏʀ ɢɪғ ᴀɴᴅ ᴘʜᴏᴛᴏ."
    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="More Help",
                    url=f"t.me/{app.username}?start=greetings",
                )
            ],
        ]
    )
    replied_message = message.reply_to_message
    chat_id = message.chat.id
    try:
        if not replied_message:
            await message.reply_text(usage, reply_markup=key)
            return
        if replied_message.animation:
            goodbye = "Animation"
            file_id = replied_message.animation.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.photo:
            goodbye = "Photo"
            file_id = replied_message.photo.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.text:
            goodbye = "Text"
            file_id = None
            text = replied_message.text
            raw_text = text.markdown
        if replied_message.reply_markup and not findall(r"\[.+\,.+\]", raw_text):
            urls = extract_urls(replied_message.reply_markup)
            if urls:
                response = "\n".join(
                    [f"{name}=[{text}, {url}]" for name, text, url in urls]
                )
                raw_text = raw_text + response
        raw_text = await check_format(ikb, raw_text)
        if raw_text:
            await set_goodbye(chat_id, goodbye, raw_text, file_id)
            return await message.reply_text(
                "ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ sᴇᴛ."
            )
        else:
            return await message.reply_text(
                "Wʀᴏɴɢ ғᴏʀᴍᴀᴛᴛɪɴɢ, ᴄʜᴇᴄᴋ ᴛʜᴇ ʜᴇʟᴘ sᴇᴄᴛɪᴏɴ.\n\n**Usᴀsɢᴇ:**\nTᴛᴇxᴛ: `Text`\nᴛᴇxᴛ + ʙᴜᴛᴛᴏɴs: `Text ~ Buttons`",
                reply_markup=key,
            )
    except UnboundLocalError:
        return await message.reply_text(
            "**Oɴʟʏ Tᴇxᴛ, Gɪғ ᴀɴᴅ Pʜᴏᴛᴏ ᴡᴇʟᴄᴏᴍᴇ ᴍᴇssᴀɢᴇ ᴀʀᴇ sᴜᴘᴘᴏʀᴛᴇᴅ.**"
        )


@app.on_message(filters.command(["resetgoodbye"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_goodbye_func(_, message):
    chat_id = message.chat.id

    # Check if goodbye message is set
    goodbye, raw_text, file_id = await get_goodbye(chat_id)

    if not raw_text:
        return await message.reply_text(
            "What are you deleting‽ You haven't set-up the custom goodbye message yet."
        )

    # If goodbye message exists, proceed to delete it
    await del_goodbye(chat_id)
    await message.reply_text("Gᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ Dᴇʟᴇᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ")


@app.on_message(filters.command("goodbye") & ~filters.private)
@adminsOnly("can_change_info")
async def goodbye(client, message: Message):
    command = message.text.split()

    if len(command) == 1:
        return await get_goodbye_func(client, message)

    if len(command) == 2:
        action = command[1].lower()
        if action in ["on", "enable", "y", "yes", "true", "t"]:
            success = await set_greetings_on(message.chat.id, "goodbye")
            if success:
                await message.reply_text(
                    "I'ʟʟ ʙᴇ sᴀʏɪɴɢ ɢᴏᴏᴅʙʏᴇ ᴛᴏ ᴀɴʏ ʟᴇᴀᴠᴇʀs ғʀᴏᴍ ɴᴏᴡ ᴏɴ!"
                )
            else:
                await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴇɴᴀʙʟᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs.")

        elif action in ["off", "disable", "n", "no", "false", "f"]:
            success = await set_greetings_off(message.chat.id, "goodbye")
            if success:
                await message.reply_text("I'ʟʟ sᴛᴀʏ ǫᴜɪᴇᴛ ᴡʜᴇɴ ᴘᴇᴏᴘʟᴇ ʟᴇᴀᴠᴇ.")
            else:
                await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴅɪsᴀʙʟᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs.")

        else:
            await message.reply_text(
                "Iɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ. Pʟᴇᴀsᴇ ᴜsᴇ:\n"
                "/goodbye - Tᴏ ɢᴇᴛ ʏᴏᴜʀ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ\n"
                "/goodbye [on, y, true, enable, t] - ᴛᴏ ᴛᴜʀɴ ᴏɴ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs\n"
                "/goodbye [off, n, false, disable, f, no] - ᴛᴏ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs\n"
                "/delgoodbye ᴏʀ /deletegoodbye ᴛᴏ ᴅᴇʟᴛᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ"
            )
    else:
        await message.reply_text(
            "Iɴᴠᴀʟɪᴅ ᴄᴏᴍᴍᴀɴᴅ. Pʟᴇᴀsᴇ ᴜsᴇ:\n"
            "/goodbye - Tᴏ ɢᴇᴛ ʏᴏᴜʀ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ\n"
            "/goodbye [on, y, true, enable, t] - ᴛᴏ ᴛᴜʀɴ ᴏɴ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs\n"
            "/goodbye [off, n, false, disable, f, no] - ᴛᴏ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇs\n"
            "/delgoodbye ᴏʀ /deletegoodbye ᴛᴏ ᴅᴇʟᴛᴇ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴛᴜʀɴ ᴏғғ ɢᴏᴏᴅʙʏᴇ"
        )


async def get_goodbye_func(_, message):
    chat = message.chat
    goodbye, raw_text, file_id = await get_goodbye(chat.id)
    if not raw_text:
        return await message.reply_text(
            "Dɪᴅ Yᴏᴜ ʀᴇᴍᴇᴍʙᴇʀ ᴛʜᴀᴛ ʏᴏᴜ ʜᴀᴠᴇ sᴇᴛ's ᴀɴᴛ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ"
        )
    if not message.from_user:
        return await message.reply_text("Yᴏᴜ'ʀᴇ ᴀɴᴏɴ, ᴄᴀɴ'ᴛ sᴇɴᴅ ɢᴏᴏᴅʙʏᴇ ᴍᴇssᴀɢᴇ.")

    await send_left_message(chat, message.from_user.id)
    is_grt = await is_greetings_on(chat.id, "goodbye")
    text = None
    if is_grt:
        text = "Tʀᴜᴇ"
    else:
        text = "Fᴀʟsᴇ"
    await message.reply_text(
        f'I ᴀᴍ ᴄᴜʀʀᴇɴᴛʟʏ sᴀʏɪɴɢ ɢᴏᴏᴅʙʏᴇ ᴛᴏ ᴜsᴇʀs :- {text}\nGᴏᴏᴅʙʏᴇ: {goodbye}\n\nғɪʟᴇ_ɪᴅ: `{file_id}`\n\n`{raw_text.replace("`", "")}`'
    )


# welcome 
import datetime
import random
from re import findall

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus as CMS
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.types import (
    Chat,
    ChatMemberUpdated,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from Alex import app
from Alex.misc import SUDOERS
from .notes import extract_urls
from Alex.utils.database import is_gbanned_user

from Alex.utils.welcomedb import (
    del_welcome,
    get_welcome,
    set_welcome,
)

from Alex.utils.error import capture_err
from Alex.utils.functions import check_format, extract_text_and_keyb
from Alex.utils.keyboard import ikb
from Alex.utils.permissions import adminsOnly


# Random welcome messages list
RANDOM_WELCOME_MESSAGES = [
    "Hi {mention}, welcome to the dark side.",
    "Hola {mention}, beware of people with disaster levels",
    "Hey {mention}, we have the droids you are looking for.",
    "Hi {mention}\nThis isn't a strange place, this is my home, it's the people who are strange.",
    "Oh, hey {mention} what's the password?",
    "Hey {mention}, I know what we're gonna do today",
    "{mention} just joined, be at alert they could be a spy.",
    "{mention} joined the group, read by Mark Zuckerberg, CIA and 35 others.",
    "Welcome {mention}, watch out for falling monkeys.",
    "Everyone stop what you’re doing, We are now in the presence of {mention}.",
    "Hey {mention}, do you wanna know how I got these scars?",
    "Welcome {mention}, drop your weapons and proceed to the spy scanner.",
    "Stay safe {mention}, Keep 3 meters social distances between your messages.",  # Corona memes lmao
    "Hey {mention}, Do you know I once One-punched a meteorite?",
    "You’re here now {mention}, Resistance is futile",
    "{mention} just arrived, the force is strong with this one.",
    "{mention} just joined on president’s orders.",
    "Hi {mention}, is the glass half full or half empty?",
    "Yipee Kayaye {mention} arrived.",
    "Welcome {mention}, if you’re a secret agent press 1, otherwise start a conversation",
    "{mention}, I have a feeling we’re not in Kansas anymore.",
    "may take our lives, but they’ll never take our {mention}.",
    "Coast is clear! You can come out guys, it’s just {mention}.",
    "Welcome {mention}, pay no attention to that guy lurking.",
    "Welcome {mention}, may the force be with you.",
    "May the {mention} be with you.",
    "{mention} just joined. Hey, where's Perry?",
    "{mention} just joined. Oh, there you are, Perry.",
    "Ladies and gentlemen, I give you ...  {mention}.",
    "Behold my new evil scheme, the {mention}-Inator.",
    "Ah, {mention} the Platypus, you're just in time... to be trapped.",
    "{mention} just arrived. Diable Jamble!",  # One Piece Sanji
    "{mention} just arrived. Aschente!",  # No Game No Life
    "{mention} say Aschente to swear by the pledges.",  # No Game No Life
    "{mention} just joined. El Psy congroo!",  # Steins Gate
    "Irasshaimase {mention}!",  # weeabo shit
    "Hi {mention}, what is 1000-7?",  # tokyo ghoul
    "Come. I don't want to destroy this place",  # hunter x hunter
    "I... am... Whitebeard!...wait..wrong anime.",  # one Piece
    "Hey {mention}...have you ever heard these words?",  # BNHA
    "Can't a guy get a little sleep around here?",  # Kamina Falls – Gurren Lagann
    "It's time someone put you in your place, {mention}.",  # Hellsing
    "Unit-01's reactivated..",  # Neon Genesis: Evangelion
    "Prepare for trouble...And make it double",  # Pokemon
    "Hey {mention}, are You Challenging Me?",  # Shaggy
    "Oh? You're Approaching Me?",  # jojo
    "Ho… mukatta kuruno ka?",  # jojo jap ver
    "I can't beat the shit out of you without getting closer",  # jojo
    "Ho ho! Then come as close as you'd like.",  # jojo
    "Hoho! Dewa juubun chikazukanai youi",  # jojo jap ver
    "Guess who survived his time in Hell, {mention}.",  # jojo
    "How many loaves of bread have you eaten in your lifetime?",  # jojo
    "What did you say? Depending on your answer, I may have to kick your ass!",  # jojo
    "Oh? You're approaching me? Instead of running away, you come right to me? Even though your grandfather, Joseph, told you the secret of The World, like an exam student scrambling to finish the problems on an exam until the last moments before the chime?",  # jojo
    "Rerorerorerorerorero.",  # jojo
    "{mention} just warped into the group!",
    "I..it's..it's just {mention}.",
    "Sugoi, Dekai. {mention} Joined!",
    "{mention}, do you know gods of death love apples?",  # Death Note owo
    "I'll take a potato chip.... and eat it",  # Death Note owo
]


async def handle_new_member(member, chat):
    try:
        if member.id in SUDOERS:
            return
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
            return
        return await send_welcome_message(chat, member.id)

    except ChatAdminRequired:
        return


@app.on_chat_member_updated(filters.group, group=6)
@capture_err
async def welcome(_, user: ChatMemberUpdated):
    if not (
        user.new_chat_member
        and user.new_chat_member.status not in {CMS.RESTRICTED}
        and not user.old_chat_member
    ):
        return

    member = user.new_chat_member.user if user.new_chat_member else user.from_user
    chat = user.chat
    return await handle_new_member(member, chat)


async def send_welcome_message(chat: Chat, user_id: int, delete: bool = False):
    # Get welcome message from database
    welcome, raw_text, file_id = await get_welcome(chat.id)

    # Get user details
    u = await app.get_users(user_id)

    # If no custom welcome message is set, choose a random message
    if not raw_text:  # raw_text is empty or None
        raw_text = random.choice(RANDOM_WELCOME_MESSAGES)

    # Placeholder replacements
    text = raw_text
    keyb = None
    if findall(r".+\,.+", raw_text):
        text, keyb = extract_text_and_keyb(ikb, raw_text)

    # Replace placeholders with actual values
    if "{chatname}" in text:
        text = text.replace("{chatname}", chat.title)
    if "{mention}" in text:
        text = text.replace("{mention}", u.mention)
    if "{id}" in text:
        text = text.replace("{id}", f"`{user_id}`")
    if "{first}" in text:
        text = text.replace("{first}", u.first_name)
    if "{last}" in text:
        sname = u.last_name or "None"
        text = text.replace("{last}", sname)
    if "{username}" in text:
        susername = u.username or "None"
        text = text.replace("{username}", susername)
    if "{date}" in text:
        DATE = datetime.datetime.now().strftime("%Y-%m-%d")
        text = text.replace("{date}", DATE)
    if "{weekday}" in text:
        WEEKDAY = datetime.datetime.now().strftime("%A")
        text = text.replace("{weekday}", WEEKDAY)
    if "{time}" in text:
        TIME = datetime.datetime.now().strftime("%H:%M:%S")
        text = text.replace("{time}", f"{time} UTC")

    # Send welcome message based on type (Text, Photo, Animation)
    if not welcome or welcome == "Text":  # Default to text if no custom welcome is set
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


@app.on_message(filters.command("setwelcome") & ~filters.private)
@adminsOnly("can_change_info")
async def set_welcome_func(_, message):
    usage = "You need to reply to a text, gif or photo to set it as greetings.\n\nNotes: caption required for gif and photo."
    key = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="More Help",
                    url=f"t.me/{app.username}?start=greetings",
                )
            ],
        ]
    )
    replied_message = message.reply_to_message
    chat_id = message.chat.id
    try:
        if not replied_message:
            await message.reply_text(usage, reply_markup=key)
            return
        if replied_message.animation:
            welcome = "Animation"
            file_id = replied_message.animation.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.photo:
            welcome = "Photo"
            file_id = replied_message.photo.file_id
            text = replied_message.caption
            if not text:
                return await message.reply_text(usage, reply_markup=key)
            raw_text = text.markdown
        if replied_message.text:
            welcome = "Text"
            file_id = None
            text = replied_message.text
            raw_text = text.markdown
        if replied_message.reply_markup and not findall(r".+\,.+", raw_text):
            urls = extract_urls(replied_message.reply_markup)
            if urls:
                response = "\n".join(
                    [f"{name}=[{text}, {url}]" for name, text, url in urls]
                )
                raw_text = raw_text + response
        raw_text = await check_format(ikb, raw_text)
        if raw_text:
            await set_welcome(chat_id, welcome, raw_text, file_id)
            return await message.reply_text(
                "Welcome message has been successfully set."
            )
        else:
            return await message.reply_text(
                "Wrong formatting, check the help section.\n\n**Usage:**\nText: `Text`\nText + Buttons: `Text ~ Buttons`",
                reply_markup=key,
            )
    except UnboundLocalError:
        return await message.reply_text(
            "**Only Text, Gif and Photo welcome message are supported.**"
        )


@app.on_message(filters.command(["resetwelcome"]) & ~filters.private)
@adminsOnly("can_change_info")
async def del_welcome_func(_, message):
    chat_id = message.chat.id

    # Check if a custom welcome message is set
    welcome, raw_text, file_id = await get_welcome(chat_id)

    if not raw_text:  # Agar customize welcome message set nahi hai
        return await message.reply_text("What are you deleting‽ You haven't set up the custom welcome yet.")

    # Agar customize welcome message set hai, toh delete karenge
    await del_welcome(chat_id)
    await message.reply_text("Welcome message has been deleted.")


@app.on_message(filters.command("welcome") & ~filters.private)
@adminsOnly("can_change_info")
async def get_welcome_func(_, message):
    chat = message.chat
    welcome, raw_text, file_id = await get_welcome(chat.id)
    if not raw_text:
        return await message.reply_text("No welcome message set.")
    if not message.from_user:
        return await message.reply_text("You're anon, can't send welcome message.")

    await send_welcome_message(chat, message.from_user.id)

    await message.reply_text(
        f'Welcome: {welcome}\n\nFile_id: `{file_id}`\n\n`{raw_text.replace("`", "")}`'
    )