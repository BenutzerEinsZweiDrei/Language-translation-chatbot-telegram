from hugchat import hugchat
import telebot

chatbot = hugchat.ChatBot(cookie_path="cookies.json")  # or cookies=[...]


# Create a new conversation
id = chatbot.new_conversation()
chatbot.change_conversation(id)

# Get conversation list
conversation_list = chatbot.get_conversation_list()


BOT_TOKEN='your telegram bot token'

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, im a language translation bot. Just keep talking to me.")
    
@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    response = chatbot.chat('Answer to the following nessage in French.Keep the answer short."'+message.text+'"')
    bot.reply_to(message, '🇫🇷 '+response)
    oldres = response
    newres = chatbot.chat('Translate the following message into english."'+oldres+'"')
    bot.reply_to(message, '🇺🇸 '+newres)

# bot.polling(none_stop=True)
bot.infinity_polling()
