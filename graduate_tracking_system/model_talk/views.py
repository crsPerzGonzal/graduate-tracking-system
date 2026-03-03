from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse ,JsonResponse
from  .models import Chat_session, Chat_sessions
from .modelos.mode_estrenado import generar_respuesta_con_Contexto
from django.db.models import Q
# Create your views here.


def chat_view(request, session_id = None): 
    if session_id is None:
        sesion = Chat_sessions.objects.create()
        return redirect("chat_con_id", session_id=sesion.id_sesion)

    sesion = get_object_or_404(Chat_sessions, id_sesion=session_id)
    
    if request.method == "POST":
        mensaje_usuaro = request.POST.get("mensaje")
        
        Chat_session.objects.create(
            id_sesion = sesion,
            role="user",
            contenido=mensaje_usuaro
        )
        respuesta_ia = generar_respuesta_con_Contexto(sesion)

        Chat_session.objects.create(
            id_sesion=sesion,
            role="ia",
            contenido=respuesta_ia
        )
    mensajes = sesion.chat_session_set.all().order_by("timestamp")
    return render(request, "model_talk/chat.html", {
        "sesion": sesion,
        "mensajes":mensajes
    })


def obtener_historial(request, session_id):
    session = get_object_or_404(Chat_sessions, id_sesion=session_id)
    mensajes = session.chat_session_set.all().order_by("timestamp")

    data = [
        {
            "role": m.role,
            "content": m.contenido,
        }
        for m in mensajes
    ]
    return JsonResponse({"historial": data})


def buscar_conversaciones(request):
    query = request.GET.get("q")
    sesiones = Chat_sessions.objects.all()

    if query: 
        sesiones = Chat_sessions.objects.filter(
             chat_session__contenido__icontains =query
        ).distinct()
    return render(request, "model_talk/buscar.html", {
        "sesiones": sesiones,
        "query": query
    })