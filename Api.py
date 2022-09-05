
from PIL import Image
from io import BytesIO
import requests, random, time

url = "https://danbooru.donmai.us/post/index.json"
test_url = "https://testbooru.donmai.us/post/index.json"

ratings = [
    'g', # general
    's', # sensitive
    'q', # questionable
    'e', # explicit
]

params = {
    "limit": 100,
    "page": random.randint(1,560),
    #"page": 560,
    "tags": "order:change_desc rating:"
}

def get_random_image(rating="g,s"):
    params["tags"] += rating
    
    switch = True
    while switch:
        r = requests.get(url, params)
        page = r.json()
        print("Page: " + str(params['page']))
    
        if 'success' in page:
            if page['success'] == False:
                print("Error: " + page['error'])
                print("Message: " + page['message'])
                print("Retrying in 3 seconds...\n")
            else:
                print(page)
            time.sleep(3)
        else:
            n = random.randint(0, 99)
            print("File: " + str(n))
            file_url = page[n]['file_url']
            r = requests.get(file_url)
            try:
                img = Image.open(BytesIO(r.content))
            except UnidentifiedImageError:
                print("Unidentified image.")
                
            print("Done.\n")
            return img, f"https://danbooru.donmai.us/posts/{page[n]['id']}"
