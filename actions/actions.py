import os
from dotenv import load_dotenv
from openai import OpenAI
from rasa_sdk import Action
from rasa_sdk.executor import CollectingDispatcher
import requests

# Cargar variables del archivo .env
load_dotenv()

# Crear el cliente de OpenAI usando la clave del entorno
client = OpenAI(api_key="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")

class ActionResponderPreguntaEmbarazo(Action):
    def name(self) -> str:
        return "action_responder_pregunta_embarazo"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        # Obtener el texto más reciente del usuario
        pregunta = tracker.latest_message.get("text")

        if not pregunta:
            dispatcher.utter_message(text="No entendí tu pregunta. ¿Podrías repetirla?")
            return []

        try:
            # Llamar al modelo GPT-3.5-Turbo con la pregunta del usuario
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente médico experto en temas de embarazo. Responde de forma clara, empática y precisa."},
                    {"role": "user", "content": pregunta}
                ],
                max_tokens=100,
                temperature=0.7
            )

            # Extraer la respuesta generada por el modelo
            respuesta = response.choices[0].message.content.strip()

            # Enviar la respuesta al usuario
            dispatcher.utter_message(text=respuesta)

        except Exception as e:
            dispatcher.utter_message(text="Lo siento, ocurrió un error al procesar tu pregunta. Intenta nuevamente.")
            print("❌ ERROR en llamada a OpenAI:", e)

        return []

class ActionRecomendarDieta(Action):
    def name(self) -> str:
        return "action_recomendar_dieta"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        # Obtén la semana de embarazo desde el slot
        semana_embarazo = tracker.get_slot("semana_embarazo") or "1"

        # Llama a la API de Nutrition API de API Ninjas
        api_url = f"https://api.api-ninjas.com/v1/nutrition?query=fruta&semana={semana_embarazo}"
        headers = {"X-Api-Key": "TU_API_KEY"}
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data:
                # Extrae la información nutricional
                alimento = data[0]
                mensaje = (
                    f"Para la semana {semana_embarazo} de embarazo, te recomiendo consumir {alimento['name']}."
                    f" Contiene {alimento['calories']} calorías, {alimento['protein_g']}g de proteína,"
                    f" {alimento['carbohydrates_total_g']}g de carbohidratos y {alimento['fat_total_g']}g de grasa."
                )
            else:
                mensaje = "No se encontraron recomendaciones para esta semana."
        else:
            mensaje = "Hubo un error al obtener las recomendaciones de dieta."

        dispatcher.utter_message(text=mensaje)
        return []