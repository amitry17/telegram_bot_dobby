import telebot
from config import keys, TOKEN
from Extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start'])

def help(message: telebot.types.Message):
    text = f'Добро пожалвать {message.chat.username}!\nЭтот бот поможет вам быстро перевести любую сумму из одной валюты в другую.\
\n Помощь для работы с ботом:\n/help'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['help'])

def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду в следующем формате:\n<имя валюты> <в какую величину перевести> <количество переводимой валюты> \nУвидить список всех доступных валют:\n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands = ['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n • '.join((text,key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types = ['text',])
def convert(message: telebot.types.Message):
  try:
    values = message.text.lower().split(' ')
    if len(values) != 3:
      raise ConvertionException('Неверный запрос \n /help')
    
    quote, base, amount = values
    total_base = CurrencyConverter.convert(quote, base, amount)
  except ConvertionException as e:
      bot.reply_to(message, f'Ошибка\n{e}' )
  except Exception as e:
      bot.reply_to(message, f'Не удалось обработать команду \n{e}' )
  text = f'Цена {amount} {quote} в {base} - {round(float(total_base) * float(amount), 2)}{keys[base]}'
  bot.send_message(message.chat.id, text)

bot.polling()