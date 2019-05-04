from telegram import Update, Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, User, CallbackQuery
from telegram.ext import run_async

from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot import dispatcher

from requests import get

import urllib.request, json

@run_async
def device(bot: Bot, update: Update):
  # Check this every time because we update info very often
  with urllib.request.urlopen("https://bootleggersrom-devices.github.io/api/devices.json") as url:
    data = json.loads(url.read().decode())

  message = update.effective_message
  text = message.text[len('/device '):].strip().lower()
  try:
    deviceinfo = data[text]
  except: 
    if text != "":
      reply_error_text = "Sorry, but %s isn't on our official devices list." % text
    else:
      reply_error_text = "Please, specify your device by using /device `codename` (example `/device mido`)"

    message.reply_text(reply_error_text.replace("_","\_"),parse_mode="Markdown")
    raise

  clean_dls_url = deviceinfo["downloadfolder"].replace("https:","http:")
  clean_lb_url = deviceinfo["download"].replace("https:","http:")
  clean_thread_url = deviceinfo["xdathread"].replace("https:","http:")
  reply_text = f'*Bootleggers for {deviceinfo["fullname"]} ({text})*\n*Maintainer:* {deviceinfo["maintainer"]}\n*Latest build:* `{deviceinfo["filename"]}`'
  
  if "xda-developers" in clean_thread_url:
    device_links = [[InlineKeyboardButton("XDA Thread", url=clean_thread_url),
                  InlineKeyboardButton("Get Latest", url=clean_lb_url),
                  InlineKeyboardButton("All Builds", url=clean_dls_url)]]
  else:
    device_links = [[InlineKeyboardButton("Get Latest", url=clean_lb_url),
                  InlineKeyboardButton("All Builds", url=clean_dls_url)]]
  message.reply_text(reply_text.replace("_","\_"),parse_mode="Markdown",
                                     reply_markup=InlineKeyboardMarkup(device_links))

@run_async
def devicelist(bot: Bot, update: Update):
  # Check this every time because we update info very often
  with urllib.request.urlopen("https://bootleggersrom-devices.github.io/api/devices.json") as url:
    data = json.loads(url.read().decode())
  message = update.effective_message
  infoDevList = "<b>List of our currently supported devices:</b>"
  
  for key in data:
    infoDevList += "\n- " + key
  print(infoDevList)
  #if infoDevList = "":
  #  infoDevListmsg = "Sorry, but there's no official devices yet."
  
  message.reply_text(infoDevList,parse_mode="HTML")

__help__ = """
 - /device:{word} Search on our device list if you device is there. example: /device surnia.\n
 - /devicelist: See the amount of devices available 
"""

__mod_name__ = "Bootleg Device List"
  
devlist_handle = DisableAbleCommandHandler("device", device)
devlistinfo_handle = DisableAbleCommandHandler("devicelist", devicelist)

dispatcher.add_handler(devlist_handle)
dispatcher.add_handler(devlistinfo_handle)