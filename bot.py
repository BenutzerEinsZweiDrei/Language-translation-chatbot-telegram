import os, time
from hugchat_api import HuggingChat
from hugchat_api.core import ListBots
import telebot
from deep_translator import GoogleTranslator

### config

debug = True # change to True or False

flag1 = "🇫🇷"
flag2 = "🇺🇸"

learnLanguage = "French" # bot will be prompted to teach that language. Put here in english.
langCode1 = "fr" # the first message shows up in
langCode2 = "en" # the second message shows up in

transPrompt = True # if you translate your prompt hugchat will remember better to answer in that language

remindShort = True # always remind him to keep answers short

BOT_TOKEN = "your telegram bot token"

EMAIL = "your huggingface email"
PASSWD = "your huggingface password"
COOKIE_STORE_PATH = "./"


### Teacher Prompt
# will be translated to your langCode1

promptTeacher = "I want you to act as a spoken "+learnLanguage+" teacher and improver for the complete conversation. I will speak to you in any language and you will reply to me in "+learnLanguage+" to practice my spoken "+learnLanguage+". I want you to keep your reply neat, limiting the reply to 100 words. I want you to strictly correct my grammar mistakes, typos, and factual errors if i use the language "+learnLanguage+". I want you to ask me a question in your reply always. Now let's start practicing, you could ask me a question first. Remember, I want you to strictly correct my grammar mistakes, typos, and factual errors and please remember to keep your answer short and in easy language. Remember all of this for the complete conversation."

### load hugchat
if debug : 
    print("DEBUG: before loading hugchat")
    
HUG = HuggingChat(max_thread=1) # create ThreadPool

# initialize sign in funciton
sign = HUG.getSign(EMAIL, PASSWD) #login

cookies = sign.loadCookiesFromDir(cookie_dir_path=COOKIE_STORE_PATH)

chatbot = HUG.getBot(email=EMAIL, cookies=cookies,model=ListBots.META_70B_HF) # create bot

Started = False

if debug : 
    print("DEBUG: hugchat loaded")


### startup telebot
if debug : 
    print("DEBUG: before loading telebot")
bot = telebot.TeleBot(BOT_TOKEN)
if debug : 
    print("DEBUG: telebot loaded")

### implement function

def send_2lang(message, send_m, transl):
       # reply first message
       if transl:
       	 send_m = GoogleTranslator(source='auto', target= langCode1 ).translate(send_m) 
       	 
       bot.reply_to(message, flag1 + ' ' + send_m)
       
       # into second language and reply
       translated = GoogleTranslator(source='auto', target= langCode2 ).translate(send_m) 
       bot.reply_to(message,  flag2 + ' ' +translated)

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
    )
            
    # give him some time to process that
    x = 0
    while not x > 300 :
        if not pro.isDone():
            time.sleep(0.1)
            x= x + 1
            if x == 100 :
            	send_2lang(message, "Sorry. Response is taking time..", True) 
        else :
        	x = 301
        if debug :
            print(x)
            
    if debug : 
        print("DEBUG: conversation startet")
    
    send_2lang(message, "Howdy, im a language translation bot. Just keep talking to me.", True)
    
    global Started
    Started = True
    
    if debug : 
        print("DEBUG: processed start command")
    
# handle all messages
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    
    
    if not Started :
    	send_2lang(message, "Please use /start command first", True)
    	return
    	
    if debug : 
        print("DEBUG: Start of echo_all")
        
    # prepare prompt
    if remindShort :
    	sho = GoogleTranslator(source='auto', target= langCode1 ).translate("Keep your answer to the following prompt short. ")
    	prompt = sho + message.text
    else :
    	prompt = message.text
    	
    if transPrompt :
    	prompt = GoogleTranslator(source='auto', target= langCode1 ).translate(prompt)
    
    # get response from bot
    response = chatbot.chat(
    text=prompt,
    conversation_id=conversation_id,
    web_search=False,
    max_tries=2,
    )
    
    # give him some time
    x = 0
    while not x > 300 :
        if not response.isDone():
            time.sleep(0.1)
            x= x + 1
            if x == 200 :
            	send_2lang(message, "Sorry. Response is taking time..", True) 
        else :
        	x = 301
        if debug :
            print(x)
     
    # choose response
    if response.isDone() :
    	chosen_response = response.getFinalText()
    else :
        chosen_response ="(debug)" + ' '.join(response.getText())
        
    if debug :
    	    print("DEBUG: received hugchat response")
    
    # send answers
    send_2lang(message, chosen_response, False)
    
    if debug : 
         print("DEBUG: bot replied. End of message function")

if debug : 
    print("DEBUG: before infinity polling. Start messaging.")
# bot.polling(none_stop=True) # check which one works better
bot.infinity_polling()

if debug : 
    print("DEBUG: end of file")
