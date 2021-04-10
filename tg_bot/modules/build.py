import subprocess
import html
import json
import random
import time
import pyowm
import yaml
from pyowm import exceptions
from datetime import datetime
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from tg_bot import dispatcher, LOGGER
from tg_bot.__main__ import STATS, USER_INFO
from tg_bot.modules.disable import DisableAbleCommandHandler
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.helper_funcs.filters import CustomFilters

from requests import get

# DO NOT DELETE THIS, PLEASE.
# Made by @androiabledroid based on @peaktogoo 's Android module on GitHub and Telegram.

LOGGER.info("Get Build from server")

@run_async
def getBuild(bot: Bot, update: Update):
	reply_text = ""
	message = update.effective_message
	device = message.text[len('/getBuild '):]
	# Fetch Device Image from lineage_wiki
	link = (f'https://download.project-oneos.org/?dir={device}')
	if len(device) == 0:
		message.reply_text("<b>Plz provide valid Arguments</b>", parse_mode=ParseMode.HTML)
	else:
		fetch = get(link)
		btn = {"inline_keyboard": [[{ "text": "Download", "url": link }]]}
		if fetch.status_code == 200:
			img_link = 'https://raw.githubusercontent.com/LineageOS/lineage_wiki/master/images/devices/' + yaml.load(get(f'https://raw.githubusercontent.com/LineageOS/lineage_wiki/master/_data/devices/{device}.yml').text, Loader=yaml.FullLoader)['image']
			image = get(img_link, stream = True)
			reply_text = (f"<b>Device</b>: {device}")
			if image.status_code == 200:
				message.reply_photo(photo=img_link, caption=reply_text, reply_markup=btn, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
			else:
				message.reply_text(reply_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
		elif fetch.status_code == 404 or fetch.status_code == 500:
			reply_text = "Device not found."
			message.reply_text(reply_text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)



__help__ = """
 - /getBuild <device>: Gets the build for device if exists.
"""

__mod_name__ = "Build"

BUILD_HANDLER = DisableAbleCommandHandler("getBuild", getBuild, admin_ok=True)

dispatcher.add_handler(BUILD_HANDLER)
