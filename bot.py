import os, time
from hugchat_api import HuggingChat
import telebot
from deep_translator import GoogleTranslator

### config

debug = True # change to True or False

flag1 = "🇫🇷"
flag2 = "🇺🇸"

learnLanguage = "French" # bot will be prompted to teach that language. Put here in english.
langCode1 = "fr" # the first message shows up in
langCode2 = "en" # the second message shows up in

BOT_TOKEN = "<your telegram bot token>"

EMAIL = "<your huggingface email>"
PASSWD = "<your huggingface password>"
COOKIE_STORE_PATH = "./" 


### Teacher Prompt

promptTeacher = "I want you to act as a spoken "+learnLanguage+" teacher and improver for the complete conversation. I will speak to you in any language and you will reply to me in "+learnLanguage+" to practice my spoken "+learnLanguage+". I want you to keep your reply neat, limiting the reply to 100 words. I want you to strictly correct my grammar mistakes, typos, and factual errors if i use the language "+learnLanguage+". I want you to ask me a question in your reply always. Now let's start practicing, you could ask me a question first. Remember, I want you to strictly correct my grammar mistakes, typos, and factual errors and please remember to keep your answer short and in easy language. Remember all of this for the complete conversation."

### load hugchat
if debug : 
    print("DEBUG: before loading hugchat")
    
HUG = HuggingChat(max_thread=1) # create ThreadPool

# initialize sign in funciton
sign = HUG.getSign(EMAIL, PASSWD) #login

cookies = sign.loadCookiesFromDir(cookie_dir_path=COOKIE_STORE_PATH)

chatbot = HUG.getBot(email=EMAIL, cookies=cookies) # create bot

Started = False

if debug : 
    print("DEBUG: hugchat loaded")


### startup telebot
if debug : 
    print("DEBUG: before loading telebot")
bot = telebot.TeleBot(BOT_TOKEN)
if debug : 
    print("DEBUG: telebot loaded")



# handle start and hello command
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    
    if debug : 
        print("DEBUG: before starting conversation")
        
    # Create a new conversation
    global conversation_id 
    conversation_id = chatbot.createConversation()
    
    # tell bot to be a teacher
    pro = chatbot.chat(
    text=promptTeacher,
    conversation_id=conversation_id,
    web_search=True,
    max_tries=2,
    # callback=(bot.updateTitle, (conversation_id,))
    )
    while not pro.isDone():
        time.sleep(0.1)
        if debug :
            print("x")
            
    if debug : 
        print("DEBUG: conversation startet")
        
    bot.reply_to(message, "Howdy, im a language translation bot. Just keep talking to me.")
    Started = True
    
    if debug : 
        print("DEBUG: processed start command")
    
# handle all messages
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    
    if not Started :
    	bot.reply_to(message, "Please use /start command first")
    	return
    	
    if debug : 
        print("DEBUG: Start of echo_all")
        
    # get response from bot
    prompt =  message.text
    
    response = chatbot.chat(
    text=prompt,
    conversation_id=conversation_id,
    web_search=True,
    max_tries=2,
    )
    while not response.isDone():
        time.sleep(0.1)
        if debug :
            print("x")
            
    if debug :
    	    print("DEBUG: received hugchat response")
    	    
    # reply first message
    bot.reply_to(message, flag1 + ' ' +response.getFinalText())
    if debug : 
        print("DEBUG: bot replied first message")
        
    # into second language and reply
    translated = GoogleTranslator(source='auto', target= langCode2 ).translate(response.getFinalText()) 
    bot.reply_to(message,  flag2 + ' ' +translated)
    
    if debug : 
         print("DEBUG: bot replied second message. End of message function")

if debug : 
    print("DEBUG: before infinity polling. Start messaging.")
# bot.polling(none_stop=True) # check which one works better
bot.infinity_polling()

if debug : 
    print("DEBUG: end of file")
