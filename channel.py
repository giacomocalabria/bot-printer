import logging, datetime, get_info

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import subprocess

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# IMPOSTAZIONI LIVELLO STAMPANTE
nomi = [['Toner','Nero','Ciano','Magenta','Giallo'],['Vassoio',1,2,3]]
levelGood = 25 # livello sopra il quale lo stato è buono
levelBad  = 0  # livello sotto il quale (incluso) lo stato è cattivo

# Define the function to send the status of the printer to the user and send a warning if the level is below a certain threshold.
async def UpdateStatus(info, update: Update, context: ContextTypes) -> None:
    status = []
    for i in [0,1]:
        a=[]
        for j,x in enumerate(info[i]):
            a.append('✅' if x>levelGood else '⚠' if x>levelBad else '❌')
            if x<levelGood and x>levelBad:
                await update.message.reply_text('⚠ ATTENZIONE !!! ⚠\n%s %s in esaurimento!' % (nomi[i][0],nomi[i][j+1]))
            if x<=levelBad:
                await update.message.reply_text('❌ ATTENZIONE !!! ❌\n%s %s esaurito!' % (nomi[i][0],nomi[i][j+1]))
        status.append(a)
    
    text = '''
``` ==== Inchiostro =====
Nero:         %3u%% %s
Ciano:        %3u%% %s
Magenta:      %3u%% %s
Giallo:       %3u%% %s
======= Carta =======
Vassoio 1:    %3u%% %s
Vassoio 2:    %3u%% %s
Vassoio 3:    %3u%% %s
=====================
Ora aggiornamento:
%s
\
```''' % (info[0][0],status[0][0],info[0][1],status[0][1],info[0][2],status[0][2],info[0][3],status[0][3],
			 info[1][0],status[1][0],info[1][1],status[1][1],info[1][2],status[1][2],
			 datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

    await update.message.reply_text(text, parse_mode="Markdown")

# Define the GET command to get the status of the printer.
async def get(update: Update, context: ContextTypes) -> None:
    await update.message.reply_text("Getting status...")
    try:
        info = get_info.get_info()
        if info is not None:
            await UpdateStatus(info, update, context)
    except Exception as e:
        print(e)

# Define the BACKUP command (not used)
'''async def backup(update: Update, context: ContextTypes) -> None:
    await update.message.reply_text("Backing up data...")
    try:
        subprocess.run("C:\\Users\\papercutbackup2.bat")
        await update.message.reply_text("Backup finished!")
    except Exception as e:
        print(e)'''

# Define the START command
async def start(update: Update, context: ContextTypes) -> None:
    # Send a message when the command /start is issued
    await update.message.reply_text("Hi! Use /get to get the status of the printer.")

# START THE BOT
def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("PUT HERE SECRET TOKEN").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    application.add_handler(CommandHandler("get", get))

    #application.add_handler(CommandHandler("backup", backup))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()