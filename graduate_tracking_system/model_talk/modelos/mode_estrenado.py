import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from model_talk.models import Chat_session

MODEL_ID = os.environ.get("HF_MODEL_ID", "criskiller/modelo_academico_final")

_tokenizer = None
_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        _tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        _model = AutoModelForCausalLM.from_pretrained(MODEL_ID)
        _model.to(_device)
        _model.eval()
    return _tokenizer, _model

def generar_respuesta_con_Contexto(sesion):
    tokenizer, model = get_model()

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
    inputs = {k: v.to(_device) for k, v in inputs.items()}

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
