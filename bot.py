from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import mysql.connector
from gemini_api import responder_gemini
from dotenv import load_dotenv
import os

load_dotenv()

telegram_token = os.getenv("TELEGRAM_TOKEN")

# Conexión a la base de datos
try:
    db = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
    db_connected = True
    print("Conectado a la base de datos MySQL")
except Exception as e:
    db_connected = False
    print(f"No se pudo conectar a la base de datos: {e}")
    print("El bot funcionará sin buscar en la base de datos")

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
        "ciudad": ""
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
        user["estado"] = "esperando_pregunta_comida"
        await update.message.reply_text("¡Gracias! ¿Qué te gustaría comer ahora?")

    elif user["estado"] == "esperando_pregunta_comida":
        preferencias = (
            f"{user['name']} es alérgico/a a {', '.join(user['alergias']) or 'nada'}, "
            f"no le gusta {', '.join(user['no_gusta']) or 'nada'}."
        )
        ubicacion = f"{user['direccion']}, {user['barrio']}, {user['ciudad']}"

        respuesta = f"{preferencias} Está en {ubicacion} y quiere comer {texto}."

        # Buscar lugares en MySQL por ciudad solo si está conectado
        if db_connected:
            try:
                cursor = db.cursor(dictionary=True)
                query = "SELECT name, address FROM restaurants WHERE city = %s LIMIT 1"
                cursor.execute(query, (user["ciudad"],))
                lugar = cursor.fetchone()
                cursor.close()

                if lugar:
                    respuesta += f"\n\n📍 Un lugar recomendado cerca es: {lugar['name']}, ubicado en {lugar['address']}."
                else:
                    respuesta += f"\n\n📍 No encontramos restaurantes en la base de datos para {user['ciudad']}."
            except Exception as e:
                respuesta += f"\n\n⚠️ No pude buscar en la base de datos: {e}"
        else:
            respuesta += f"\n\n📍 No tengo acceso a la base de datos de lugares en este momento."

        # Sugerencia de comida con Gemini
        restricciones = f"Alergias: {', '.join(user['alergias']) or 'ninguna'}. No le gusta: {', '.join(user['no_gusta']) or 'nada'}."
        
        # Crear un restaurante ficticio para Gemini
        restaurante_ficticio = {
            "nombre": "Restaurante Local",
            "ciudad": user["ciudad"],
            "platos": "Variedad de platos locales, pastas, carnes, pescados, ensaladas y postres"
        }
        
        respuesta += "\n\n🍽️ " + responder_gemini(texto, restricciones, restaurante_ficticio)

        await update.message.reply_text(respuesta)

if __name__ == "__main__":
    app = ApplicationBuilder().token(telegram_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
