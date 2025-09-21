from flask import url_for


def serialize_business(b):
    actions = f"""
    <form method='POST' action='{url_for('admin.toggle_premium', business_id=b['id'])}' style='display:inline'>
        <button class='btn btn-sm btn-outline-success'>Premium</button>
    </form>
    <a href='{url_for('business.edit', business_id=b['id'])}' class='btn btn-sm btn-outline-secondary'>Editar</a>
    <form method='POST' action='{url_for('business.delbusiness', business_id=b['id'])}' style='display:inline'>
        <button class='btn btn-sm btn-outline-danger'>Excluir</button>
    </form>
    """
    return {
        "id": b['id'],
        "nome": b['nome'],
        "categoria": b['categoria'],
        "owner": b['by_user'],
        "premium": bool(b['premium']),
        "premium_valid_until": b['premium_valid_until'],
        "evento": b['evento'],
        "created_at": b['added_at'],
        "actions": actions
    }

def serialize_user(u):
    actions = f"""
        <a href='{url_for('user.perfiledit', user_id=u['id'])}' class='btn btn-sm btn-outline-secondary'>Editar</a>
        <form method='POST' action='{url_for('user.excluir', user_id=u['id'])}' style='display:inline'>
            <button class='btn btn-sm btn-outline-danger'>Excluir</button>
        </form>
    """
    return {
        "id": u['id'],
        "nome": u['username'],
        "email": u['email'],
        "contact": u['telephone'],
        "role": u['role'],
        "actions": actions
    }

def serialize_feed(f):
    return {
        "id": f['id'],
        "business_id": f['business_id'],
        "created_at": f['created_at'],
        "feed_id": f['id']
    }

def serialize_comment(c):
    actions = f"""
        <a class='btn btn-sm btn-outline-secondary' data-bs-toggle='modal' data-bs-target='#edit_comment_{c['id']}'>Editar</a>
        <form method='POST' action='{url_for('comentario.excluir', business_id=c['business_id'], comment_id=c['id'])}' style='display:inline'>
            <button class='btn btn-sm btn-outline-danger'>Excluir</button>
        </form>
    """
    return {
        "id": c['id'],
        "autor": c['user_id'],
        "content": c['content'],
        "business_id": c['business_id'],
        "created_at": c['created_at'],
        "edited": bool(c['edited']),
        "actions": actions
    }