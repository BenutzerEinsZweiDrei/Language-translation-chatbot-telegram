from hugchat import hugchat
import telebot
from deep_translator import GoogleTranslator

chatbot = hugchat.ChatBot(cookie_path="cookies.json")  # or cookies=[...]


# Create a new conversation
id = chatbot.new_conversation()
chatbot.change_conversation(id)

# Get conversation list
conversation_list = chatbot.get_conversation_list()


BOT_TOKEN='your telegram token'

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, im a language translation bot. Just keep talking to me.")
    
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    translate_message = GoogleTranslator(source='auto', target='fr').translate(message.text) # just ask in french so he answers in french
    response = chatbot.chat(translate_message)
    response_str = str(response) # try to fix doctype html crash
    bot.reply_to(message, '🇫🇷 '+response_str)
    translated = GoogleTranslator(source='auto', target='en').translate(response_str) 
    bot.reply_to(message, '🇺🇸 '+translated)
    
    
# bot.polling(none_stop=True)
bot.infinity_polling()
