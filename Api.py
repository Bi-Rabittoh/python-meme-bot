
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import requests, random, time

base_url = "https://danbooru.donmai.us/"
base_url_test = "https://testbooru.donmai.us/"

page_suffix = "post/index.json"
post_suffix = "posts/"

ratings = [
    'g', # general
    's', # sensitive
    'q', # questionable
    'e', # explicit
]

rating_normal = "g,s"
rating_lewd = "q"

limit = 100
max_pages = 700
sleep_seconds = 3
max_tries = 5

def get_random_image(rating=rating_normal):
    params = {
        "limit": limit,
        #"tags": "order:change_desc rating:" + rating,
        "tags": "rating:" + rating,
    }
    #url = "https://danbooru.donmai.us/post/index.json"
    count = 0
    while count < max_tries:
        params['page'] = random.randint(1,max_pages)
        r = requests.get(base_url + page_suffix, params)
        page = r.json()
        #print("Page: " + str(params['page']))
    
        if 'success' in page:
            if page['success'] == False:
                print("Error: " + page['error'])
                print("Message: " + page['message'])
            else:
                print(page)
        else:
            n = random.randint(0, limit - 1)
            #print("File: " + str(n))
            try:
                file_url = page[n]['file_url']
                r = requests.get(file_url)
                try:
                    img = Image.open(BytesIO(r.content))
                    return img, base_url + post_suffix + str(page[n]['id'])
                except UnidentifiedImageError:
                    print("Unidentified image: " + file_url)
            except KeyError:
                print("Image has no file_url. post: " + base_url + post_suffix + str(page[n]['id']))
                print(str(page[n]))
            except IndexError:
                print("Page does not exist. " + str(page))
        
        count += 1
        print(f"Try #{count} failed. Retrying in {sleep_seconds} seconds...\n")
        #time.sleep(sleep_seconds)
    print(f"Reached {count} tries. Giving up.")
    return None, None
