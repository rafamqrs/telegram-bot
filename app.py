# -*- coding: utf-8 -*-
#!/usr/bin/python
import os
import telebot
from telebot import types
import configparser
import requests
import logging
from url_normalize import url_normalize

bot_token_savecoins = os.environ['BOT_KEY_SAVECOINS']
bot = telebot.TeleBot(bot_token_savecoins)

def init_log():
    logging.basicConfig(filename='app.log', level=logging.INFO)
    logging.info('Iniciando a config de log')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Olá, bem vindo ao BOT que irá lhe ajudar na consulta de preços do site savecoins.")
    bot.reply_to(message, "Digite o nome do jogo desejado:")

def message_error_handler(message):
    bot.reply_to(message.chat.id, "Não foi possível realizar a consulta. Estamos com problema e em breve o serviço será normalizado")

@bot.message_handler(func=lambda m: True)
def get_data_from_savecoins(message):
    try:
        if message:
            url_normalized = url_normalize(config_properties['savecoins']['url'] + '?currency=BRL&locale=en&filter[platform]=nintendo&filter[title]=' + message.text)
            logging.info(url_normalized)
            request = requests.get(url_normalized)
            json_response = request.json()
            markup = types.ReplyKeyboardMarkup()
            if len(json_response['data']) > 1:
                games_list = json_response['data']
                for game in games_list:
                    markup.row(types.KeyboardButton(game['title']))
                bot.send_message(message.chat.id, "Escolha um jogo:", reply_markup=markup)
            elif json_response['data']: 
                get_link_to_buy(message, json_response['data'][0]['slug'])
    except Exception as err:
        logging.error(f'Ocorreu um erro no metodo get_data_from_savecoins: {err}')
        message_error_handler('Ocorreu um erro ao buscar informações do jogo')

def get_link_to_buy(message, slug):
    try:
        logging.debug('get data' + config_properties['savecoins']['url'] + '/' + slug + '?currency=BRL&locale=en')
        request = requests.get(config_properties['savecoins']['url'] + '/' + slug + '?currency=BRL&locale=en')
        json_response = request.json()
        bot.send_message(message.chat.id, 'Nome: {title} Preço:{price} LinkDigital:{link}'.format(title=json_response['data']['title'], price=json_response['data']['price_info']['currentPrice'], link=json_response['data']['linkToPurchaseDigital']))
    except Exception as err:
        logging.error(f'Não foi possivel concluir o metodo get_link_to_by: {err}')
        message_error_handler(message)


    
def read_config_file():
    try:
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config
    except Exception as err:
        logging.error(f'Ocorreu um erro ao ler o arquivo ini.: {err}')


init_log()
config_properties = read_config_file()

bot.polling()
