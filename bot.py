from hugchat import hugchat
import telebot
from deep_translator import GoogleTranslator

# config

debug = True # change to True or False

flag1 = "🇫🇷"
flag2 = "🇺🇸"

learnLanguage = "French" # bot will be prompted to teach that language. Put here in english.
langCode1 = "fr" # the first message shows up in
langCode2 = "en" # the second message shows up in

BOT_TOKEN = "<your telegram bot token>"

# Teacher Prompt
# will be translated to your langCode1

promptTeacher = "I want you to act as a spoken "+learnLanguage+" teacher and improver for the prompt at the end of the message. I will speak to you in "+learnLanguage+" and you will reply to me in "+learnLanguage+" to practice my spoken "+learnLanguage+". I want you to keep your reply neat, limiting the reply to 100 words. I want you to strictly correct my grammar mistakes, typos, and factual errors. I want you to ask me a question in your reply. Now let's start practicing, you could ask me a question first. Remember, I want you to strictly correct my grammar mistakes, typos, and factual errors and please remember to keep your answer short and in easy language. Remember all of this but write your answer only to the following prompt '"

# load hugchat
if debug : 
    print("DEBUG: before loading hugchat")
chatbot = hugchat.ChatBot(cookie_path="cookies.json")  # or cookies=[...]
if debug : 
    print("DEBUG: hugchat loaded")

if debug : 
    print("DEBUG: before starting conversation")
# Create a new conversation
chatbot.switch_llm(1) # use llama
id = chatbot.new_conversation()
chatbot.change_conversation(id)

# Get conversation list
conversation_list = chatbot.get_conversation_list()
if debug : 
    print("DEBUG: conversation startet")

# startup telebot
if debug : 
    print("DEBUG: before loading telebot")
bot = telebot.TeleBot(BOT_TOKEN)
if debug : 
    print("DEBUG: telebot loaded")

# handle start and hello command
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, im a language translation bot. Just keep talking to me.")
    if debug : 
        print("DEBUG: processed start command")
    
# handle all messages
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    if debug : 
        print("DEBUG: Start of echo_all")
    # tell bot to act as a language teacher before every message.
    prompt = promptTeacher + message.text + "'"
    translated_prompt = GoogleTranslator(source='auto', target= langCode1 ).translate(prompt) 
    if debug : 
            print("DEBUG: prompt translated")
    response = chatbot.chat(translated_prompt)
    if debug :
    	    print("DEBUG: received hugchat response")
    bot.reply_to(message, flag1 + ' ' +response)
    if debug : 
        print("DEBUG: bot replied first message")
    # into second language
    translated = GoogleTranslator(source='auto', target= langCode2 ).translate(response) 
    bot.reply_to(message,  flag2 + ' ' +translated)
    if debug : 
         print("DEBUG: bot replied second message. End of message function")

if debug : 
    print("DEBUG: before infinity polling. Start messaging.")
# bot.polling(none_stop=True) # check which one works better
bot.infinity_polling()

if debug : 
    print("DEBUG: end of file")
