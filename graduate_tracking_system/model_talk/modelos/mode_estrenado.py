import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from model_talk.models import Chat_session, Chat_sessions

tokenizer = AutoTokenizer.from_pretrained("C:\\Users\\pc798\\OneDrive\\Escritorio\\IA learn\\list_project\\modelo_IA\\model_enfermeria_final")
model = AutoModelForCausalLM.from_pretrained("C:\\Users\\pc798\\OneDrive\\Escritorio\\IA learn\\list_project\\modelo_IA\\model_enfermeria_final")

def generar_respuesta_con_Contexto(sesion):
    mensajes = Chat_session.objects.filter(id_sesion=sesion)

    historial = ""

    for m in mensajes:
        if m.role == "user":
            historial += f"Usuario: {m.contenido}\n"
        else:
            historial += f"Asistente: {m.contenido}\n"

    prompt = f"""
Eres un asistente experto en enfermería universitaria.
Respondes de forma clara, técnica y pedagógica.

{historial}
Asistente:
"""

    inputs = tokenizer(prompt, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.6,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    texto = tokenizer.decode(outputs[0], skip_special_tokens=True)

    respuesta = texto.split("Asistente:")[-1].strip()
    if "Usuario:" in respuesta:
        respuesta = respuesta.split("Usuario:")[0].strip()

    return respuesta