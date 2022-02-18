import telebot
import time
import json
from telebot import types
from config import token

bot = telebot.TeleBot(token)



@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Показать видеокарты")
    markup.add(item1)
    bot.send_message(message.chat.id, f'Привет', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def show_data(message):
    with open("all_cards.json", "r", encoding="utf-8") as file:
        cards_data = json.load(file)

    filt = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("<20к")
    item2 = types.KeyboardButton("20к-40к")
    item3 = types.KeyboardButton("40к-60к")
    item4 = types.KeyboardButton(">60к")
    filt.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, f'Выбери ценовой диапазон', reply_markup=filt)

    if message.text == "<20к":
        for index, item in enumerate(cards_data):
            if item['Цена'].isalpha():
                continue
            else:
                try:
                    if int(item['Цена'].rstrip("₽").replace(" ", "")) < 20000:
                        try:
                            card = f"{item['Название']} \n" \
                                   f"{item['Цена']}\n\n" \
                                   f"{item['Адрес']} \n\n" \
                                   f"{item['Описание']}\n" \
                                   f"{item['Ссылка']}\n" \
                                   f"{item['Дата']}"
                            bot.send_message(message.chat.id, card)
                        except:
                            time.sleep(1)
                except ValueError:
                    continue

    elif message.text == "20к-40к":
        for index, item in enumerate(cards_data):
            if item['Цена'].isalpha():
                continue
            else:
                try:
                    if int(item['Цена'].rstrip("₽").replace(" ", "")) >= 20000 and int(item['Цена'].rstrip("₽").replace(" ", "")) < 40000:
                        try:
                            card = f"{item['Название']} \n" \
                                   f"{item['Цена']}\n\n" \
                                   f"{item['Адрес']} \n\n" \
                                   f"{item['Описание']}\n" \
                                   f"{item['Ссылка']}\n" \
                                   f"{item['Дата']}"
                            bot.send_message(message.chat.id, card)
                        except:
                            time.sleep(1)
                except ValueError:
                    continue

    elif message.text == "40к-60к":
        for index, item in enumerate(cards_data):
            if item['Цена'].isalpha():
                continue
            else:
                try:
                    if int(item['Цена'].rstrip("₽").replace(" ", "")) >= 40000 and int(item['Цена'].rstrip("₽").replace(" ", "")) < 60000:
                        try:
                            card = f"{item['Название']} \n" \
                                   f"{item['Цена']}\n\n" \
                                   f"{item['Адрес']} \n\n" \
                                   f"{item['Описание']}\n" \
                                   f"{item['Ссылка']}\n" \
                                   f"{item['Дата']}"
                            bot.send_message(message.chat.id, card)
                        except:
                            time.sleep(1)
                except ValueError:
                    continue
    elif message.text == ">60к":
        for index, item in enumerate(cards_data):
            if item['Цена'].isalpha():
                continue
            else:
                try:
                    if int(item['Цена'].rstrip("₽").replace(" ", "")) >= 60000:
                        try:
                            card = f"{item['Название']} \n" \
                                   f"{item['Цена']}\n\n" \
                                   f"{item['Адрес']} \n\n" \
                                   f"{item['Описание']}\n" \
                                   f"{item['Ссылка']}\n" \
                                   f"{item['Дата']}"
                            bot.send_message(message.chat.id, card)
                        except:
                            time.sleep(1)
                except ValueError:
                    continue


bot.polling()
