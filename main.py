from selenium.webdriver.common.by import By
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

import youtube_dl

#following secrets have been removed from here
TOKEN = ''
allowed_users = [] 

      
def welcome(update, context):
    update.message.reply_text("Hey!Send the link of tweet to get the video")

def message_action(update, context):
      id = update.message.chat_id
      if id in allowed_users:
        link = update.message.text
        if (('twitter' or 't.co') in link):
                chrome_options = Options()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                driver = webdriver.Chrome(options=chrome_options)
                site = "https://twittervideodownloader.com"
                # s = Service("D:\SeleniumDriverChrome\chromedriver.exe")
                # driver = webdriver.Chrome(service=s)
                driver.get(site)
                field = driver.find_element(By.NAME, 'tweet')
                field.send_keys(link)
                submit = driver.find_element(By.CLASS_NAME, 'input-group-button')
                submit.click()
                d = driver.find_element(By.LINK_TEXT, "Download Video")
                link = d.get_attribute('href')
                update.message.reply_video(video=link)
        elif (('youtube' or 'youtu.be') in link):
                with youtube_dl.YoutubeDL(dict(forceurl=True)) as ydl:
                   r = ydl.extract_info(link, download=False)
                   link = r['formats'][-1]['url']
                try:
                        update.message.reply_video(link)
                except:
                        update.message.reply_text(link)

            
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
start = CommandHandler('start', welcome)
dispatcher.add_handler(start)
user_message = MessageHandler(Filters.text, message_action)
dispatcher.add_handler(user_message)
updater.start_polling()
updater.idle()
