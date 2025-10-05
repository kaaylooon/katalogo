
from flask import Blueprint, redirect, request, url_for, session
from auth import author_or_admin_required, login_required
from services.comment_service import criar_comentario
from services import *
from db import *

routes = Blueprint("comentario", __name__)

@routes.route('/business/<int:business_id>/comentario/comentar', methods=['POST'])
@login_required
def comentar(business_id: int):
    business = buscar_id_business(business_id)
    if not business:
        return "Negócio não encontrado", 404
    content = request.form.get("content")

    criar_comentario(session["user_id"], business_id, content)

    log_event(
            "## Comentário adicionado",
            level=logging.INFO,
            business_id=business_id,
            user_id=session['user_id'],
            conteudo=content
        )

    return redirect(request.referrer or '/')

@routes.route('/business/<int:business_id>/comentario/<int:comment_id>/excluir', methods=['POST'])
@login_required
@author_or_admin_required(
    mostrar_comentario_by_id,   
    author_field="user_id",
    arg_name="comment_id"
)
def excluir(comment_id: int, business_id: int):
    comentario = mostrar_comentario_by_id(comment_id)
    if comentario:
        content = comentario['content']

    del_comentario(comment_id)

    log_event(
            "## Comentário excluído",
            level=logging.INFO,
            business_id=business_id,
            user_id=session['user_id'],
            conteudo=content
        )

    return redirect(request.referrer or '/')

@routes.route('/business/<int:business_id>/comentario/<int:comment_id>/editar', methods=['POST'])
@login_required
@author_or_admin_required(
    mostrar_comentario_by_id,   
    author_field="user_id",
    arg_name="comment_id"
)
def editar(business_id: int, comment_id: int):
    business = buscar_id_business(business_id)
    if not business:
        return "Negócio não encontrado", 404
    comentario = mostrar_comentario_by_id(comment_id)
    if comentario:
        conteudoAnterior = comentario['content']

    if request.method == "POST":
        content = request.form.get("content")
        editar_comentario(content, True, comment_id)

        log_event(
            "## Comentário editado",
            level=logging.INFO,
            business_id=business_id,
            user_id=session['user_id'],
            conteudoAnterior=conteudoAnterior,
            novoConteudo=content
        )

    return redirect(request.referrer or '/')


