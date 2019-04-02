from __future__ import print_function
import telebot
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

bot_token = '894065303:AAEnIsQHguU7bGVuPiF0DuYtRYyppa9ZjtQ'
bot = telebot.TeleBot(token=bot_token)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']


@bot.message_handler(commands=['hola'])
def send_welcome(message):
    bot.reply_to(message, 'Bienvenido a BuloBlocker! ')

@bot.message_handler(commands=['ayuda'])
def send_help(message):
    bot.reply_to(message, ""
                          "Siempre estar bien saludar con /hola \n"
                          "En caso de querer recordar los comandos vuelve a usar /ayuda \n"
                          "Infórmate sobre esta iniciativa con /descripcion"
                          "\n\nPara que rastreemos tu bulos solo tienes que envierme el enlace a la notica. "
                          "Una vez tengamos el enlace te comentaremos los siguientes pasos.")


@bot.message_handler(func=lambda msg: msg.text is not None and '://' in msg.text)
def at_answer(message):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('BuloBlocker-451d2c1b42d2.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('Respuestas Formulario Muckrakers').sheet1
    df = pd.DataFrame(wks.get_all_records())
    print(df)
    # Comprobamos si hemos el fact check de esta noticia
    if any(message.text in string for string in df['ENLACE A LA PLATAFORMA DONDE ESTÁ PUBLICADA LA NOTICIA']):
        bot.reply_to(message, "Gracias por tu colaboración este ya lo tenemos")
        print("Gracias por tu colaboración este ya lo tenemos")
    else:
        parts = message.text.split("//")
        partes = parts[1].split(".")
        if partes[0] == "www":
            fuente = partes[1]
        else:
            fuente = partes[0]

        bot.send_message(message.chat.id ,'WOW! Todavía no habíamos visto esta noticia.')
        bot.reply_to(message, "Vale, este podría ser un bulo. En nuestras fuentes tenemos X solicitudes para revisar posibles bulos de esta fuente"
                              "además de Y bulos verificados de la fuente" + fuente)
        bot.send_message(message.chat.id, "Te importa que te hagamos un par de preguntas sobre este bulo?")
        # En caso de no tener hecho el fact-Check vamos a ver de los fact check cuantas veces aparece esta fuente para
        #dar un mensje estimado de cuando de fiable pìuede ser esta notica
        print(message.text)


        print(fuente)
        print("WOW! Todavía no habíamos visto esta noticia.")
        print("Si no te importa te vamos a preguntar un par de preguntillas para que quede registrada y podamos analizarla")



while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(15)





#GOOGLE

#Client ID
#660192323788-krda88jji7s23vfje4aqvetaj9bjlut2.apps.googleusercontent.com
#Client secret
#3wGPhbGzwaAJ3YrhhN7MEOn7