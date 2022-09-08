
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import requests, random, time, logging, time

random.seed(time.time())

base_url = "https://danbooru.donmai.us/"
base_url_test = "https://testbooru.donmai.us/"

ratings = [
    'g', # general
    's', # sensitive
    'q', # questionable
    'e', # explicit
]

rating_normal = "rating:g,s"
rating_lewd = "rating:s,q"

supported_file_types = [
    ".jpg",
    ".jpeg",
    ".png"
]

def _valid_extension(fname: str):
    for t in [".jpg", ".jpeg", ".png"]:
        if fname.lower().endswith(t):
            return True
    return False

def get_random_image(rating=rating_normal, tags=""):
    page_suffix = "post/index.json"
    post_suffix = "posts/"
    
    limit = 100
    max_pages = 1000
    sleep_seconds = 3
    max_tries = 5

    params = {
        "limit": limit,
        "tags": rating + tags,
    }
    
    if tags != "":
        max_pages = 50
        
    count = 0
    while count < max_tries:
        params['page'] = random.randint(1, max_pages)
        page = requests.get(base_url + page_suffix, params).json()
        n = random.randint(0, params['limit'] - 1)
        
        try:
            file_url = page[n]['file_url']
            if not _valid_extension(file_url):
                raise Exception
            r = requests.get(file_url)
            img = Image.open(BytesIO(r.content))
            link = base_url + post_suffix + str(page[n]['id'])
            return img, link
            
        except (KeyError, IndexError, Exception):
            logging.warning("Can't display image.")
        except UnidentifiedImageError:
            logging.warning("Unidentified image: " + file_url)
        
        count += 1
        logging.warning(f"Try #{count} failed.\n")
        #time.sleep(sleep_seconds)
    logging.error(f"Reached {count} tries. Giving up.")
    return None, None
