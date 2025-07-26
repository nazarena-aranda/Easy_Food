
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from gemini_api import responder_gemini
from dotenv import load_dotenv
import os

load_dotenv()

usuarios = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    usuarios[chat_id] = {
        "estado": "esperando_name",
        "name": "",
        "alergias": [],
        "no_gusta": [],
        "direccion": "",
        "barrio": "",
        "ciudad": "",
        "pais": ""
    }
    await update.message.reply_text("Hola! Soy Easy Food Bot, ¿Cómo te llamás?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    texto = update.message.text.lower()

    if chat_id not in usuarios:
        await update.message.reply_text("Por favor escribí /start para comenzar!!")
        return

    user = usuarios[chat_id]

    if user["estado"] == "esperando_name":
        user["name"] = texto
        user["estado"] = "esperando_alergia"
        await update.message.reply_text(f"¡Encantado, {user['name']}! ¿Tenés alguna alergia?, dime cuál (una a la vez)")

    elif user["estado"] == "esperando_alergia":
        if texto in ["no", "ninguna", "nada"]:
            user["estado"] = "esperando_no_gusta"
            await update.message.reply_text("Perfecto. ¿Hay algo que no te guste comer?")
        else:
            user["alergias"].append(texto)
            await update.message.reply_text("¿Alguna otra alergia? (escribí 'no' si ya está)")

    elif user["estado"] == "esperando_no_gusta":
        if texto in ["no", "ninguno", "nada"]:
            user["estado"] = "esperando_direccion"
            await update.message.reply_text("Entendido. ¿Cuál es tu dirección exacta?")
        else:
            user["no_gusta"].append(texto)
            await update.message.reply_text("¿Algo más que no te guste? (escribí 'no' si ya está)")

    elif user["estado"] == "esperando_direccion":
        user["direccion"] = texto
        user["estado"] = "esperando_barrio"
        await update.message.reply_text("¿En qué barrio estás?")

    elif user["estado"] == "esperando_barrio":
        user["barrio"] = texto
        user["estado"] = "esperando_ciudad"
        await update.message.reply_text("¿En qué ciudad vivís?")

    elif user["estado"] == "esperando_ciudad":
        user["ciudad"] = texto
        user["estado"] = "esperando_pais"
        await update.message.reply_text("¿En qué país estás?")

    elif user["estado"] == "esperando_pais":
        user["pais"] = texto

        payload = {
            "telegramId": chat_id,
            "name": user["name"],
            "allergies": user["alergias"],
            "dislikes": user["no_gusta"],
            "address": user["direccion"],
            "barrio": user["barrio"],
            "ciudad": user["ciudad"],
            "pais": user["pais"]
        }

        try:
            response = requests.post("http://localhost:8080/api/usuarios", json=payload)
            if response.status_code in [200, 201]:
                await update.message.reply_text("¡Listo! Tus datos fueron guardados correctamente. Voy a buscar restaurantes cerca de tu zona")
                user["estado"] = "esperando_pregunta_comida"
            else:
                await update.message.reply_text("Hubo un error al guardar tus datos.")
        except Exception as e:
            await update.message.reply_text("No pude conectarme con el servidor.")
            print(f"Error al conectar: {e}")

    elif user["estado"] == "esperando_pregunta_comida":
        name = user["name"]
        allergies = user["alergias"]
        no_gusta = user["no_gusta"]
        resumen = (
            f"{name} es alérgico/a a {', '.join(allergies) or 'nada'}, "
            f"no le gusta {', '.join(no_gusta) or 'nada'}, "
            f"vive en {user['direccion']}, barrio {user['barrio']}, ciudad {user['ciudad']}, país {user['pais']}, "
            f"y quiere saber: {texto}. Recomendale una comida."
        )

        respuesta = responder_gemini(resumen)
        await update.message.reply_text(respuesta)

if __name__ == '__main__':
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
