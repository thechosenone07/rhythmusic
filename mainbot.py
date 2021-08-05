import os
import aiohttp
import asyncio
import json
import sys
import time
from youtubesearchpython import SearchVideos
from pyrogram import filters, Client
from sample_config import Config
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, UsernameNotOccupied

Jebot = Client(
   "Song Downloader",
   api_id=Config.APP_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.TG_BOT_TOKEN,
)


 #For private messages        
 #Ignore commands
 #No bots also allowed

@Jebot.on_message(filters.private & ~filters.bot & ~filters.command("help") & ~filters.command("start") & ~filters.command("s"))
async def song(client, message):
    cap = "@fastsongdownloderslbzbot"
    url = message.text
    rkp = await message.reply("<b>🔍 Searching your song ...</b>")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("<b>Failed to find your song 😥.... Try anyother one !</b>")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("<b>Downloading ⏳ Your Song, Please Wait </b>")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("The download content was too short ⏱.")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await rkp.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await rkp.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("<b>Uploading ⏳ Your Song, Please Wait </b>") 
        lol = "./thumb.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["Uploader..."]),
                 thumb=lol,
                 caption=cap) 
        await rkp.delete()
        os.system("rm -rf *.mp3")
        os.system("rm -rf *.webp")
  
    
@Jebot.on_message(filters.command("song") & ~filters.edited & filters.group)
async def song(client, message):
    cap = "@fastsongdownloderslbzbot"
    url = message.text.split(None, 1)[1]
    rkp = await message.reply("<b>🔍 Searching your song ...</b>")
    if not url:
        await rkp.edit("**<b>What's the song you want?, Please use this format **\nformat /song <song name> </b>")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("<b>Failed to find your song 😥.... Try anyother one !</b>")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("<b>Downloading ⏳ Your Song, Please Wait </b>")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("The download content was too short ⏱.")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await rkp.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await rkp.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("<b>Uploading ⏳ Your Song, Please Wait </b>") 
        lol = "./thumb.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["Uploader..."]),
                 thumb=lol,
                 caption=cap) 
        await rkp.delete()
        os.system("rm -rf *.mp3")
        os.system("rm -rf *.webp")
 
    
JOIN_ASAP = "<b>You Need To Join My updates channel  For Executing This Command 👮‍♀️...</b>"

FSUBB = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton(text="🔔 Join My Channel", url=f"https://t.me/sl_bot_zone")
        ]]
    )
@Jebot.on_message(command(["start", f"start"]) & other_filters)
@errors
async def start(_, message: Message):
   if message.chat.type == 'private': 
    try:
        await message._client.get_chat_member(int("-1001325914694"), message.from_user.id)
    except UserNotParticipant:
        await message.reply_text(
        text=JOIN_ASAP, disable_web_page_preview=True, reply_markup=FSUBB
    )
        return
       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>👋 Hey There, I'm a Song Downloader Bot. A bot by 👨‍💻 @slbotzone.

                                                           """,   
                            reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Add Me To Your Group ➕", url=f"https://t.me/fastsongdownloderslbzbot?startgroup=true"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🛠  Help Menu 🛠", callback_data="help""
                    )
                ],
                [
                    InlineKeyboardButton(
                        "⚒ Create your one 📦", url="https://www.youtube.com/channel/UCvYfJcTr8RY72dIapzMqFQA"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🔔  My Update Channel", url=f"https://t.me/sl_bot_zone"
                    ),
                    InlineKeyboardButton(
                        "💬 Support Group ", url="https://t.me/slbotzone"
                    )
                ]
            ]
        )
    )      
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )
   else:

       await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>✅ Song Downloader Is Online.\n\n</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "Help", callback_data="help")
                                        
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html",
            reply_to_message_id=message.message_id
        )

@Jebot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="""<b>Send a song name to download song

@slbotzone</b>""",
            reply_to_message_id=message.message_id
        )
    else:
        await Jebot.send_message(
               chat_id=message.chat.id,
               text="<b>Song Downloader Help.\n\nSyntax: /song lelena </b>",
            reply_to_message_id=message.message_id
        )     
        

@Jebot.on_callback_query()
async def button(Jebot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(Jebot, update.message)

print(
    """
Bot Started!

Join @slbotzone
"""
)

Jebot.run()
