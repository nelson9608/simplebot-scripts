from urllib.parse import quote_plus

import imdb
import simplebot
from deltachat import Message
from simplebot.bot import DeltaBot, Replies
from simplebot_instantview import prepare_html, session  # noqa


@simplebot.command()
def tvseries(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Envie el comando y siga las instrucciones"""
  
serie =input("escribe el nombre de la serie")
# Crea una instancia de la clase IMDb
ia = imdb.IMDb()

# Busca la serie de TV por su nombre
series = ia.search_movie(serie)

# Obtiene el ID de la serie de TV
serie_id = series[0].getID()

# Obtiene la información de la serie de TV
serie = ia.get_movie(serie_id)

# Obtiene la sinopsis de la serie de TV
sinopsis = serie.get('plot')

# Imprime la sinopsis de la serie de TV
print(sinopsis)

