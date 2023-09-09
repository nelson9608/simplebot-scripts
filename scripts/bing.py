import simplebot
from simplebot_downloader import download
import requests
from bs4 import BeautifulSoup

@simplebot.command
def bing_images(message, replies):
    """Busca imágenes en Bing y devuelve las primeras 5 imágenes."""
    query = message.text.partition(' ')[2]
    if not query:
        replies.add(text='Por favor, proporciona una consulta de búsqueda.')
        return

    url = f'https://www.bing.com/images/search?q={query}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    images = soup.find_all('img', class_='mimg')
    for image in images[:5]:
        image_url = image['src']
        download(image_url, 'bing_image.jpg')  # Usa simplebot_downloader para descargar la imagen
        replies.add(filename='bing_image.jpg', caption=f'Imagen de {query} en Bing')
