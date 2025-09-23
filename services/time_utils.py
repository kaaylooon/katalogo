import datetime
from typing import List, Dict

def verificar_disponibilidade(horario: List[Dict]) -> bool:
    if not horario or not horario[0] or not horario[0]["abre"]:
        return False

    now = datetime.datetime.now().time() 

    abre = horario[0]["abre"]   
    fecha = horario[0]["fecha"] 
    
    if abre < fecha: 
        return abre <= now <= fecha
    else:
        return now >= abre or now <= fecha
