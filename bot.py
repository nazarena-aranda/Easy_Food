from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import mysql.connector
from gemini_api import responder_gemini
from dotenv import load_dotenv
import os

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")

# Conexión a la base de datos
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

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
    user = usuarios.get(chat_id)

    if not user:
        await update.message.reply_text("Por favor escribí /start para comenzar.")
        return

    if user["estado"] == "esperando_name":
        user["name"] = texto
        user["estado"] = "esperando_alergia"
        await update.message.reply_text(f"¡Encantado, {user['name']}! ¿Tenés alguna alergia?, decime cuál (una a la vez)")

    elif user["estado"] == "esperando_alergia":
        if texto in ["no", "ninguna", "nada"]:
            user["estado"] = "esperando_no_gusta"
            await update.message.reply_text("¿Hay algo que no te guste?, decime qué (uno a la vez)")
        else:
            user["alergias"].append(texto)
            await update.message.reply_text("¿Alguna otra alergia? (escribí 'no' si ya está)")

    elif user["estado"] == "esperando_no_gusta":
        if texto in ["no", "ninguno", "nada"]:
            user["estado"] = "esperando_direccion"
            await update.message.reply_text("¿Cuál es tu dirección exacta?")
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
        user["estado"] = "esperando_pregunta_comida"
        await update.message.reply_text("¡Gracias! ¿Qué te gustaría comer ahora?")

    elif user["estado"] == "esperando_pregunta_comida":
        preferencias = (
            f"{user['name']} es alérgico/a a {', '.join(user['alergias']) or 'nada'}, "
            f"no le gusta {', '.join(user['no_gusta']) or 'nada'}."
        )
        ubicacion = f"{user['direccion']}, {user['barrio']}, {user['ciudad']}, {user['pais']}"

        # Buscar lugares en MySQL por ciudad
        cursor = db.cursor(dictionary=True)
        query = "SELECT nombre, direccion FROM lugares WHERE ciudad = %s LIMIT 1"
        cursor.execute(query, (user["ciudad"],))
        lugar = cursor.fetchone()
        cursor.close()

        if lugar:
            respuesta = (
                f"{preferencias} Está en {ubicacion} y tiene hambre. "
                f"Un lugar recomendado cerca es: {lugar['nombre']}, ubicado en {lugar['direccion']}."
            )
        else:
            respuesta = (
                f"{preferencias} Está en {ubicacion}, pero no encontramos lugares en la base de datos para esa ciudad."
            )

        # Sugerencia de comida con Gemini
        respuesta += "\n\n" + responder_gemini(f"{preferencias} Vive en {ubicacion} y quiere comer {texto}. Recomendale una comida.")

        await update.message.reply_text(respuesta)

if __name__ == "__main__":
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
