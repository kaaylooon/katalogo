import datetime
from typing import List, Tuple

def verificar_disponibilidade(horario: List[Tuple]) -> bool:
	now = datetime.datetime.now()
	now_str = now.strftime("%H:%M")

	abre = horario[0][3]
	fecha = horario[0][4]

	if abre <= now_str <= fecha:
		return True
	else:
		return False