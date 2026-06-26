import os
from dotenv import load_dotenv
from openai import OpenAI
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List

# Crear el cliente de OpenAI usando la clave del entorno
client = OpenAI(api_key="")

class ActionResponderPreguntaEmbarazo(Action):
    def name(self) -> str:
        return "action_responder_pregunta_embarazo"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        pregunta = tracker.latest_message.get("text")
        if not pregunta:
            dispatcher.utter_message(text="No entendí tu pregunta. ¿Podrías repetirla?")
            return []

        try:
            # Directamente procesamos la pregunta sin necesidad de validación extra
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[ 
                    {"role": "system", "content": (
                        "Eres un asistente médico experto en embarazo. "
                        "Responde de forma clara, empática y precisa. "
                        "solo responde preguntas de embarazo"
                        "Agrega siempre un comentario bonito para la futura madre.")},
                    {"role": "user", "content": pregunta}
                ],
                max_tokens=150,
                temperature=0.7
            )

            respuesta = response.choices[0].message.content.strip()
            dispatcher.utter_message(text=respuesta)

        except Exception as e:
            dispatcher.utter_message(text="Ocurrió un error procesando tu pregunta.")
            print("❌ ERROR:", e)

        return []

class ActionOpenAIFallback(Action):
    def name(self) -> str:
        return "action_openai_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:
        
        # Obtén el mensaje del usuario
        mensaje_usuario = tracker.latest_message.get("text", "").lower()
        
        # Lista de palabras clave relacionadas con embarazo
        palabras_clave_embarazo = [
            "embarazo", "gestación", "maternidad", "bebé", "trimestre", "parto", 
            "náuseas", "ecografía", "consultas", "embarazada", "feto", "sintomas", "labor de parto"
        ]
        
        # Verifica si la pregunta contiene palabras clave relacionadas con embarazo
        if any(palabra in mensaje_usuario for palabra in palabras_clave_embarazo):
            try:
                # Enviar la pregunta a OpenAI para procesarla
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[ 
                        {"role": "system", "content": (
                            "Eres un asistente médico especializado en embarazo. "
                            "Responde de forma clara, empática y profesional. "
                            "Incluye siempre una fuente confiable al final como la OMS, CDC o MedlinePlus. "
                            "Solo debes hablar sobre el embarazo, si preguntan sobre otro tema diles que no estás hecho para eso.")},
                        {"role": "user", "content": mensaje_usuario}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )

                # Recupera la respuesta de OpenAI
                respuesta = response.choices[0].message.content.strip()
                dispatcher.utter_message(text=respuesta)

            except Exception as e:
                dispatcher.utter_message(text="Lo siento, no pude generar una respuesta en este momento.")
                print("❌ ERROR:", e)
        else:
            # Si la pregunta no está relacionada con el embarazo
            dispatcher.utter_message(text="Lo siento, no puedo responder preguntas sobre otros temas. Solo puedo ayudar con información relacionada al embarazo.")
        
        return []
