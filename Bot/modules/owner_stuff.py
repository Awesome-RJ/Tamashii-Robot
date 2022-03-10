from Bot.__main__ import STATS
from telegram import ParseMode
from telegram.ext import CommandHandler, Filters
from telegram.ext.dispatcher import run_async
from Bot import (
    dispatcher,
    updater,
    OWNER_ID
)
from telegram import __version__
from psutil import cpu_percent, virtual_memory, disk_usage, boot_time
import datetime
import platform
from platform import python_version

@run_async
def stats(update, context):
    uptime = datetime.datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    status = "*-------< System >-------*\n"
    status += f"*System uptime:* {str(uptime)}" + "\n"

    uname = platform.uname()
    status += f"*System:* {str(uname.system)}" + "\n"
    status += f"*Node name:* {str(uname.node)}" + "\n"
    status += f"*Release:* {str(uname.release)}" + "\n"
    status += f"*Version:* {str(uname.version)}" + "\n"
    status += f"*Machine:* {str(uname.machine)}" + "\n"
    status += f"*Processor:* {str(uname.processor)}" + "\n\n"

    mem = virtual_memory()
    cpu = cpu_percent()
    disk = disk_usage("/")
    status += f"*CPU usage:* {str(cpu)}" + " %\n"
    status += f"*Ram usage:* {str(mem[2])}" + " %\n"
    status += f"*Storage used:* {str(disk[3])}" + " %\n\n"
    status += f"*Python version:* {python_version()}" + "\n"
    status += f"*Library version:* {str(__version__)}" + "\n"
    update.effective_message.reply_text(

        "*Chizuru, the lewd one near you*\n" + 
        "built by [Dank-del](t.me/dank_as_fuck)\n" +
        "Built with ❤️ using python-telegram-bot\n\n" + status +
        "*Current Stats*:\n"
        + "\n".join([mod.__stats__() for mod in STATS]) + 
        "\n\n© *2020-2021 Dank-del*",
    parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    
    
STATS_HANDLER = CommandHandler("stats", stats, filters=Filters.user(OWNER_ID))
dispatcher.add_handler(STATS_HANDLER)