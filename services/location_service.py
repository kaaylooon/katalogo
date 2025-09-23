
import requests
from .logger import logger

ESTADO_URL = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
CEP_URL = "https://cep.awesomeapi.com.br/"
GEOAPI_URL = "https://nominatim.openstreetmap.org/search"


def get_municipios(uf):
	url = f"{ESTADO_URL}/{uf}/municipios"
	response = requests.get(url)
	if response.status_code == 200:
		return response.json()
	else:
		return []

def get_coordenadas(address):
	logger.info(f"Tentando obter coordenadas para o endereço: {address}") 
	params = {"q": address, "format": "json"}
	headers = {"User-Agent": "AppTest/1.0 (kaylon.alt@outlook.com)"}
	try:
		response = requests.get(GEOAPI_URL, params=params, headers=headers, timeout=5)
		response.raise_for_status()
		data = response.json()
		if data:
			lat = float(data[0]["lat"])
			lon = float(data[0]["lon"])
			return lat, lon
		else:
			return None, None
	except Exception as e:
		print("Erro ao obter coordenadas:", e)
		return None, None


def get_cep(cep):
	url = f"{CEP_URL}/json/{cep}"
	response = requests.get(url)
	if response.status_code == 200:
		return response.json()
	else:
		return response.status_code