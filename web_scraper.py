import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Función para crear la carpeta si no existe
def crear_carpeta(carpeta):
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
        print(f"Carpeta '{carpeta}' creada.")
    else:
        print(f"Carpeta '{carpeta}' ya existe.")

# Función para validar el formato de la imagen
def es_formato_valido(url):
    formatos_validos = ['.png', '.jpg', '.jpeg', '.webp']
    return any(url.lower().endswith(formato) for formato in formatos_validos)

# Función para descargar una imagen
def descargar_imagen(url, carpeta):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        nombre_imagen = os.path.join(carpeta, url.split("/")[-1])
        with open(nombre_imagen, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Imagen descargada: {nombre_imagen}")
    except requests.RequestException as e:
        print(f"Error al descargar {url}: {e}")

# Función principal para extraer y descargar imágenes
def extraer_y_descargar_imagenes(url, carpeta):
    crear_carpeta(carpeta)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        imgs = soup.find_all('img')
        
        for img in imgs:
            src = img.get('src')
            if not src:
                continue
            img_url = urljoin(url, src)
            if es_formato_valido(img_url):
                descargar_imagen(img_url, carpeta)
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")

# URL del sitio web a recorrer
url = 'https://demo.ezoco.es/digital/tienda'
# Carpeta donde se guardarán las imágenes
carpeta = 'imagenes'

# Llamada a la función principal
extraer_y_descargar_imagenes(url, carpeta)
