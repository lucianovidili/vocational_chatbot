import os
import requests
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import ollama

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")


load_dotenv()

# Estado temporal del test
test_questions = [
    "¿Preferís trabajar con personas o con datos?",
    "¿Te atraen más las ciencias exactas o las humanidades?",
    "¿Preferís tareas creativas o rutinarias?",
    "¿Te gusta resolver problemas prácticos o teóricos?",
    "¿Preferís trabajo en oficina o al aire libre?",
    "¿Te atrae más trabajar en equipo o individualmente?"
]

def home(request):
    return render(request, "chatbot/chatbot.html")

def ask_gpt(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "").strip().lower()

        # Inicia test
        if user_message == "empezar test":
            request.session['test_step'] = 0
            request.session['answers'] = []
            return JsonResponse({"reply": f"Vamos a comenzar el test. {test_questions[0]}"})

        # Si está en el test
        if 'test_step' in request.session:
            step = request.session['test_step']
            answers = request.session['answers']
            answers.append(user_message)
            step += 1
            if step < len(test_questions):
                request.session['test_step'] = step
                request.session['answers'] = answers
                return JsonResponse({"reply": test_questions[step]})
            else:
                del request.session['test_step']
                del request.session['answers']
                return JsonResponse({"reply": "¡Test finalizado! Según tus respuestas, te recomendaría explorar carreras en tecnología, salud o educación."})

        # Chat normal con GPT
        messages = [
            {"role": "system", "content": "Sos un orientador vocacional amable y breve."},
            {"role": "user", "content": user_message}
        ]
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            bot_reply = response["choices"][0]["message"]["content"]
            return JsonResponse({"reply": bot_reply})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Método no permitido"})

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            payload = {
                "model": "mistral-small-latest",
                "messages": [
                    {
                        "role": "system",
                        "content": 
                            "Eres un orientador vocacional amable y experimentado."
                            "Por favor responde siempre en español."
                            "Cuando haya enumeracion de cosas como 1., 2., 3., etc, enumerar asi: 1), 2), 3), etc. y deja una linea en blanco entre cada cosa."
                            "Debajo de tu respuesta completa a su prompt, escribe '_______', sin dejar lineas en blanco arriba."
                            "Limitate a contestar lo que se te pregunta."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }

            headers = {
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json"
            }

            # Aquí se conecta con Mistral en internet
            r = requests.post("https://api.mistral.ai/v1/chat/completions", headers=headers, json=payload)
            r.raise_for_status()
            response_json = r.json()

            bot_reply = response_json["choices"][0]["message"]["content"]

            return JsonResponse({"reply": bot_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

