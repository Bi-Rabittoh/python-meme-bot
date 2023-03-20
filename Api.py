import logging
import requests
from io import BytesIO

from PIL import Image, UnidentifiedImageError
from anime_api.apis import WaifuPicsAPI
from anime_api.apis.waifu_pics.types import ImageCategory

max_tries = 5
supported_file_types = [".jpg", ".jpeg", ".png"]
api = WaifuPicsAPI()


def _valid_extension(fname: str):
    for t in supported_file_types:
        if fname.lower().endswith(t):
            return True
    return False


def get_random_image(nsfw=False):
    cat = ImageCategory.NSFW.WAIFU if nsfw else ImageCategory.SFW.WAIFU

    count = 0
    while count < max_tries:
        try:
            img = api.get_random_image(category=cat)
            if not _valid_extension(img.url):
                raise Exception
            r = requests.get(img.url)
            image = Image.open(BytesIO(r.content))

            return image, img.url

        except (KeyError, IndexError, Exception):
            logging.warning("Can't display image.")
        except UnidentifiedImageError:
            logging.warning("Unidentified image: " + img.url)

        count += 1
        logging.warning(f"Try #{count} failed.\n")
    logging.error(f"Reached {count} tries. Giving up.")
    return None, None
