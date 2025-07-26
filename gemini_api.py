import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def responder_gemini(preferencia, restricciones, restaurante):
    prompt = f"""
    Un usuario quiere comer {preferencia}. Encontramos el restaurante "{restaurante['nombre']}" en {restaurante['ciudad']}.
    Este es su menú: {restaurante['platos']}.
    El usuario tiene estas restricciones: {restricciones}.
    ¿Qué plato le recomendás y por qué?
    """

    response = genai.GenerativeModel("gemini-pro").generate_content(prompt)
    return response.text
