
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY") 

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-pro")

def responder_gemini(mensaje):
    try:
        respuesta = model.generate_content(mensaje)
        return respuesta.text
    except Exception as e:
        return f"Ocurrió un error con Gemini: {str(e)}"
