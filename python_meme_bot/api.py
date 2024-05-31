import logging
import requests
from io import BytesIO

from PIL import Image, UnidentifiedImageError

max_tries = 5
supported_file_types = [".jpg", ".jpeg", ".png"]
endpoint = "https://api.waifu.pics"

class APIException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"Error {self.status_code}: {self.message}"

def _valid_extension(fname: str):
    for t in supported_file_types:
        if fname.lower().endswith(t):
            return True
    return False

def get_random_image(nsfw=False):
    count = 0
    while count < max_tries:
        try:
            apiUrl = endpoint + f"/{'nsfw' if nsfw else 'sfw'}/waifu"
            response = requests.get(apiUrl)    

            content = response.json()
            if response.status_code != 200:
                raise APIException(response.status_code, content['message'])
            
            url = content["url"]
            if not _valid_extension(url):
                raise AssertionError
            
            r = requests.get(url)
            b = BytesIO(r.content)
            image = Image.open(b)
            return image, url

        except (KeyError, IndexError, AssertionError, APIException):
            logging.warning("Can't display image.")
        except UnidentifiedImageError:
            logging.warning("Unidentified image: " + url)

        count += 1
        logging.warning(f"Try #{count} failed.\n")
    logging.error(f"Reached {count} tries. Giving up.")
    return None, None
