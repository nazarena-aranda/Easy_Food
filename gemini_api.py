import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

modelo = genai.GenerativeModel("gemini-flash")
modelo = genai.GenerativeModel("models/gemini-1.5-flash")

def responder_gemini(preferencia, restricciones, restaurante):
    platos = restaurante.get('platos', '')
    if isinstance(platos, list):
        platos = ', '.join(platos)
    if not platos:
        return "Este restaurante no tiene platos cargados aún. Probá con otro"

    prompt = f"""
    Un usuario quiere comer {preferencia}. Encontramos el restaurante "{restaurante['nombre']}" en {restaurante['ciudad']}.
    Este es su menú: {platos}.
    El usuario tiene estas restricciones: {restricciones}.
    ¿Qué plato le recomendás? Respondé de forma breve, simpática y clara.
    """

    try:
        print("Prompt enviado a Gemini:\n", prompt)  
        respuesta = modelo.generate_content(prompt)
        return respuesta.text.strip()
    except Exception as e:
        print("ERROR EN GEMINI:", e) 
        return "¡Uy! Hubo un problema al generar la respuesta. Probá de nuevo más tarde."