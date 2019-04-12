from __future__ import print_function
import telebot
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from telebot import types
import ast
import time
import telebot
bot_token = '894065303:AAEnIsQHguU7bGVuPiF0DuYtRYyppa9ZjtQ'
bot = telebot.TeleBot(token=bot_token)
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
opciones = {"/bulo": "Enviar Bulo", "/info": "Información", "/ayuda": "Ayuda!", "/fastbulo": "¿Mas rápido...?"}
fuentes = {"1": "WhatsApp", "/2": "Telegram", "/3": "Familiar/conocido", "/4": "Otras redes sociales", "/5": "Lista de difusión"}
crossIcon = u"\u274C"

print("Servidor iniciado!")


@bot.message_handler(commands=['hola', 'start'])
def send_welcome(message):
    bot.reply_to(message, '¡Hola! \nTe damos la bienvenida al Buloblocker de Greenpeace España. Utilizando este bot, ya estás luchando contra la desinformación. \n¡Felicidades! ')

    bot.send_message(chat_id=message.chat.id,
                     text="¿Qué quieres hacer?",
                     reply_markup=makeKeyboard(opciones),
                     parse_mode='HTML')


@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "La desinformación, es decir, la información falsa se expande, de manera intencionada, por nuestros móviles, redes sociales o conversaciones. Estos mensajes 'hackean' nuestros cerebros y nuestras democracias, porque generan premisas falsas, contaminan el debate y polarizan nuestra sociedad. El histórico negacionismo sobre el cambio climático, la acusación de intereses ocultos en los grupos ecologistas y otras tantas historias más forman parte de esta estrategia de desinformación que pretende mentir sobre el impacto del actual modelo económico sobre el planeta. "
                          "\nQueremos parar esa 'desinformación verde'. Desde Greenpeace os pedimos que nos ayudéis a buscar los bulos que circulan y que compartáis los desmentidos. \nMás información: https://es.greenpeace.org/es/noticias/buloblocker/")


@bot.message_handler(commands=['ayuda'])
def send_help(message):
    bot.reply_to(message, ""
                          "Por si estas un poco perdido, te recordamos como hablar a BuloBlocker!\n"
                          "Saluda con un /hola \n"
                          "En caso de querer recordar los comandos vuelve a usar /ayuda \n"
                          "Infórmate sobre esta iniciativa con /info\n"
                          "Mandanos un Bulo siguiendo los pasos de /bulo\n"
                          "Echale un ojo a la guía sobre como enviar bulos de forma rápida /fasturl ")


@bot.message_handler(commands=['fastbulo'])
def send_fast_bulo(message):
    bot.reply_to(message, "Si tienes pensado hablarme a menudo, esto te interesa:\n"
                          "Puedes saltarte muchos pasos a la hora de enviar URL, y que me puedas mandar enlaces mucho mas rápido. \n"
                          "De hecho, puedes saltarte el saludo (/hola), incluso decirme que vas a mandar una url (/url) y simplemente mandármela. "
                          "Pruébalo, ¡ya verás que rápido! \n")


@bot.message_handler(commands=['bulo'])
def start_bulo(message):
    bot.reply_to(message, "Adelante!, envía por el chat el enlace" )


@bot.message_handler(commands=['test'])
def handle_command_adminwindow(message):
    bot.send_message(chat_id=message.chat.id,
                     text="Here are the values of stringList",
                     reply_markup=makeKeyboard(opciones),
                     parse_mode='HTML')


def makeKeyboard(stringList):

    markup = types.InlineKeyboardMarkup()

    for key, value in stringList.items():
        markup.add(types.InlineKeyboardButton(text=value, callback_data="['value', '" + value + "', '" + key + "']"),
        #types.InlineKeyboardButton(text=crossIcon, callback_data="['key', '" + key + "']"))

    return markup


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    opciones =  { "/bulo": "Enviar Bulo", "/info": "Información", "/ayuda": "Ayuda!",
                   "/fastbulo": "¿Mas rápido...?"}
    if call.data.startswith("['value'"):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        #bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)
        #if keyFromCallBack.startswith("/hola"):
        #    send_welcome(call.message)
        if keyFromCallBack.startswith("/bulo"):
            start_bulo(call.message)
        if keyFromCallBack.startswith("/info"):
            send_info(call.message)
        if keyFromCallBack.startswith("/ayuda"):
            send_help(call.message)
        if keyFromCallBack.startswith("/fastbulo"):
            send_fast_bulo(call.message)

   # if call.data.startswith("['key'"):
   #     keyFromCallBack = ast.literal_eval(call.data)[1]
   #     del opciones[keyFromCallBack]
   #     opciones = opciones
   #     bot.edit_message_text(chat_id=call.message.chat.id,
   #                           text="respuesta",
   #                           message_id=call.message.message_id,
   #                           reply_markup=makeKeyboard(opciones),
   #                           parse_mode='HTML')

    fuentes = {"1": "WhatsApp", "/2": "Telegram", "/3": "Familiar/conocido", "/4": "Otras redes sociales",
               "/5": "Lista de difusión"}
    if call.data.startswith("['value'") and ast.literal_eval(call.data)[1] in [ "WhatsApp", "Telegram", "Familiar/conocido", "Otras redes sociales", "Lista de difusión"]:
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        # bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)
        credentials = ServiceAccountCredentials.from_json_keyfile_name('BuloBlocker-451d2c1b42d2.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Respuestas Formulario Muckrakers').sheet1
        df = pd.DataFrame(wks.get_all_records())
        print(df)
        lista_var_temp = [call.message.chat.first_name, "usuarioTelegram", "Sin Info", call.message.text,
                          "Sin especificar", "Sin especificar",
                          valueFromCallBack, "Sin especificar", "Sin especificar", "Sin especificar",
                          time.strftime("%d/%m/%y") + " " + time.strftime("%H:%M:%S")]
        wks.append_row(lista_var_temp)

        bot.send_message(call.message.chat.id, "Gracias por enviarnos esta desinformación o contenido dudoso. \n"
                                               "Nuestro personal de campañas, lo estudiará para realizar la verificación. "
                                               "Puedes consultar nuestra biblioteca de desmentidos o Greenchecking. "
                                               "\n\nDifúndela y ayúdanos a parar la desinformación")
    if call.data.startswith("['key'"):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del fuentes[keyFromCallBack]
        fuentes = fuentes
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="respuesta",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(fuentes),
                              parse_mode='HTML')

    if opciones == 0:
        opciones = {    "/bulo": "Enviar Bulo", "/info": "Información", "/ayuda": "Ayuda!", "/fastbulo": "¿Mas rápido...?"}




@bot.callback_query_handler(func=lambda call: True)
def handle_query_fuente(call):
    fuentes = {"1": "WhatsApp", "/2": "Telegram", "/3": "Familiar/conocido", "/4": "Otras redes sociales", "/5": "Lista de difusión"}
    if call.data.startswith("['value'"):
        valueFromCallBack = ast.literal_eval(call.data)[1]
        keyFromCallBack = ast.literal_eval(call.data)[2]
        #bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="You Clicked " + valueFromCallBack + " and key is " + keyFromCallBack)
        credentials = ServiceAccountCredentials.from_json_keyfile_name('BuloBlocker-451d2c1b42d2.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open('Respuestas Formulario Muckrakers').sheet1
        df = pd.DataFrame(wks.get_all_records())
        print(df)
        lista_var_temp = [call.message.chat.first_name, "usuarioTelegram", "Sin Info", call.message.text, "Sin especificar", "Sin especificar",
                          valueFromCallBack, "Sin especificar", "Sin especificar", "Sin especificar",
                          time.strftime("%d/%m/%y") + " " + time.strftime("%H:%M:%S")]
        wks.append_row(lista_var_temp)

        bot.send_message(call.message.chat.id, "Gracias por enviarnos esta desinformación o contenido dudoso. \n"
                                          "Nuestro personal de campañas, lo estudiará para realizar la verificación. "
                                          "Puedes consultar nuestra biblioteca de desmentidos o Greenchecking. "
                                          "\n\nDifúndela y ayúdanos a parar la desinformación")
    if call.data.startswith("['key'"):
        keyFromCallBack = ast.literal_eval(call.data)[1]
        del fuentes[keyFromCallBack]
        fuentes = fuentes
        bot.edit_message_text(chat_id=call.message.chat.id,
                              text="respuesta",
                              message_id=call.message.message_id,
                              reply_markup=makeKeyboard(fuentes),
                              parse_mode='HTML')

    if fuentes == 0:
        fuentes = {"/hola": "Saluda!", "/bulo": "Enviar Bulo", "/info": "Información", "/ayuda": "Ayuda!", "/fastbulo": "¿Mas rápido...?"}


@bot.message_handler(func=lambda msg: msg.text is not None and '://' in msg.text)
def send_bulo(message):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('BuloBlocker-451d2c1b42d2.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('Respuestas Formulario Muckrakers').sheet1
    df = pd.DataFrame(wks.get_all_records())
    nombr_temp = message.chat.id
    lista_var_temp = [nombr_temp, "usuarioTelegram", "Sin Info", message.text, "Sin especificar", "Sin especificar", "Sin especificar", "Sin especificar", "Sin especificar", "Sin especificar",time.strftime("%d/%m/%y") + " " + time.strftime("%H:%M:%S")]

    bot.send_message(message.chat.id, "¿Quieres ayudarnos?")

    bot.send_message(chat_id=message.chat.id, text="¿Cómo recibiste esta información?",
                     reply_markup=makeKeyboard(fuentes), parse_mode='HTML')





    # FALTA AÑADIR LO DE SI SE QUIERE AÑADIR INFORMACIÓN EXTRA! IMPORTANTE!

    # Comprobamos si hemos el fact check de esta noticia
    #if any(message.text in string for string in df['ENLACE A LA PLATAFORMA DONDE ESTÁ PUBLICADA LA NOTICIA']):
    #    bot.reply_to(message, "Gracias por tu colaboración este ya lo tenemos")
    #    print("Gracias por tu colaboración este ya lo tenemos")
    #else:
    #    parts = message.text.split("//")
    #    partes = parts[1].split(".")
    #    if partes[0] == "www":
    #        fuente = partes[1]
    #    else:
    #        fuente = partes[0]

    #wks.append_row(lista_var_temp)


while True:
    try:
        bot.polling()
    except Exception:
        time.sleep(999999999999999999999999999999999999999999999999999999999999999999999999999)


