import requests
from bs4 import BeautifulSoup
import simplebot
from simplebot.bot import DeltaBot, Replies

@simplebot.command
def bing_image(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Obtener una imagen basada en el texto dado.

    Ejemplo:
    /bing_image gatos y perros
    """
    _bing_image_cmd(1, bot, payload, message, replies)

@simplebot.command
def bing_image5(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Buscar imágenes en Bing y devolver hasta cinco resultados.

    Ejemplo:
    /bing_image5 rosas
    """
    _bing_image_cmd(5, bot, payload, message, replies)

def _bing_image_cmd(img_count: int, bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    if not payload:
        replies.add(text="❌ No se proporcionó texto", quote=message)
        return
    imgs = img_count
    for filename, data in _get_bing_images(bot, payload):
        replies.add(filename=filename, bytefile=io.BytesIO(data))
        imgs -= 1
        if imgs <= 0:
            break
    if imgs == img_count:
        replies.add(text="❌ No hay resultados", quote=message)

def _get_bing_images(bot: DeltaBot, query: str):
    url = f"https://www.bing.com/images/search?q={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img", class_="mimg")
    for image in images[:num_results]:
        image_url = image["src"]
        image_data = requests.get(image_url).content
        filename = f"{query}_{num_results}.jpg"
        yield filename, image_data
