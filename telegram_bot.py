import requests
import telebot

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

bot = telebot.TeleBot(TOKEN)

def send_message(message):
    bot.send_message(CHAT_ID, message)

# Example: Send profit booking alert
send_message("✅ Book Profit in Canara Robeco Bluechip - Profit: +31.5%")
