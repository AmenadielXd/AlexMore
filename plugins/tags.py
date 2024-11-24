from Alex import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [ "<b>ʜᴇʏ ʙᴀʙʏ ᴋᴀʜᴀ ʜᴏ 🤗</b>",
           "<b>ᴏʏᴇ sᴏ ɢʏᴇ ᴋʏᴀ ᴏɴʟɪɴᴇ ᴀᴀᴏ 😊</b>",
           "<b>ᴠᴄ ᴄʜᴀʟᴏ ʙᴀᴛᴇɴ ᴋᴀʀᴛᴇ ʜᴀɪɴ ᴋᴜᴄʜ ᴋᴜᴄʜ 😃</b>",
           "<b>ᴋʜᴀɴᴀ ᴋʜᴀ ʟɪʏᴇ ᴊɪ..?? 🥲</b>",
           "<b>ɢʜᴀʀ ᴍᴇ sᴀʙ ᴋᴀɪsᴇ ʜᴀɪɴ ᴊɪ 🥺</b>",
           "<b>ᴘᴛᴀ ʜᴀɪ ʙᴏʜᴏᴛ ᴍɪss ᴋᴀʀ ʀʜɪ ᴛʜɪ ᴀᴀᴘᴋᴏ 🤭</b>",
           "<b>ᴏʏᴇ ʜᴀʟ ᴄʜᴀʟ ᴋᴇsᴀ ʜᴀɪ..?? 🤨</b>",
           "<b>ᴍᴇʀɪ ʙʜɪ sᴇᴛᴛɪɴɢ ᴋᴀʀʙᴀ ᴅᴏɢᴇ..?? 🙂</b>",
           "<b>ᴀᴀᴘᴋᴀ ɴᴀᴍᴇ ᴋʏᴀ ʜᴀɪ..?? 🥲</b>",
           "<b>ɴᴀsᴛᴀ ʜᴜᴀ ᴀᴀᴘᴋᴀ..?? 😋</b>",
           "<b>ᴍᴇʀᴇ ᴋᴏ ᴀᴘɴᴇ ɢʀᴏᴜᴘ ᴍᴇ ᴋɪᴅɴᴀᴘ ᴋʀ ʟᴏ 😍</b>",
           "<b>ᴀᴀᴘᴋɪ ᴘᴀʀᴛɴᴇʀ ᴀᴀᴘᴋᴏ ᴅʜᴜɴᴅ ʀʜᴇ ʜᴀɪɴ ᴊʟᴅɪ ᴏɴʟɪɴᴇ ᴀʏɪᴀᴇ 😅</b>",
           "<b>ᴍᴇʀᴇ sᴇ ᴅᴏsᴛɪ ᴋʀᴏɢᴇ..?? 🤔</b>",
           "<b>sᴏɴᴇ ᴄʜᴀʟ ɢʏᴇ ᴋʏᴀ 🙄</b>",
           "<b>ᴇᴋ sᴏɴɢ ᴘʟᴀʏ ᴋʀᴏ ɴᴀ ᴘʟss 😕</b>",
           "<b>ᴀᴀᴘ ᴋᴀʜᴀ sᴇ ʜᴏ..?? 🙃</b>",
           "<b>ʜᴇʟʟᴏ ᴊɪ ɴᴀᴍᴀsᴛᴇ 😛</b>",
           "<b>ʜᴇʟʟᴏ ʙᴀʙʏ ᴋᴋʀʜ..? 🤔</b>",
           "<b>ᴅᴏ ʏᴏᴜ ᴋɴᴏᴡ ᴡʜᴏ ɪs ᴍʏ ᴏᴡɴᴇʀ.? ☺️</b>",
           "<b>ᴄʜʟᴏ ᴋᴜᴄʜ ɢᴀᴍᴇ ᴋʜᴇʟᴛᴇ ʜᴀɪɴ.🤗</b>",
           "<b>ᴀᴜʀ ʙᴀᴛᴀᴏ ᴋᴀɪsᴇ ʜᴏ ʙᴀʙʏ 😇</b>",
           "<b>ᴛᴜᴍʜᴀʀɪ ᴍᴜᴍᴍʏ ᴋʏᴀ ᴋᴀʀ ʀᴀʜɪ ʜᴀɪ 🤭</b>",
           "<b>ᴍᴇʀᴇ sᴇ ʙᴀᴛ ɴᴏɪ ᴋʀᴏɢᴇ 🥺</b>",
           "<b>ᴏʏᴇ ᴘᴀɢᴀʟ ᴏɴʟɪɴᴇ ᴀᴀ ᴊᴀ 😶</b>",
           "<b>ᴀᴀᴊ ʜᴏʟɪᴅᴀʏ ʜᴀɪ ᴋʏᴀ sᴄʜᴏᴏʟ ᴍᴇ..?? 🤔</b>",
           "<b>ᴏʏᴇ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ 😜</b>",
           "<b>sᴜɴᴏ ᴇᴋ ᴋᴀᴍ ʜᴀɪ ᴛᴜᴍsᴇ 🙂</b>",
           "<b>ᴋᴏɪ sᴏɴɢ ᴘʟᴀʏ ᴋʀᴏ ɴᴀ 😪</b>",
           "<b>ɴɪᴄᴇ ᴛᴏ ᴍᴇᴇᴛ ᴜʜ ☺</b>",
           "<b>ᴍᴇʀᴀ ʙᴀʙᴜ ɴᴇ ᴛʜᴀɴᴀ ᴋʜᴀʏᴀ ᴋʏᴀ..? 🙊</b>",
           "<b>sᴛᴜᴅʏ ᴄᴏᴍᴘʟᴇᴛᴇ ʜᴜᴀ?? 😺</b>",
           "<b>ʙᴏʟᴏ ɴᴀ ᴋᴜᴄʜ ʏʀʀ 🥲</b>",
           "<b>sᴏɴᴀʟɪ ᴋᴏɴ ʜᴀɪ...?? 😅</b>",
           "<b>ᴛᴜᴍʜᴀʀɪ ᴇᴋ ᴘɪᴄ ᴍɪʟᴇɢɪ..? 😅</b>",
           "<b>ᴍᴜᴍᴍʏ ᴀᴀ ɢʏɪ ᴋʏᴀ 😆</b>",
           "<b>ᴏʀ ʙᴀᴛᴀᴏ ʙʜᴀʙʜɪ ᴋᴀɪsɪ ʜᴀɪ 😉</b>",
           "<b>ɪ ʟᴏᴠᴇ ʏᴏᴜ 💚</b>",
           "<b>ᴅᴏ ʏᴏᴜ ʟᴏᴠᴇ ᴍᴇ..? 👀</b>",
           "<b>ʀᴀᴋʜɪ ᴋᴀʙ ʙᴀɴᴅ ʀᴀʜɪ ʜᴏ..?? 🙉</b>",
           "<b>ᴇᴋ sᴏɴɢ sᴜɴᴀᴜ..? 😹</b>",
           "<b>ᴏɴʟɪɴᴇ ᴀᴀ ᴊᴀ ʀᴇ sᴏɴɢ sᴜɴᴀ ʀᴀʜɪ ʜᴜ 😻</b>",
           "<b>ɪɴsᴛᴀɢʀᴀᴍ ᴄʜᴀʟᴀᴛᴇ ʜᴏ..?? 🙃</b>",
           "<b>ᴡʜᴀᴛsᴀᴘᴘ ɴᴜᴍʙᴇʀ ᴅᴏɢᴇ ᴀᴘɴᴀ ᴛᴜᴍ..? 😕</b>",
           "<b>ᴛᴜᴍʜᴇ ᴋᴏɴ sᴀ ᴍᴜsɪᴄ sᴜɴɴᴀ ᴘᴀsᴀɴᴅ ʜᴀɪ..? 🙃</b>",
           "<b>sᴀʀᴀ ᴋᴀᴍ ᴋʜᴀᴛᴀᴍ ʜᴏ ɢʏᴀ ᴀᴀᴘᴋᴀ..? 🙃</b>",
           "<b>ᴋᴀʜᴀ sᴇ ʜᴏ ᴀᴀᴘ 😊</b>",
           "<b>sᴜɴᴏ ɴᴀ 🧐</b>",
           "<b>ᴍᴇʀᴀ ᴇᴋ ᴋᴀᴀᴍ ᴋᴀʀ ᴅᴏɢᴇ..? ♥️</b>",
           "<b>ʙʏ ᴛᴀᴛᴀ ᴍᴀᴛ ʙᴀᴀᴛ ᴋᴀʀɴᴀ ᴀᴀᴊ ᴋᴇ ʙᴀᴅ 😠</b>",
           "<b>ᴍᴏᴍ ᴅᴀᴅ ᴋᴀɪsᴇ ʜᴀɪɴ..? ❤</b>",
           "<b>ᴋʏᴀ ʜᴜᴀ..? 🤔</b>",
           "<b>ʙᴏʜᴏᴛ ʏᴀᴀᴅ ᴀᴀ ʀʜɪ ʜᴀɪ 😒</b>",
           "<b>ʙʜᴜʟ ɢʏᴇ ᴍᴜᴊʜᴇ 😏</b>",
           "<b>ᴊᴜᴛʜ ɴʜɪ ʙᴏʟɴᴀ ᴄʜᴀʜɪʏᴇ 🤐</b>",
           "<b>ᴋʜᴀ ʟᴏ ʙʜᴀᴡ ᴍᴀᴛ ᴋʀᴏ ʙᴀᴀᴛ 😒</b>",
           "<b>ᴋʏᴀ ʜᴜᴀ 😮</b>"
           "<b>ʜɪɪ ʜᴏɪ ʜᴇʟʟᴏ 👀</b>",
           "<b>ᴀᴀᴘᴋᴇ ᴊᴀɪsᴀ ᴅᴏsᴛ ʜᴏ sᴀᴛʜ ᴍᴇ ғɪʀ ɢᴜᴍ ᴋɪs ʙᴀᴀᴛ ᴋᴀ 🙈</b>",
           "<b>ᴀᴀᴊ ᴍᴇ sᴀᴅ ʜᴏᴏɴ ☹️</b>",
           "<b>ᴍᴜsᴊʜsᴇ ʙʜɪ ʙᴀᴀᴛ ᴋᴀʀ ʟᴏ ɴᴀ 🥺</b>",
           "<b>ᴋʏᴀ ᴋᴀʀ ʀᴀʜᴇ ʜᴏ 👀</b>",
           "<b>ᴋʏᴀ ʜᴀʟ ᴄʜᴀʟ ʜᴀɪ 🙂</b>",
           "<b>ᴋᴀʜᴀ sᴇ ʜᴏ ᴀᴀᴘ..?🤔</b>",
           "<b>ᴄʜᴀᴛᴛɪɴɢ ᴋᴀʀ ʟᴏ ɴᴀ..🥺</b>",
           "<b>ᴍᴇ ᴍᴀsᴏᴏᴍ ʜᴜ ɴᴀ 🥺</b>",
           "<b>ᴋᴀʟ ᴍᴀᴊᴀ ᴀʏᴀ ᴛʜᴀ ɴᴀ 😅</b>",
           "<b>ɢʀᴏᴜᴘ ᴍᴇ ʙᴀᴀᴛ ᴋʏᴜ ɴᴀʜɪ ᴋᴀʀᴛᴇ ʜᴏ 😕</b>",
           "<b>ᴀᴀᴘ ʀᴇʟᴀᴛɪᴏᴍsʜɪᴘ ᴍᴇ ʜᴏ..? 👀</b>",
           "<b>ᴋɪᴛɴᴀ ᴄʜᴜᴘ ʀᴀʜᴛᴇ ʜᴏ ʏʀʀ 😼</b>",
           "<b>ᴀᴀᴘᴋᴏ ɢᴀɴᴀ ɢᴀɴᴇ ᴀᴀᴛᴀ ʜᴀɪ..? 😸</b>",
           "<b>ɢʜᴜᴍɴᴇ ᴄʜᴀʟᴏɢᴇ..?? 🙈</b>",
           "<b>ᴋʜᴜs ʀᴀʜᴀ ᴋᴀʀᴏ 🤞</b>",
           "<b>ʜᴀᴍ ᴅᴏsᴛ ʙᴀɴ sᴀᴋᴛᴇ ʜᴀɪ...? 🥰</b>",
           "<b>ᴋᴜᴄʜ ʙᴏʟ ᴋʏᴜ ɴʜɪ ʀᴀʜᴇ ʜᴏ.. 🥺</b>",
           "<b>ᴋᴜᴄʜ ᴍᴇᴍʙᴇʀs ᴀᴅᴅ ᴋᴀʀ ᴅᴏ 🥲</b>",
           "<b>sɪɴɢʟᴇ ʜᴏ ʏᴀ ᴍɪɴɢʟᴇ 😉</b>",
           "<b>ᴀᴀᴏ ᴘᴀʀᴛʏ ᴋᴀʀᴛᴇ ʜᴀɪɴ 🥳</b>",
           "<b>ʙɪᴏ ᴍᴇ ʟɪɴᴋ ʜᴀɪ ᴊᴏɪɴ ᴋᴀʀ ʟᴏ 🧐</b>",
           "<b>ᴍᴜᴊʜᴇ ʙʜᴜʟ ɢʏᴇ ᴋʏᴀ 🥺</b>",
           "<b>ʏᴀʜᴀ ᴀᴀ ᴊᴀᴏ @thexparadise ᴍᴀsᴛɪ ᴋᴀʀᴇɴɢᴇ 🤭</b>",
           "<b>ᴛʀᴜᴛʜ ᴀɴᴅ ᴅᴀʀᴇ ᴋʜᴇʟᴏɢᴇ..? 😊</b>",
           "<b>ᴀᴀᴊ ᴍᴜᴍᴍʏ ɴᴇ ᴅᴀᴛᴀ ʏʀʀ 🥺</b>",
           "<b>ᴊᴏɪɴ ᴋᴀʀ ʟᴏ 🤗</b>",
           "<b>ᴇᴋ ᴅɪʟ ʜᴀɪ ᴇᴋ ᴅɪʟ ʜɪ ᴛᴏ ʜᴀɪ 😗</b>",
           "<b>ᴛᴜᴍʜᴀʀᴇ ᴅᴏsᴛ ᴋᴀʜᴀ ɢʏᴇv🥺</b>",
           "<b>ᴍᴇᴛ ᴍʏ ᴏᴡɴᴇʀ @itslucciii 🥰</b>",
           "<b>ᴋᴀʜᴀ ᴋʜᴏʏᴇ ʜᴏ ᴊᴀᴀɴ 😜</b>",
           "<b>ɢᴏᴏᴅ ɴɪɢʜᴛ ᴊɪ ʙʜᴜᴛ ʀᴀᴛ ʜᴏ ɢʏɪ 🥰</b>",
           ]

VC_TAG = [ "<b>ᴏʏᴇ ᴠᴄ ᴀᴀᴏ ɴᴀ ᴘʟs 😒</b>",
         "<b>ᴊᴏɪɴ ᴠᴄ ғᴀsᴛ ɪᴛs ɪᴍᴀᴘᴏʀᴛᴀɴᴛ 😐</b>",
         "<b>ʙᴀʙʏ ᴄᴏᴍᴇ ᴏɴ ᴠᴄ ғᴀsᴛ 🙄</b>",
         "<b>ᴄʜᴜᴘ ᴄʜᴀᴘ ᴠᴄ ᴘʀ ᴀᴀᴏ 🤫</b>",
         "<b>ᴍᴀɪɴ ᴠᴄ ᴍᴇ ᴛᴜᴍᴀʀᴀ ᴡᴀɪᴛ ᴋʀ ʀʜɪ 🥺</b>",
         "<b>ᴠᴄ ᴘᴀʀ ᴀᴀᴏ ʙᴀᴀᴛ ᴋʀᴛᴇ ʜᴀɪ ☺️</b>",
         "<b>ʙᴀʙᴜ ᴠᴄ ᴀᴀ ᴊᴀɪʏᴇ ᴇᴋ ʙᴀʀ 🤨</b>",
         "<b>ᴠᴄ ᴘᴀʀ ʏᴇ ʀᴜssɪᴀɴ ᴋʏᴀ ᴋᴀʀ ʀʜɪ ʜᴀɪ 😮‍💨</b>",
         "<b>ᴠᴄ ᴘᴀʀ ᴀᴀᴏ ᴠᴀʀɴᴀ ʙᴀɴ ʜᴏ ᴊᴀᴏɢᴇ 🤭</b>",
         "<b>sᴏʀʀʏ ʙᴀʙʏ ᴘʟs ᴠᴄ ᴀᴀ ᴊᴀᴏ ɴᴀ 😢</b>",
         "<b>ᴠᴄ ᴀᴀɴᴀ ᴇᴋ ᴄʜɪᴊ ᴅɪᴋʜᴀᴛɪ ʜᴜ 😮</b>",
         "<b>ᴠᴄ ᴍᴇ ᴄʜᴇᴄᴋ ᴋʀᴋᴇ ʙᴀᴛᴀɴᴀ ᴋᴏɴ sᴀ sᴏɴɢ ᴘʟᴀʏ ʜᴏ ʀʜᴀ ʜᴀɪ.. 💫</b>",
         "<b>ᴠᴄ ᴊᴏɪɴ ᴋʀɴᴇ ᴍᴇ ᴋʏᴀ ᴊᴀᴛᴀ ʜᴀɪ ᴛʜᴏʀᴀ ᴅᴇʀ ᴋᴀʀ ʟᴏ ɴᴀ 😇</b>",
         "<b>ᴊᴀɴᴇᴍᴀɴ ᴠᴄ ᴀᴀᴏ ɴᴀ ʟɪᴠᴇ sʜᴏᴡ ᴅɪᴋʜᴀᴛɪ ʜᴏᴏɴ.. 😵‍💫</b>",
         "<b>ᴏᴡɴᴇʀ ʙᴀʙᴜ ᴠᴄ ᴛᴀᴘᴋᴏ ɴᴀ... 😕</b>",
         "<b>ʜᴇʏ ᴄᴜᴛɪᴇ ᴠᴄ ᴀᴀɴᴀ ᴛᴏ ᴇᴋ ʙᴀᴀʀ... 🌟</b>",
         "<b>ᴠᴄ ᴘᴀʀ ᴀᴀ ʀʜᴇ ʜᴏ ʏᴀ ɴᴀ... ✨</b>",
         "<b>ᴠᴄ ᴘᴀʀ ᴀᴀ ᴊᴀ ᴠʀɴᴀ ɢʜᴀʀ sᴇ ᴜᴛʜᴡᴀ ᴅᴜɴɢɪ... 🌝</b>",
         "<b>ʙᴀʙʏ ᴠᴄ ᴘᴀʀ ᴋʙ ᴀᴀ ʀʜᴇ ʜᴏ. 💯</b>",
        ]

HITAG = [ "<b>❅ बेबी कहा हो। 🤗</b>",
           "<b>❅ ओए सो गए क्या, ऑनलाइन आओ ।😊</b>",
           "<b>❅ ओए वीसी आओ बात करते हैं । 😃</b>",
           "<b>❅ खाना खाया कि नही। 🥲</b>",
           "<b>❅ घर में सब कैसे हैं। 🥺</b>",
           "<b>❅ पता है बहुत याद आ रही आपकी। 🤭</b>",
           "<b>❅ और बताओ कैसे हो।..?? 🤨</b>",
           "<b>❅ मेरी भी सैटिंग करवा दो प्लीज..?? 🙂</b>",
           "<b>❅ आपका नाम क्या है।..?? 🥲</b>",
           "<b>❅ नाश्ता हो गया..?? 😋</b>",
           "<b>❅ मुझे अपने ग्रूप में ऐड कर लो। 😍</b>",
           "<b>❅ आपका दोस्त आपको बुला रहा है। 😅</b>",
           "<b>❅ मुझसे शादी करोगे ..?? 🤔</b>",
           "<b>❅ सोने चले गए क्या 🙄</b>",
           "<b>❅ अरे यार कोई AC चला दो 😕</b>",
           "<b>❅ आप कहा से हो..?? 🙃</b>",
           "<b>❅ हेलो जी नमस्ते 😛</b>",
           "<b>❅ BABY क्या कर रही हो..? 🤔</b>",
           "<b>❅ क्या आप मुझे जानते हो .? ☺️</b>",
           "<b>❅ आओ baby Ludo खेलते है .🤗</b>",
           "<b>❅ चलती है क्या 9 से 12... 😇</b>",
           "<b>❅ आपके पापा क्या करते है 🤭</b>",
           "<b>❅ आओ baby बाजार चलते है गोलगप्पे खाने। 🥺</b>",
           "<b>❅ अकेली ना बाजार जाया करो, नज़र लग जायेगी। 😶</b>",
           "<b>❅ और बताओ BF कैसा है ..?? 🤔</b>",
           "<b>❅ गुड मॉर्निंग 😜</b>",
           "<b>❅ मेरा एक काम करोगे। 🙂</b>",
           "<b>❅ DJ वाले बाबू मेरा गाना चला दो। 😪</b>",
           "<b>❅ आप से मिलकर अच्छा लगा।☺</b>",
           "<b>❅ मेरे बाबू ने थाना थाया।..? 🙊</b>",
           "<b>❅ पढ़ाई कैसी चल रही हैं ? 😺</b>",
           "<b>❅ हम को प्यार हुआ। 🥲</b>",
           "<b>❅ Nykaa कौन है...? 😅</b>",
           "<b>❅ तू खींच मेरी फ़ोटो ..? 😅</b>",
           "<b>❅ Phone काट मम्मी आ गई क्या। 😆</b>",
           "<b>❅ और भाबी से कब मिल वा रहे हो । 😉</b>",
           "<b>❅ क्या आप मुझसे प्यार करते हो 💚</b>",
           "<b>❅ मैं तुम से बहुत प्यार करती हूं..? 👀</b>",
           "<b>❅ बेबी एक kiss दो ना..?? 🙉</b>",
           "<b>❅ एक जॉक सुनाऊं..? 😹</b>",
           "<b>❅ vc पर आओ कुछ दिखाती हूं  😻</b>",
           "<b>❅ क्या तुम instagram चलते हो..?? 🙃</b>",
           "<b>❅ whatsapp नंबर दो ना अपना..? 😕</b>",
           "<b>❅ आप की दोस्त से मेरी सेटिंग करा दो ..? 🙃</b>",
           "<b>❅ सारा काम हो गया हो तो ऑनलाइन आ जाओ।..? 🙃</b>",
           "<b>❅ कहा से हो आप 😊** ",
           "<b>❅ जा तुझे आज़ाद कर दिया मैंने मेरे दिल से। 🥺</b>",
           "<b>❅ मेरा एक काम करोगे, ग्रूप मे कुछ मेंबर ऐड कर दो ..? ♥️</b>",
           "<b>❅ मैं तुमसे नाराज़ हूं 😠</b>",
           "<b>❅ आपकी फैमिली कैसी है..? ❤</b>",
           "<b>❅ क्या हुआ..? 🤔</b>",
           "<b>❅ बहुत याद आ रही है आपकी 😒</b>",
           "<b>❅ भूल गए मुझे 😏</b>",
           "<b>❅ झूठ क्यों बोला आपने मुझसे 🤐</b>",
           "<b>❅ इतना भाव मत खाया करो, रोटी खाया करो कम से कम मोटी तो हो जाओगी 😒</b>",
           "<b>❅ ये attitude किसे दिखा रहे हो 😮</b>",
           "<b>❅ हेमलो कहा busy ho 👀</b>",
           "<b>❅ आपके जैसा दोस्त पाकर मे बहुत खुश हूं। 🙈</b>",
           "<b>❅ आज मन बहुत उदास है ☹️</b>",
           "<b>❅ मुझसे भी बात कर लो ना 🥺</b>",
           "<b>❅ आज खाने में क्या बनाया है 👀</b>",
           "<b>❅ क्या चल रहा है 🙂</b>",
           "<b>❅ message क्यों नहीं करती हो..🥺</b>",
           "<b>❅ मैं मासूम हूं ना 🥺</b>",
           "<b>❅ कल मज़ा आया था ना 😅</b>",
           "<b>❅ कल कहा busy थे 😕</b>",
           "<b>❅ आप relationship में हो क्या..? 👀</b>",
           "<b>❅ कितने शांत रहते हो यार आप 😼</b>",
           "<b>❅ आपको गाना, गाना आता है..? 😸</b>",
           "<b>❅ घूमने चलोगे मेरे साथ..?? 🙈</b>",
           "<b>❅ हमेशा हैप्पी रहा करो यार 🤞</b>",
           "<b>❅ क्या हम दोस्त बन सकते है...? 🥰</b>",
           "<b>❅ आप का विवाह हो गया क्या.. 🥺</b>",
           "<b>❅ कहा busy the इतने दिनों से 🥲</b>",
           "<b>❅ single हो या mingle 😉</b>",
           "<b>❅ आओ पार्टी करते है 🥳</b>",
           "<b>❅ Bio में link हैं join कर लो 🧐</b>",
           "<b>❅ मैं तुमसे प्यार नहीं करती, 🥺</b>",
           "<b>❅ यहां आ जाओ ना @the_losthope मस्ती करेंगे 🤭</b>",
           "<b>❅ भूल जाओ मुझे,..? 😊</b>",
           "<b>❅ अपना बना ले पिया, अपना बना ले 🥺</b>",
           "<b>❅ मेरा ग्रुप भी join कर लो ना 🤗</b>",
           "<b>❅ मैने तेरा नाम Dil rakh diya 😗</b>",
           "<b>❅ तुमारे सारे दोस्त कहा गए 🥺</b>",
           "<b>❅ met my owner @itslucciii 🥰</b>",
           "<b>❅ किसकी याद मे खोए हो जान 😜</b>",
           "<b>❅ गुड नाईट जी बहुत रात हो गई 🥰</b>",
           ]

LYF_TAG = [ "<b>❅ ɪғ ʏᴏᴜ ᴅᴏ ɴᴏᴛ sᴛᴇᴘ ғᴏʀᴡᴀʀᴅ ʏᴏᴜ ᴡɪʟʟ ʀᴇᴍᴀɪɴ ɪɴ ᴛʜᴇ sᴀᴍᴇ ᴘʟᴀᴄᴇ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʜᴀʀᴅ ʙᴜᴛ ɴᴏᴛ ɪᴍᴘᴏssɪʙʟᴇ.</b>",
         "<b>❅ ʟɪғᴇ’s ᴛᴏᴏ sʜᴏʀᴛ ᴛᴏ ᴀʀɢᴜᴇ ᴀɴᴅ ғɪɢʜᴛ.</b>",
         "<b>❅ ᴅᴏɴ’ᴛ ᴡᴀɪᴛ ғᴏʀ ᴛʜᴇ ᴘᴇʀғᴇᴄᴛ ᴍᴏᴍᴇɴᴛ ᴛᴀᴋᴇ ᴍᴏᴍᴇɴᴛ ᴀɴᴅ ᴍᴀᴋᴇ ɪᴛ ᴘᴇʀғᴇᴄᴛ.</b>",
         "<b>❅ sɪʟᴇɴᴄᴇ ɪs ᴛʜᴇ ʙᴇsᴛ ᴀɴsᴡᴇʀ ᴛᴏ sᴏᴍᴇᴏɴᴇ ᴡʜᴏ ᴅᴏᴇsɴ’ᴛ ᴠᴀʟᴜᴇ ʏᴏᴜʀ ᴡᴏʀᴅs.</b>",
         "<b>❅ ᴇᴠᴇʀʏ ɴᴇᴡ ᴅᴀʏ ɪs ᴀ ᴄʜᴀɴᴄᴇ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ʟɪғᴇ.</b>",
         "<b>❅ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ʟɪғᴇ, ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴘʀɪᴏʀɪᴛɪᴇs.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ᴊᴏᴜʀɴᴇʏ, ɴᴏᴛ ᴀ ʀᴀᴄᴇ..</b>",
         "<b>❅ sᴍɪʟᴇ ᴀɴᴅ ᴅᴏɴ’ᴛ ᴡᴏʀʀʏ, ʟɪғᴇ ɪs ᴀᴡᴇsᴏᴍᴇ.</b>",
         "<b>❅ ᴅᴏ ɴᴏᴛ ᴄᴏᴍᴘᴀʀᴇ ʏᴏᴜʀsᴇʟғ ᴛᴏ ᴏᴛʜᴇʀs ɪғ ʏᴏᴜ ᴅᴏ sᴏ ʏᴏᴜ ᴀʀᴇ ɪɴsᴜʟᴛɪɴɢ ʏᴏᴜʀsᴇʟғ.</b>",
         "<b>❅ ɪ ᴀᴍ ɪɴ ᴛʜᴇ ᴘʀᴏᴄᴇss ᴏғ ʙᴇᴄᴏᴍɪɴɢ ᴛʜᴇ ʙᴇsᴛ ᴠᴇʀsɪᴏɴ ᴏғ ᴍʏsᴇʟғ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʟɪᴋᴇ ɪᴄᴇ ᴇɴᴊᴏʏ ɪᴛ ʙᴇғᴏʀᴇ ɪᴛ ᴍᴇʟᴛs.</b>",
         "<b>❅ ʙᴇ ғʀᴇᴇ ʟɪᴋᴇ ᴀ ʙɪʀᴅ.</b>",
         "<b>❅ ɴᴏ ᴏɴᴇ ɪs ᴄᴏᴍɪɴɢ ᴛᴏ sᴀᴠᴇ ʏᴏᴜ. ᴛʜɪs ʟɪғᴇ ᴏғ ʏᴏᴜʀ ɪs 100% ʏᴏᴜʀ ʀᴇsᴘᴏɴsɪʙɪʟɪᴛʏ..</b>",
         "<b>❅ ʟɪғᴇ ᴀʟᴡᴀʏs ᴏғғᴇʀs ʏᴏᴜ ᴀ sᴇᴄᴏɴᴅ ᴄʜᴀɴᴄᴇ. ɪᴛ’s ᴄᴀʟʟᴇᴅ ᴛᴏᴍᴏʀʀᴏᴡ.</b>",
         "<b>❅ ʟɪғᴇ ʙᴇɢɪɴs ᴀᴛ ᴛʜᴇ ᴇɴᴅ ᴏғ ʏᴏᴜʀ ᴄᴏᴍғᴏʀᴛ ᴢᴏɴᴇ.</b>",
         "<b>❅ ᴀʟʟ ᴛʜᴇ ᴛʜɪɴɢs ᴛʜᴀᴛ ʜᴜʀᴛ ʏᴏᴜ, ᴀᴄᴛᴜᴀʟʟʏ ᴛᴇᴀᴄʜ ʏᴏᴜ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʟɪᴋᴇ ᴀ ᴄᴀᴍᴇʀᴀ. sᴏ ғᴀᴄᴇ ɪᴛ ᴡɪᴛʜ ᴀ sᴍɪʟᴇ.</b>",
         "<b>❅ ʟɪғᴇ ɪs 10% ᴏғ ᴡʜᴀᴛ ʜᴀᴘᴘᴇɴs ᴛᴏ ʏᴏᴜ ᴀɴᴅ 90% ᴏғ ʜᴏᴡ ʏᴏᴜ ʀᴇsᴘᴏɴᴅ ᴛᴏ ɪᴛ.</b>",
         "<b>❅ ʟɪғᴇ ᴀʟᴡᴀʏs ᴏғғᴇʀs ʏᴏᴜ ᴀ sᴇᴄᴏɴᴅ ᴄʜᴀɴᴄᴇ. ɪᴛ’s ᴄᴀʟʟᴇᴅ ᴛᴏᴍᴏʀʀᴏᴡ.</b>",
         "<b>❅ ɴᴏ ᴏɴᴇ ɪs ᴄᴏᴍɪɴɢ ᴛᴏ sᴀᴠᴇ ʏᴏᴜ. ᴛʜɪs ʟɪғᴇ ᴏғ ʏᴏᴜʀ ɪs 100% ʏᴏᴜʀ ʀᴇsᴘᴏɴsɪʙɪʟɪᴛʏ..</b>",
         "<b>❅ ʟɪғᴇ ɪs ɴᴏᴛ ᴀɴ ᴇᴀsʏ ᴛᴀsᴋ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ᴡᴏɴᴅᴇʀғᴜʟ ᴀᴅᴠᴇɴᴛᴜʀᴇ.</b>",
         "<b>❅ ʟɪғᴇ ʙᴇɢɪɴs ᴏɴ ᴛʜᴇ ᴏᴛʜᴇʀ sɪᴅᴇ ᴏғ ᴅᴇsᴘᴀɪʀ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ɴᴏᴛ ᴀ ᴘʀᴏʙʟᴇᴍ ᴛᴏ ʙᴇ sᴏʟᴠᴇᴅ ʙᴜᴛ ᴀ ʀᴇᴀʟɪᴛʏ ᴛᴏ ʙᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇᴅ.</b>",
         "<b>❅ ʟɪғᴇ ᴅᴏᴇs ɴᴏᴛ ʜᴀᴠᴇ ᴀ ʀᴇᴍᴏᴛᴇ; ɢᴇᴛ ᴜᴘ ᴀɴᴅ ᴄʜᴀɴɢᴇ ɪᴛ ʏᴏᴜʀsᴇʟғ.</b>",
         "<b>❅ sᴛᴀʀᴛ ᴛʀᴜsᴛɪɴɢ ʏᴏᴜʀsᴇʟғ, ᴀɴᴅ ʏᴏᴜ’ʟʟ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ʟɪᴠᴇ.</b>",
         "<b>❅ ʜᴇᴀʟᴛʜ ɪs ᴛʜᴇ ᴍᴏsᴛ ɪᴍᴘᴏʀᴛᴀɴᴛ ɢᴏᴏᴅ ᴏғ ʟɪғᴇ.</b>",
         "<b>❅ ᴛɪᴍᴇ ᴄʜᴀɴɢᴇ ᴘʀɪᴏʀɪᴛʏ ᴄʜᴀɴɢᴇs.</b>",
         "<b>❅ ᴛᴏ sᴇᴇ ᴀɴᴅ ᴛᴏ ғᴇᴇʟ ᴍᴇᴀɴs ᴛᴏ ʙᴇ, ᴛʜɪɴᴋ ᴀɴᴅ ʟɪᴠᴇ.</b>",
         "<b>❅ ʙᴇ ᴡɪᴛʜ sᴏᴍᴇᴏɴᴇ ᴡʜᴏ ʙʀɪɴɢs ᴏᴜᴛ ᴛʜᴇ ʙᴇsᴛ ᴏғ ʏᴏᴜ.</b>",
         "<b>❅ ʏᴏᴜʀ ᴛʜᴏᴜɢʜᴛs ᴀʀᴇ ʏᴏᴜʀ ʟɪғᴇ.</b>",
         "<b>❅ ᴘᴇᴏᴘʟᴇ ᴄʜᴀɴɢᴇ, ᴍᴇᴍᴏʀɪᴇs ᴅᴏɴ’ᴛ.</b>",
         "<b>❅ ᴏᴜʀ ʟɪғᴇ ɪs ᴡʜᴀᴛ ᴡᴇ ᴛʜɪɴᴋ ɪᴛ ɪs.</b>",
         "<b>❅ ʟɪɢʜᴛ ʜᴇᴀʀᴛ ʟɪᴠᴇs ʟᴏɴɢᴇʀ.</b>",
         "<b>❅ ᴅᴇᴘʀᴇssɪᴏɴ ᴇᴠᴇɴᴛᴜᴀʟʟʏ ʙᴇᴄᴏᴍᴇs ᴀ ʜᴀʙɪᴛ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ɢɪғᴛ. ᴛʀᴇᴀᴛ ɪᴛ ᴡᴇʟʟ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴡʜᴀᴛ ᴏᴜʀ ғᴇᴇʟɪɴɢs ᴅᴏ ᴡɪᴛʜ ᴜs.</b>",
         "<b>❅ ᴡʀɪɴᴋʟᴇs ᴀʀᴇ ᴛʜᴇ ʟɪɴᴇs ᴏғ ʟɪғᴇ ᴏɴ ᴛʜᴇ ғᴀᴄᴇ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴍᴀᴅᴇ ᴜᴘ ᴏғ sᴏʙs, sɴɪғғʟᴇs, ᴀɴᴅ sᴍɪʟᴇs.</b>",
         "<b>❅ ɴᴏᴛ ʟɪғᴇ, ʙᴜᴛ ɢᴏᴏᴅ ʟɪғᴇ, ɪs ᴛᴏ ʙᴇ ᴄʜɪᴇғʟʏ ᴠᴀʟᴜᴇᴅ.</b>",
         "<b>❅ ʏᴏᴜ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ʟɪғᴇ ʙʏ ᴄʜᴀɴɢɪɴɢ ʏᴏᴜʀ ʜᴇᴀʀᴛ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ɴᴏᴛʜɪɴɢ ᴡɪᴛʜᴏᴜᴛ ᴛʀᴜᴇ ғʀɪᴇɴᴅsʜɪᴘ.</b>",
         "<b>❅ ɪғ ʏᴏᴜ ᴀʀᴇ ʙʀᴀᴠᴇ ᴛᴏ sᴀʏ ɢᴏᴏᴅ ʙʏᴇ, ʟɪғᴇ ᴡɪʟʟ ʀᴇᴡᴀʀᴅ ʏᴏᴜ ᴡɪᴛʜ ᴀ ɴᴇᴡ ʜᴇʟʟᴏ.</b>",
         "<b>❅ ᴛʜᴇʀᴇ ɪs ɴᴏᴛʜɪɴɢ ᴍᴏʀᴇ ᴇxᴄɪᴛɪɴɢ ɪɴ ᴛʜᴇ ᴡᴏʀʟᴅ, ʙᴜᴛ ᴘᴇᴏᴘʟᴇ.</b>",
         "<b>❅ ʏᴏᴜ ᴄᴀɴ ᴅᴏ ᴀɴʏᴛʜɪɴɢ, ʙᴜᴛ ɴᴏᴛ ᴇᴠᴇʀʏᴛʜɪɴɢ.</b>",
         "<b>❅ ʟɪғᴇ ʙᴇᴄᴏᴍᴇ ᴇᴀsʏ ᴡʜᴇɴ ʏᴏᴜ ʙᴇᴄᴏᴍᴇ sᴛʀᴏɴɢ.</b>",
         "<b>❅ ᴍʏ ʟɪғᴇ ɪsɴ’ᴛ ᴘᴇʀғᴇᴄᴛ ʙᴜᴛ ɪᴛ ᴅᴏᴇs ʜᴀᴠᴇ ᴘᴇʀғᴇᴄᴛ ᴍᴏᴍᴇɴᴛs.</b>",
         "<b>❅ ʟɪғᴇ ɪs ɢᴏᴅ’s ɴᴏᴠᴇʟ. ʟᴇᴛ ʜɪᴍ ᴡʀɪᴛᴇ ɪᴛ.</b>",
         "<b>❅ ᴏᴜʀ ʟɪғᴇ ɪs ᴀ ʀᴇsᴜʟᴛ ᴏғ ᴏᴜʀ ᴅᴏᴍɪɴᴀɴᴛ ᴛʜᴏᴜɢʜᴛs.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ᴍᴏᴛɪᴏɴ ғʀᴏᴍ ᴀ ᴅᴇsɪʀᴇ ᴛᴏ ᴀɴᴏᴛʜᴇʀ ᴅᴇsɪʀᴇ.</b>",
         "<b>❅ ᴛᴏ ʟɪᴠᴇ ᴍᴇᴀɴs ᴛᴏ ғɪɢʜᴛ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʟɪᴋᴇ ᴀ ᴍᴏᴜɴᴛᴀɪɴ, ɴᴏᴛ ᴀ ʙᴇᴀᴄʜ.</b>",
         "<b>❅ ᴛʜᴇ ᴡᴏʀsᴛ ᴛʜɪɴɢ ɪɴ ʟɪғᴇ ɪs ᴛʜᴀᴛ ɪᴛ ᴘᴀssᴇs.</b>",
         "<b>❅ ʟɪғᴇ ɪs sɪᴍᴘʟᴇ ɪғ ᴡᴇ ᴀʀᴇ sɪᴍᴘʟᴇ.</b>",
         "<b>❅ ᴀʟᴡᴀʏs ᴛʜɪɴᴋ ᴛᴡɪᴄᴇ, sᴘᴇᴀᴋ ᴏɴᴄᴇ.</b>",
         "<b>❅ ʟɪғᴇ ɪs sɪᴍᴘʟᴇ, ᴡᴇ ᴍᴀᴋᴇ ɪᴛ ᴄᴏᴍᴘʟɪᴄᴀᴛᴇᴅ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ɴᴏᴛ ᴍᴜᴄʜ ᴏʟᴅᴇʀ ᴛʜᴀɴ ᴛʜᴇ ᴅᴇᴀᴛʜ.</b>",
         "<b>❅ ᴛʜᴇ sᴇᴄʀᴇᴛ ᴏғ ʟɪғᴇ ɪs ʟᴏᴡ ᴇxᴘᴇᴄᴛᴀᴛɪᴏɴs!</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀ ᴛᴇᴀᴄʜᴇʀ..,ᴛʜᴇ ᴍᴏʀᴇ ᴡᴇ ʟɪᴠᴇ, ᴛʜᴇ ᴍᴏʀᴇ ᴡᴇ ʟᴇᴀʀɴ.</b>",
         "<b>❅ ʜᴜᴍᴀɴ ʟɪғᴇ ɪs ɴᴏᴛʜɪɴɢ ʙᴜᴛ ᴀɴ ᴇᴛᴇʀɴᴀʟ ɪʟʟᴜsɪᴏɴ.</b>",
         "<b>❅ ᴛʜᴇ ʜᴀᴘᴘɪᴇʀ ᴛʜᴇ ᴛɪᴍᴇ, ᴛʜᴇ sʜᴏʀᴛᴇʀ ɪᴛ ɪs.</b>",
         "<b>❅ ʟɪғᴇ ɪs ʙᴇᴀᴜᴛɪғᴜʟ ɪғ ʏᴏᴜ  ᴋɴᴏᴡ ᴡʜᴇʀᴇ ᴛᴏ ʟᴏᴏᴋ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀᴡᴇsᴏᴍᴇ ᴡɪᴛʜ ʏᴏᴜ ʙʏ ᴍʏ sɪᴅᴇ.</b>",
         "<b>❅ ʟɪғᴇ – ʟᴏᴠᴇ = ᴢᴇʀᴏ</b>",
         "<b>❅ ʟɪғᴇ ɪs ғᴜʟʟ ᴏғ sᴛʀᴜɢɢʟᴇs.</b>",
         "<b>❅ ɪ ɢᴏᴛ ʟᴇss ʙᴜᴛ ɪ ɢᴏᴛ ʙᴇsᴛ</b>",
         "<b>❅ ʟɪғᴇ ɪs 10% ᴡʜᴀᴛ ʏᴏᴜ ᴍᴀᴋᴇ ɪᴛ, ᴀɴᴅ 90% ʜᴏᴡ ʏᴏᴜ ᴛᴀᴋᴇ ɪᴛ.</b>",
         "<b>❅ ᴛʜᴇʀᴇ ɪs sᴛɪʟʟ sᴏ ᴍᴜᴄʜ ᴛᴏ sᴇᴇ</b>",
         "<b>❅ ʟɪғᴇ ᴅᴏᴇsɴ’ᴛ ɢᴇᴛ ᴇᴀsɪᴇʀ ʏᴏᴜ ɢᴇᴛ sᴛʀᴏɴɢᴇʀ.</b>",
         "<b>❅ ʟɪғᴇ ɪs ᴀʙᴏᴜᴛ ʟᴀᴜɢʜɪɴɢ & ʟɪᴠɪɴɢ.</b>",
         "<b>❅ ᴇᴀᴄʜ ᴘᴇʀsᴏɴ ᴅɪᴇs ᴡʜᴇɴ ʜɪs ᴛɪᴍᴇ ᴄᴏᴍᴇs.</b>",
        ]


ENTAG = [ "<b>※ ɪ ʟᴏᴠᴇ ʏᴏᴜ...ᰔᩚ</b>",
           "<b>※ ғᴏʀɢᴇᴛ ᴍᴇ..ᰔᩚ</b>",
           "<b>※ ɪ ᴅᴏɴ'ᴛ ʟᴏᴠᴇ ʏᴏᴜ...ᰔᩚ</b>",
           "<b>※ ᴍᴀᴋᴇ ɪᴛ ʏᴏᴜʀs ᴘɪʏᴀ, ᴍᴀᴋᴇ ɪᴛ ʏᴏᴜʀs...ᰔᩚ</b>",
           "<b>※ ᴊᴏɪɴ ᴍʏ ɢʀᴏᴜᴘ ᴀʟsᴏ...ᰔᩚ</b>",
           "<b>※ ɪ ᴋᴇᴘᴛ ʏᴏᴜʀ ɴᴀᴍᴇ ɪɴ ᴍʏ ʜᴇᴀʀᴛ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴇʀᴇ ᴀʀᴇ ᴀʟʟ ʏᴏᴜʀ ғʀɪᴇɴᴅs...ᰔᩚ</b>",
           "<b>※ ɪɴ ᴡʜᴏsᴇ ᴍᴇᴍᴏʀʏ ᴀʀᴇ ʏᴏᴜ ʟᴏsᴛ ᴍʏ ʟᴏᴠᴇ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴀᴛs ʏᴏᴜʀ ᴘʀᴏғᴇssɪᴏɴ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴇʀᴇ ᴅɪᴅ ʏᴏᴜ ʟɪᴠᴇ...ᰔᩚ</b>",
           "<b>※ ɢᴏᴏᴅ ᴍᴏʀɴɪɴɢ, ʙᴀʙʏ...ᰔᩚ</b>",
           "<b>※ ɢᴏᴏᴅ ɴɪɢʜᴛ, ɪᴛ's ᴠᴇʀʏ ʟᴀᴛᴇ...ᰔᩚ</b>",
           "<b>※ ɪ ғᴇᴇʟ ᴠᴇʀʏ sᴀᴅ ᴛᴏᴅᴀʏ...ᰔᩚ</b>",
           "<b>※ ᴛᴀʟᴋ ᴛᴏ ᴍᴇ ᴛᴏᴏ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴀᴛ's ғᴏʀ ᴅɪɴɴᴇʀ ᴛᴏᴅᴀʏ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴀᴛ's ɢᴏɪɴɢ ᴏɴ...ᰔᩚ</b>",
           "<b>※ ᴡʜʏ ᴅᴏɴ'ᴛ ʏᴏᴜ ᴍᴇssᴀɢᴇ...ᰔᩚ</b>",
           "<b>※ ɪ ᴀᴍ ɪɴɴᴏᴄᴇɴᴛ...ᰔᩚ</b>",
           "<b>※ ɪᴛ ᴡᴀs ғᴜɴ ʏᴇsᴛᴇʀᴅᴀʏ, ᴡᴀsɴ'ᴛ ɪᴛ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴇʀᴇ ᴡᴇʀᴇ ʏᴏᴜ ʙᴜsʏ ʏᴇsᴛᴇʀᴅᴀʏ...ᰔᩚ</b>",
           "<b>※ ʏᴏᴜ ʀᴇᴍᴀɪɴ sᴏ ᴄᴀʟᴍ ғʀɪᴇɴᴅ...ᰔᩚ</b>",
           "<b>※ ᴅᴏ ʏᴏᴜ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ sɪɴɢ, sɪɴɢ...ᰔᩚ</b>",
           "<b>※ ᴡɪʟʟ ʏᴏᴜ ᴄᴏᴍᴇ ғᴏʀ ᴀ ᴡᴀʟᴋ ᴡɪᴛʜ ᴍᴇ...ᰔᩚ</b>",
           "<b>※ ᴀʟᴡᴀʏs ʙᴇ ʜᴀᴘᴘʏ ғʀɪᴇɴᴅ...ᰔᩚ</b>",
           "<b>※ ᴄᴀɴ ᴡᴇ ʙᴇ ғʀɪᴇɴᴅs...ᰔᩚ</b>",
           "<b>※ ᴀʀᴇ ʏᴏᴜ ᴍᴀʀʀɪᴇᴅ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴇʀᴇ ʜᴀᴠᴇ ʏᴏᴜ ʙᴇᴇɴ ʙᴜsʏ ғᴏʀ sᴏ ᴍᴀɴʏ ᴅᴀʏs...ᰔᩚ</b>",
           "<b>※ ʟɪɴᴋ ɪs ɪɴ ʙɪᴏ, ᴛᴏ ᴊᴏɪɴ ɴᴏᴡ...ᰔᩚ</b>",
           "<b>※ ʜᴀᴅ ғᴜɴ...ᰔᩚ</b>",
           "<b>※ ᴅᴏ ʏᴏᴜ ᴋɴᴏᴡ ᴛʜᴇ ᴏᴡɴᴇʀ ᴏғ ᴛʜɪs ɢʀᴏᴜᴘ...ᰔᩚ</b>",
           "<b>※ ᴅᴏ ʏᴏᴜ ᴇᴠᴇʀ ʀᴇᴍᴇᴍʙᴇʀ ᴍᴇ...ᰔᩚ</b>",
           "<b>※ ʟᴇᴛ's ᴘᴀʀᴛʏ...ᰔᩚ</b>",
           "<b>※ ʜᴏᴡ ᴄᴏᴍᴇ ᴛᴏᴅᴀʏ...ᰔᩚ</b>",
           "<b>※ ʟɪsᴛᴇɴ ᴍᴇ...ᰔᩚ</b>",
           "<b>※ ʜᴏᴡ ᴡᴀs ʏᴏᴜʀ ᴅᴀʏ...ᰔᩚ</b>",
           "<b>※ ᴅɪᴅ ʏᴏᴜ sᴇᴇ...ᰔᩚ</b>",
           "<b>※ ᴀʀᴇ ʏᴏᴜ ᴛʜᴇ ᴀᴅᴍɪɴ ʜᴇʀᴇ...ᰔᩚ</b>",
           "<b>※ ᴀʀᴇ ʏᴏᴜ ɪɴ ʀᴇʟᴀᴛɪᴏɴsʜɪᴘ...ᰔᩚ</b>",
           "<b>※ ᴀɴᴅ ʜᴏᴡ ɪs ᴛʜᴇ ᴘʀɪsᴏɴᴇʀ...ᰔᩚ</b>",
           "<b>※ sᴀᴡ ʏᴏᴜ ʏᴇsᴛᴇʀᴅᴀʏ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴇʀᴇ ᴀʀᴇ ʏᴏᴜ ғʀᴏᴍ...ᰔᩚ</b>",
           "<b>※ ᴀʀᴇ ʏᴏᴜ ᴏɴʟɪɴᴇ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ ʟɪᴋᴇ ᴛᴏ ᴇᴀᴛ...ᰔᩚ</b>",
           "<b>※ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ, ɪ ᴡɪʟʟ ᴘʟᴀʏ ᴍᴜsɪᴄ ᴀɴᴅ ᴛᴀɢ ᴇᴠᴇʀʏᴏɴᴇ...ᰔᩚ</b>",
           "<b>※ ᴡɪʟʟ ʏᴏᴜ ᴘʟᴀʏ ᴛʀᴜᴛʜ ᴀɴᴅ ᴅᴀʀᴇ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴀᴛs ʜᴀᴘᴘᴇɴᴇᴅ ᴛᴏ ʏᴏᴜ...ᰔᩚ</b>",
           "<b>※ ᴅᴏ ʏᴏᴜ ᴡᴀɴɴᴀ ᴇᴀᴛ ᴄʜᴏᴄᴏʟᴀᴛᴇ...ᰔᩚ</b>",
           "<b>※ ʜᴇʟʟᴏ ʙᴀʙʏ...ᰔᩚ</b>",
           "<b>※ ᴅᴏ ᴄʜᴀᴛᴛɪɴɢ ᴡɪᴛʜ ᴍᴇ...ᰔᩚ</b>",
           "<b>※ ᴡʜᴀᴛ ᴅᴏ ʏᴏᴜ sᴀʏ...ᰔᩚ</b>",
           "<b>※ ɢɪᴠᴇ ᴍᴇ ʏᴏᴜʀ ᴡʜᴀᴛsᴀᴘᴘ ɴᴜᴍʙᴇʀ ᴘʟᴇᴀsᴇ...ᰔᩚ</b>"
           ]

BNTAG = ["<b>⚘ আমাকে ভুলে যাও...💥</b>",
         "<b>⚘ আমি তোমাকে ভালোবাসি না...💥</b>",
         "<b>⚘ এটাকে তোমার করো পিয়া, তোমার করো...💥</b>",
         "<b>⚘ আমার গ্রুপেও যোগ দিন...💥</b>",
         "<b>⚘ আমি হৃদয়ে তোমার নাম রেখেছি...💥</b>",
         "<b>⚘ তোমার সব বন্ধু কোথায়...💥</b>",
         "<b>⚘ কার স্মৃতিতে তুমি হারিয়ে গেছো আমার ভালোবাসা...💥</b>",
         "<b>⚘ তোমার পেশা কি...💥</b>",
         "<b>⚘ তুমি কোথায় থাকো...💥</b>",
         "<b>⚘ শুভ সকাল, বাবু...💥</b>",
         "<b>⚘ শুভ রাত্রি, অনেক দেরি হয়ে গেছে...💥</b>",
         "<b>⚘ আমার আজ খুব খারাপ লাগছে...💥</b>",
         "<b>⚘ আমার সাথেও কথা বল...💥</b>",
         "<b>⚘ আজ রাতের খাবারের জন্য কি...💥</b>",
         "<b>⚘ কি হচ্ছে...💥</b>",
         "<b>⚘ তুমি মেসেজ দাও না কেন...💥</b>",
         "<b>⚘ আমি নির্দোষ...💥</b>",
         "<b>⚘ এটা গতকাল মজা ছিল, তাই না...💥</b>",
         "<b>⚘ তুমি গতকাল কোথায় ব্যস্ত ছিলে...💥</b>",
         "<b>⚘ তুমি কি সম্পর্কে আছো...💥</b>",
         "<b>⚘ তুমি খুব শান্ত থাকো বন্ধু...💥</b>",
         "<b>⚘ তুমি কি গাইতে জানো, গাইতে...💥</b>",
         "<b>⚘ তুমি কি আমার সাথে বেড়াতে আসবে...💥</b>",
         "<b>⚘ সবসময় হাসিখুশি থেকো বন্ধু...💥</b>",
         "<b>⚘ আমরা কি বন্ধু হতে পারি...💥</b>",
         "<b>⚘ তুমি কি বিবাহিত...💥</b>",
         "<b>⚘ এত দিন কোথায় ব্যস্ত ছিলে...💥</b>",
         "<b>⚘ লিঙ্ক বায়োতে আছে, এখন যোগ দিতে...💥</b>",
         "<b>⚘ মজা করলাম...💥</b>",
         "<b>⚘ আপনি কি এই গ্রুপের মালিককে চেনেন...💥</b>",
         "<b>⚘ তোমার কি কখনো মনে পড়ে আমায়...💥</b>",
         "<b>⚘ চলো পার্টি করি...💥</b>",
         "<b>⚘ আজ কেমন এলো...💥</b>",
         "<b>⚘ কেমন কাটলো তোমার দিন...💥</b>",
         "<b>⚘ তুমি কি দেখেছো...💥</b>",
         "<b>⚘ আপনি কি এখানকার প্রশাসক...💥</b>",
         "<b>⚘ আমরা বন্ধু হতে পারি...💥</b>",
         "<b>⚘ তুমি কি সম্পর্কে আছো...💥</b>",
         "<b>⚘ আর বন্দী কেমন আছে...💥</b>",
         "<b>⚘ তোমাকে গতকাল দেখেছি...💥</b>",
         "<b>⚘ তুমি কোথা থেকে...💥</b>",
         "<b>⚘ আপনি কি অনলাইনে আছেন...💥</b>",
         "<b>⚘ তুমি কি আমার বন্ধু....💥</b>",
         "<b>⚘ তুমি কি খেতে পছন্দ কর...💥</b>",
         "<b>⚘ আমাকে আপনার গ্রুপে অ্যাড করুন, আমি গান বাজিয়ে সবাইকে ট্যাগ করব....💥</b>",
         "<b>⚘ আজ আমি দুঃখিত...💥</b>",
         "<b>⚘ তুমি কি সত্য খেলবে এবং সাহস করবে...💥</b>",
         "<b>⚘ তোমার মত বন্ধু থাকলে চিন্তার কি আছে...💥</b>",
         "<b>⚘ কি হয়েছে তোমার...💥</b>",
         "<b>⚘ তুমি কি চকলেট খেতে চাও....💥</b>",
         "<b>⚘ হ্যালো বাবু...💥</b>",
         "<b>⚘ আমার সাথে চ্যাট করো...💥</b>",
         "<b>⚘ তুমি কি বলো...💥</b>"
        ]

SHAYRI = [ " ➠ <b>बहुत अच्छा लगता है तुझे सताना और फिर प्यार से तुझे मनाना...। 𑁍 \n\n**⎯꯭‌♡︎°‌⁪Bahut aacha lagta hai tujhe satana Aur fir pyar se tujhe manana...❀</b>",
           " ➠ <b>मेरी जिंदगी मेरी जान हो तुम मेरे सुकून का दुसरा नाम हो तुम...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Meri zindagi Meri jaan ho tum Mere sukoon ka Dusra naam ho tum...❀</b>",
           " ➠ <b>तुम मेरी वो खुशी हो जिसके बिना, मेरी सारी खुशी अधूरी लगती है...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Tum Meri Wo Khushi Ho Jiske Bina, Meri Saari Khushi Adhuri Lagti Ha...❀</b>",
           " ➠ <b>काश वो दिन जल्दी आए,जब तू मेरे साथ सात फेरो में बन्ध जाए...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Kash woh din jldi aaye Jb tu mere sath 7 feron me bndh jaye...❀",
           " ➠ <b>अपना हाथ मेरे दिल पर रख दो और अपना दिल मेरे नाम कर दो...।** 𑁍 \n\n**⎯꯭‌♡︎°‌⁪apna hath mere dil pr rakh do aur apna dil mere naam kar do...❀",
           " ➠ <b>महादेव ना कोई गाड़ी ना कोई बंगला चाहिए सलामत रहे मेरा प्यार बस यही दुआ चाहिए...। 𑁍 \n\⎯꯭‌♡︎°‌⁪Mahadev na koi gadi na koi bangla chahiye salamat rhe mera pyar bas yahi dua chahiye...❀</b>",
           " ➠ <b>फिक्र तो होगी ना तुम्हारी इकलौती मोहब्बत हो तुम मेरी...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Fikr to hogi na tumhari ikloti mohabbat ho tum meri...❀</b>",
           " ➠ <b>सुनो जानू आप सिर्फ किचन संभाल लेना आप को संभालने के लिए मैं हूं ना...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪suno jaanu aap sirf kitchen sambhal lena ap ko sambhlne ke liye me hun naa...❀</b>",
           " ➠ <b>सौ बात की एक बात मुझे चाहिए बस तेरा साथ...।  𑁍 \n\n⎯꯭‌♡︎°‌⁪So bat ki ek bat mujhe chahiye bas tera sath...❀</b>",
           " ➠ <b>बहुत मुश्किलों से पाया हैं तुम्हें, अब खोना नहीं चाहते,कि तुम्हारे थे तुम्हारे हैं अब किसी और के होना नहीं चाहते...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Bahut muskilon se paya hai tumhe Ab khona ni chahte ki tumhare they tumhare hai ab kisi or k hona nhi chahte...❀</b>",
           " ➠ <b>बेबी बातें तो रोज करते है चलो आज रोमांस करते है...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Baby baten to roj karte haichalo aaj romance karte hai...❀</b>",
           " ➠ <b>सुबह शाम तुझे याद करते है हम और क्या बताएं की तुमसे कितना प्यार करते है हम...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪subha sham tujhe yad karte hai hum aur kya batayen ki tumse kitna pyar karte hai hum...❀</b>",
           " ➠ <b>किसी से दिल लग जाने को मोहब्बत नहीं कहते जिसके बिना दिल न लगे उसे मोहब्बत कहते हैं...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Kisi se dil lag jane ko mohabbat nahi kehte jiske nina dil na lage use mohabbat kehte hai...❀</b>",
           " ➠ <b>मेरे दिल के लॉक की चाबी हो तुम क्या बताएं जान मेरे जीने की एकलौती वजह हो तुम...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪mere dil ke lock ki chabi ho tum kya batayen jaan mere jeene ki eklauti wajah ho tum...❀</b>",
           " ➠ <b>हम आपकी हर चीज़ से प्यार कर लेंगे, आपकी हर बात पर ऐतबार कर लेंगे, बस एक बार कह दो कि तुम सिर्फ मेरे हो, हम ज़िन्दगी भर आपका इंतज़ार कर लेंगे...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Hum apki har cheez se pyar kar lenge apki har baat par etvar kar lenge bas ek bar keh do ki tum sirf mere ho hum zindagi bhar apka intzaar kar lenge...❀</b>",
           " ➠ <b>मोहब्बत कभी स्पेशल लोगो से नहीं होती जिससे होती है वही स्पेशल बन जाता है...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Mohabbat kabhi special logo se nahi hoti jisse bhi hoti hai wahi special ban jate hai...❀</b>",
           " ➠ <b>तू मेरी जान है इसमें कोई शक नहीं तेरे अलावा मुझ पर किसी और का हक़ नहीं...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Tu meri jaan hai isme koi shak nahi tere alawa mujhe par kisi aur ka hak nhi...❀</b>",
           " ➠ <b>पहली मोहब्बत मेरी हम जान न सके, प्यार क्या होता है हम पहचान न सके, हमने उन्हें दिल में बसा लिया इस कदर कि, जब चाहा उन्हें दिल से निकाल न सके...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Pehli mohabbat meri hum jaan na sake pyar kya hota hai hum pehchan na sake humne unhe dil me basa liya is kadar ki jab chaha unhe dil se nikal na sake...❀</b>",
           " ➠ <b>खुद नहीं जानती वो कितनी प्यारी हैं , जान है हमारी पर जान से प्यारी हैं, दूरियों के होने से कोई फर्क नहीं पड़ता वो कल भी हमारी थी और आज भी हमारी है...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪khud nahi janti vo kitni pyari hai jan hai hamari par jan se jyda payari hai duriya ke hone se frak nahi pdta vo kal bhe hamari the or aaj bhe hamari hai...❀</b>",
           " ➠ <b>चुपके से आकर इस दिल में उतर जाते हो, सांसों में मेरी खुशबु बनके बिखर जाते हो, कुछ यूँ चला है तेरे इश्क का जादू, सोते-जागते तुम ही तुम नज़र आते हो...। 𑁍  \n\n⎯꯭‌♡︎°‌⁪Chupke Se Aakar Iss Dil Mein Utar Jate Ho, Saanso Mein Meri Khushbu BanKe Bikhar Jate Ho,Kuchh Yun Chala Hai Tere Ishq Ka Jadoo, Sote-Jagte Tum Hi Tum Najar Aate Ho...❀</b>",
           " ➠ <b>प्यार करना सिखा है नफरतो का कोई ठौर नही, बस तु ही तु है इस दिल मे दूसरा कोई और नही...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Pyar karna sikha hai naftaro ka koi thor nahi bas tu hi tu hai is dil me dusra koi aur nahi hai...❀</b>",
           " ➠ <b>रब से आपकी खुशीयां मांगते है, दुआओं में आपकी हंसी मांगते है, सोचते है आपसे क्या मांगे,चलो आपसे उम्र भर की मोहब्बत मांगते है...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Rab se apki khushiyan mangte hai duao me apki hansi mangte hai sochte hai apse kya mange chalo apse umar bhar ki mohabbat mangte hai...❀</b>",
           " ➠ <b>काश मेरे होंठ तेरे होंठों को छू जाए देखूं जहा बस तेरा ही चेहरा नज़र आए हो जाए हमारा रिश्ता कुछ ऐसा होंठों के साथ हमारे दिल भी जुड़ जाए...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪kash mere hoth tere hontho ko chu jayen dekhun jaha bas teri hi chehra nazar aaye ho jayen humara rishta kuch easa hothon ke sath humare dil bhi jud jaye...❀</b>",
           " ➠ <b>आज मुझे ये बताने की इजाज़त दे दो, आज मुझे ये शाम सजाने की इजाज़त दे दो, अपने इश्क़ मे मुझे क़ैद कर लो,आज जान तुम पर लूटाने की इजाज़त दे दो...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Aaj mujhe ye batane ki izazat de do, aaj mujhe ye sham sajane ki izazat de do, apne ishq me mujhe ked kr lo aaj jaan tum par lutane ki izazat de do...❀</b>",
           " ➠ <b>जाने लोग मोहब्बत को क्या क्या नाम देते है, हम तो तेरे नाम को ही मोहब्बत कहते है...। 𑁍\n\n⎯꯭‌♡︎°‌⁪Jane log mohabbat ko kya kya naam dete hai hum to tere naam ko hi mohabbat kehte hai...❀</b>",
           " ➠ <b>देख के हमें वो सिर झुकाते हैं। बुला के महफिल में नजर चुराते हैं। नफरत हैं हमसे तो भी कोई बात नहीं। पर गैरो से मिल के दिल क्यों जलाते हो...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Dekh Ke Hame Wo Sir Jhukate Hai Bula Ke Mahfhil Me Najar Churate Hai Nafrat Hai Hamse To Bhi Koei Bat Nhi Par Gairo Se Mil Ke Dil Kyo Jalate Ho...❀</b>",
           " ➠ <b>तेरे बिना टूट कर बिखर जायेंगे,तुम मिल गए तो गुलशन की तरह खिल जायेंगे, तुम ना मिले तो जीते जी ही मर जायेंगे, तुम्हें जो पा लिया तो मर कर भी जी जायेंगे...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Tere bina tut kar bikhar jeynge tum mil gaye to gulshan ki tarha khil jayenge tum na mile to jite ji hi mar jayenge tumhe jo pa liya to mar kar bhi ji jayenge...❀</b>",
           " ➠ <b>सनम तेरी कसम जेसे मै जरूरी हूँ तेरी ख़ुशी के लिये, तू जरूरी है मेरी जिंदगी के लिये...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Sanam teri kasam jese me zaruri hun teri khushi ke liye tu zaruri hai meri zindagi ke liye...❀</b>",
           " ➠ <b>तुम्हारे गुस्से पर मुझे बड़ा प्यार आया हैं इस बेदर्द दुनिया में कोई तो हैं जिसने मुझे पुरे हक्क से धमकाया हैं...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Tumharfe gusse par mujhe pyar aaya hai is bedard duniya me koi to hai jisne mujhe pure hakk se dhamkaya hai...❀</b>",
           " ➠ <b>पलको से आँखो की हिफाजत होती है धडकन दिल की अमानत होती है ये रिश्ता भी बडा प्यारा होता है कभी चाहत तो कभी शिकायत होती है...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Palkon se Aankho ki hifajat hoti hai dhakad dil ki Aamanat hoti hai, ye rishta bhi bada pyara hota hai, kabhi chahat to kabhi shikayat hoti hai...❀</b>",
           " ➠ <b>मुहब्बत को जब लोग खुदा मानते हैं प्यार करने वाले को क्यों बुरा मानते हैं। जब जमाना ही पत्थर दिल हैं। फिर पत्थर से लोग क्यों दुआ मांगते है...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Muhabbt Ko Hab Log Khuda Mante Hai, Payar Karne Walo Ko Kyu Bura Mante Hai,Jab Jamana Hi Patthr Dil Hai,Fhir Patthr Se Log Kyu Duaa Magte Hai...❀</b>",
           " ➠ <b>हुआ जब इश्क़ का एहसास उन्हें आकर वो पास हमारे सारा दिन रोते रहे हम भी निकले खुदगर्ज़ इतने यारो कि ओढ़ कर कफ़न, आँखें बंद करके सोते रहे...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Hua jab ishq ka ehsaas unhe akar wo pass humare sara din rate rahe, hum bhi nikale khudgarj itne yaro ki ood kar kafan ankhe band krke sote rhe...❀</b>",
           " ➠ <b>दिल के कोने से एक आवाज़ आती हैं। हमें हर पल उनकी याद आती हैं। दिल पुछता हैं बार -बार हमसे के जितना हम याद करते हैं उन्हें क्या उन्हें भी हमारी याद आती हैं...।𑁍 \n\n⎯꯭‌♡︎°‌⁪Dil Ke Kone Se Ek Aawaj Aati Hai, Hame Har Pal Uaski Yad Aati Hai, Dil Puchhta Hai Bar Bar Hamse Ke, Jitna Ham Yad Karte Hai Uanhe, Kya Uanhe Bhi Hamari Yad Aati Hai...❀</b>",
           " ➠ <b>कभी लफ्ज़ भूल जाऊं कभी बात भूल जाऊं, तूझे इस कदर चाहूँ कि अपनी जात भूल जाऊं, कभी उठ के तेरे पास से जो मैं चल दूँ, जाते हुए खुद को तेरे पास भूल जाऊं...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Kabhi Lafz Bhool Jaaun Kabhi Baat Bhool Jaaun, Tujhe Iss Kadar Chahun Ki Apni Jaat Bhool Jaaun, Kabhi Uthh Ke Tere Paas Se Jo Main Chal Dun, Jaate Huye Khud Ko Tere Paas Bhool Jaaun...❀</b>",
           " ➠ <b>आईना देखोगे तो मेरी याद आएगी साथ गुज़री वो मुलाकात याद आएगी पल भर क लिए वक़्त ठहर जाएगा, जब आपको मेरी कोई बात याद आएगी...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Aaina dekhoge to meri yad ayegi sath guzari wo mulakat yad ayegi pal bhar ke waqt thahar jayega jab apko meri koi bat yad ayegi...❀</b>",
           " ➠ <b>प्यार किया तो उनकी मोहब्बत नज़र आई दर्द हुआ तो पलके उनकी भर आई दो दिलों की धड़कन में एक बात नज़र आई दिल तो उनका धड़का पर आवाज़ इस दिल की आई...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Pyar kiya to unki mohabbat nazar aai dard hua to palke unki bhar aai do dilon ki dhadkan me ek baat nazar aai dil to unka dhadka par awaz dil ki aai...❀</b>",
           " ➠ <b>कई चेहरे लेकर लोग यहाँ जिया करते हैं हम तो बस एक ही चेहरे से प्यार करते हैं ना छुपाया करो तुम इस चेहरे को,क्योंकि हम इसे देख के ही जिया करते हैं...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Kai chehre lekar log yahn jiya karte hai hum to bas ek hi chehre se pyar karte hai na chupaya karo tum is chehre ko kyuki hum ise dekh ke hi jiya karte hai...❀</b>",
           " ➠ <b>सबके bf को अपनी gf से बात करके नींद आजाती है और मेरे वाले को मुझसे लड़े बिना नींद नहीं आती...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Sabke bf ko apni gf se baat karke nind aajati hai aur mere wale ko mujhse lade bina nind nhi aati...❀</b>",
           " ➠ <b>सच्चा प्यार कहा किसी के नसीब में होता है. एसा प्यार कहा इस दुनिया में किसी को नसीब होता है...। 𑁍 \n\n⎯꯭‌♡︎°‌⁪Sacha pyar kaha kisi ke nasib me hota hai esa pyar kahan is duniya me kisi ko nasib hota hai...❀</b>" ]


@app.on_message(filters.command(["rtag" ], prefixes=["/", "@", "#", "!"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("⬤ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs. ")

    if message.reply_to_message and message.text:
        return await message.reply("⬤ /rtag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("⬤ /rtag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("⬤ /rtag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("⬤ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["vctag"], prefixes=["/", "@", ".", "#", "!"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("⬤ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs. ")

    if message.reply_to_message and message.text:
        return await message.reply("/vctag  ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ. ")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/vctag  ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ. ...")
    else:
        return await message.reply("/vctag  ᴛʏᴘᴇ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ. ..")
    if chat_id in spam_chats:
        return await message.reply("⬤ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss . . .")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(VC_TAG)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["hitag" ], prefixes=["/", "@", "#", "!"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("⬤ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs. ")

    if message.reply_to_message and message.text:
        return await message.reply("⬤ /hitag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("⬤ /hitag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("⬤ /hitag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("⬤ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(HITAG)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@app.on_message(filters.command(["lifetag" ], prefixes=["/", "@", "#", "!"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("⬤ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs. ")

    if message.reply_to_message and message.text:
        return await message.reply("⬤ /lifetag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("⬤ /lifetag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("⬤ /lifetag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("⬤ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(LYF_TAG)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["entag" ], prefixes=["/", "@", "#", "!"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("⬤ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs. ")

    if message.reply_to_message and message.text:
        return await message.reply("⬤ /entag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("⬤ /entag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("⬤ /entag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("⬤ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(ENTAG)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["bntag" ], prefixes=["/", "@", "#", "!"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("⬤ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs. ")

    if message.reply_to_message and message.text:
        return await message.reply("⬤ /bntag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("⬤ /bntag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("⬤ /bntag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("⬤ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(BNTAG)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["stag" ], prefixes=["/", "@", "#", "!"]))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("⬤ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs. ")

    if message.reply_to_message and message.text:
        return await message.reply("⬤ /stag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("⬤ /stag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏᴛ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("⬤ /stag ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ʙᴏᴛ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("⬤ ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += "<a href='tg://user?id={}'>{}</a>".format(usr.user.id, usr.user.first_name)

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(SHAYRI)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(4)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["sstop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("⬤ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ , ᴏɴʟʏ ᴀᴅᴍɪɴ ᴄᴀɴ ᴅᴏ ᴛʜɪs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("♥︎ sʜᴀʏᴀʀɪ ᴛᴀɢ sᴛᴏᴘᴇᴅ.")


@app.on_message(filters.command(["enstop", "bnstop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("⬤ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("♥︎ ᴇɴɢʟɪsʜ/ʙᴀɴɢʟᴀ ᴛᴀɢ sᴛᴏᴘᴘᴇᴅ.")


@app.on_message(filters.command(["histop", "lstop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("⬤ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("♥︎ ʜɪɴᴅɪ/ʟɪғᴇ ᴛᴀɢ sᴛᴏᴘᴘᴇᴅ.")



@app.on_message(filters.command(["rstop", "vstop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("⬤ ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ ʙᴀʙʏ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("⬤ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ʙᴀʙʏ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴅᴏ ᴛʜɪs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("♥︎ ʀᴀɴᴅᴏᴍ ᴍᴇssᴀɢᴇ ᴛᴀɢ sᴛᴏᴘᴘᴇᴅ.")