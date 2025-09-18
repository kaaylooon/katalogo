

from flask import url_for, session


def serialize_business(b):
	actions = f"""
	<form method='POST' action='{url_for('admin.toggle_premium', business_id=b[0])}' style='display:inline'>
		<button class='btn btn-sm btn-outline-success'>Premium</button>
	</form>

	<a href='{url_for('business.edit', business_id=b[0])}' class='btn btn-sm btn-outline-secondary'>Editar</a>

	<form method='POST' action='{url_for('business.delbusiness', business_id=b[0])}' style='display:inline'>
		<button class='btn btn-sm btn-outline-danger'>Excluir</button>
	</form>
	"""
	return {
		"id": b[0],
		"nome": b[1],
		"categoria": b[3],
		"owner": b[9],
		"premium": bool(b[13]),
		"created_at": b[8],
		"actions": actions
	}


def serialize_user(u):
	return {
		"id": u[0],
		"nome": u[1],
		"email": u[2],
		"contact": u[4],
		"role": u[6]
	}

def serialize_comment(c):
	actions = f"""
		<a class='btn btn-sm btn-outline-secondary' data-bs-toggle='modal' data-bs-target='#edit_comment_{c[0]}'>Editar</a>

		<form method='POST' action='{url_for('comentario.excluir', business_id=c[3], comment_id=c[0])}' style='display:inline'>
			<button class='btn btn-sm btn-outline-danger'>Excluir</button>
		</form>
	"""
	return {
		"id": c[0],
		"autor": c[1],
		"content": c[2],
		"business_id": c[3],
		"created_at": c[4],
		"edited": bool(c[5]),
		"actions": actions
	}
