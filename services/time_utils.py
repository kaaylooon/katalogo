import datetime
from typing import List, Dict

def verificar_disponibilidade(horario: List[Dict]) -> bool:
    now = datetime.datetime.now().time()  # pega o horário atual (time)

    abre = horario[0]["abre"]   
    fecha = horario[0]["fecha"] 

    return abre <= now <= fecha