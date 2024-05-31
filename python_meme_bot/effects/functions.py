from PIL import Image, ImageDraw, ImageFont
from PIL.ImageColor import getrgb
from PIL.ImageEnhance import Brightness
from io import BytesIO
import textwrap, os, random, time, math

random.seed(time.time())

BASE_WIDTH = 1200
IMPACT_FONT_FILE = os.path.join("fonts", "impact.ttf")
ARIAL_FONT_FILE = os.path.join("fonts", "opensans.ttf")

k1 = 0.612123
k2 = 1.216428
k3 = 0.341428
k4 = 0.364576

'''
k1 = 0.6
k2 = 2 * k1
k3 = k1 / 2
k4 = k3
'''

def _get_font_size(h, w, n, letter_spacing, line_spacing):

    font_size = (math.sqrt(4 * k1 * k2 * h * n * w + math.pow(k2, 2) * math.pow(n, 2) * math.pow(letter_spacing, 2) + ((2 * k1 * k2 * k3 - 2 * k4 * math.pow(k2, 2)) * math.pow(n, 2) - 2 * k1 * k2 * line_spacing) * letter_spacing + math.pow(k1, 2) * math.pow(n, 2) * math.pow(line_spacing, 2) + (2 * k1 * k4 * k2 - 2 * math.pow(k1, 2) * k3) * math.pow(n, 2) * line_spacing + (math.pow(k1, 2) * math.pow(k3, 2) - 2 * k1 * k4 * k2 * k3 + math.pow(k4, 2) * math.pow(k2, 2)) * math.pow(n, 2)) - k2 * n * letter_spacing - k1 * n * line_spacing + (k1 * k3 + k4 * k2) * n) / (2 * k1 * k2 * n)
    line_width = w / (k1 * font_size - k4 + letter_spacing)
    return font_size, line_width

def _darken_image(image: Image, amount=0.5):
    return Brightness(image).enhance(amount)

def _draw_line(d: ImageDraw, x: int, y: int, line: str, font: ImageFont, letter_spacing: int = 9, fill = (255, 255, 255), stroke_width: int = 9, stroke_fill = (0, 0, 0)):
    
    for i in range(len(line)):
                d.text((x, y), line[i], fill=fill, stroke_width=stroke_width, font=font, stroke_fill=stroke_fill)
                x += font.getlength(line[i]) + letter_spacing

def _draw_ttbt(text: str, img: Image, bottom=False):
        
    LETTER_SPACING = 9
    LINE_SPACING = 10  
    FILL = (255, 255, 255)
    STROKE_WIDTH = 9
    STROKE_FILL = (0, 0, 0)
    FONT_BASE = 100
    MARGIN = 10

    split_caption = textwrap.wrap(text.upper(), width=20)
    if split_caption == []:
        return
    
    font_size = FONT_BASE + 10 if len(split_caption) <= 1 else FONT_BASE
    font = ImageFont.truetype(font=IMPACT_FONT_FILE, size=font_size)
    img_width, img_height = img.size

    d = ImageDraw.Draw(img)
    txt_height = d.textbbox((0, 0), split_caption[0], font=font)[3]

    if bottom:
        factor = -1
        split_caption.reverse()
        y = (img_height - (img_height / MARGIN)) - (txt_height / 2)
    else:
        factor = 1
        y = (img_height / MARGIN) - (txt_height / 1.5)

    for line in split_caption:
        txt_width = d.textbbox((0, 0), line, font=font)[2]

        x = (img_width - txt_width - (len(line) * LETTER_SPACING)) / 2

        _draw_line(d, x, y, line, font, LETTER_SPACING, FILL, STROKE_WIDTH, STROKE_FILL)

        y += (txt_height + LINE_SPACING) * factor

def img_to_bio(image):
    
    bio = BytesIO()
    
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")

    image.save(bio, 'JPEG')
    bio.seek(0)
    return bio

def bt_effect(text: str, img: Image):

    lines = [x for x in text.split("\n") if x]
    bt = lines[0] if len(lines) > 0 else None
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    
    if bt is None:
        return img
    
    _draw_ttbt(bt, img, bottom=True)

    img = img.resize((int(BASE_WIDTH / 2), int(float(img.size[1]) * (BASE_WIDTH / 2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img_to_bio(img)

def ttbt_effect(text: str, img: Image):
    
    lines = [x for x in text.split("\n") if x]
    
    tt = lines[0] if len(lines) > 0 else None
    bt = lines[1] if len(lines) > 1 else None
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    
    if tt is None and bt is None:
        return img
    
    if (tt is not None):
        _draw_ttbt(tt, img)
    if (bt is not None):
        _draw_ttbt(bt, img, bottom=True)
        
    img = img.resize((int(BASE_WIDTH / 2), int(float(img.size[1]) * (BASE_WIDTH / 2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img_to_bio(img)

def splash_effect(input_text: str, img: Image):
    
    LETTER_SPACING = 1
    LINE_SPACING = 3  
    FILL = (255, 255, 255)
    STROKE_WIDTH = 1
    STROKE_FILL = (0, 0, 0)
    
    input_text = input_text.strip()
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    
    img = _darken_image(img)
    
    img_width, img_height = img.size
    
    w = img_width / 2
    h = img_height / 2
    
    n = len(input_text)
    
    try:
        FONT_BASE, LINE_WIDTH = _get_font_size(h, w, n, LETTER_SPACING, LINE_SPACING)
    except ValueError as e:
        print(e)
        FONT_BASE = 60
        LINE_WIDTH = 30
    
    lines = [ x for x in input_text.split("\n") if x ]
    first_line = lines.pop(0)
    text = "\n".join(lines)
    
    FONT_BASE /= 2
    LINE_WIDTH *= 2

    text = textwrap.wrap(text.upper(), width=int(LINE_WIDTH))
    
    if text == []:
        print("Splash effect needs two lines!")
        return
    text.insert(0, first_line)
    n_lines = len(text)

    font_first = ImageFont.truetype(font=ARIAL_FONT_FILE, size=int(FONT_BASE - (FONT_BASE / 2.5)))
    font_base = ImageFont.truetype(font=ARIAL_FONT_FILE, size=int(FONT_BASE))

    d = ImageDraw.Draw(img)

    _, _, first_txt_width, first_txt_height = d.textbbox((0, 0), text[0], font=font_first)
    _, _, max_txt_width, txt_height = d.textbbox((0, 0), text[1], font=font_base)

    total_height = (txt_height + LINE_SPACING) * (n_lines - 1) + LINE_SPACING + first_txt_height
        
    y = (img_height - total_height) / 2
        
    for i in range(1, n_lines):
        
        temp = int(font_base.getlength(text[i]))
        if temp > max_txt_width:
            max_txt_width = temp

    max_txt_width = max_txt_width if max_txt_width > first_txt_width else first_txt_width
    x_start = (img_width - max_txt_width) / 2
        
    for i in range(n_lines):
        
        font = font_base if i > 0 else font_first
        _draw_line(d=d, x=x_start, y=y, line=text[i], font=font, letter_spacing=LETTER_SPACING, fill=FILL, stroke_width=STROKE_WIDTH, stroke_fill=STROKE_FILL)

        y += (txt_height if i > 0 else first_txt_height) + LINE_SPACING
        
    img = img.resize((int(BASE_WIDTH / 2), int(float(img.size[1]) * (BASE_WIDTH / 2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img_to_bio(img)

def wot_effect(input_text: str, img: Image):
    
    LETTER_SPACING = 1
    LINE_SPACING = 3  
    FILL = (255, 255, 255)
    STROKE_WIDTH = 1
    STROKE_FILL = (0, 0, 0)
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    img = _darken_image(img)
    
    img_width, img_height = img.size
    
    n = len(input_text.strip())

    MARGIN_H = img_height / (n / 270)
    MARGIN_W = 0
    
    w = img_width - MARGIN_W
    h = img_height - MARGIN_H
    
    try:
        FONT_BASE, LINE_WIDTH = _get_font_size(h, w, n, LETTER_SPACING, LINE_SPACING)
    except ValueError as e:
        print(e)
        FONT_BASE = 60
        LINE_WIDTH = 30

    text = textwrap.wrap(input_text.strip(), width=int(LINE_WIDTH))

    if text == []:
        return None
    
    n_lines = len(text)
    font = ImageFont.truetype(font=ARIAL_FONT_FILE, size=int(FONT_BASE))
    d = ImageDraw.Draw(img)
    
    txt_height = k2 * FONT_BASE - k3 + LINE_SPACING
    max_text_height = txt_height * n_lines
    y = (img_height - max_text_height) / 2
        
    for i in range(n_lines):
        txt_width = d.textbbox((0, 0), text[i], font=font)[2]
        x = (img_width - txt_width - (len(text[i]) * LETTER_SPACING)) / 2

        _draw_line(d=d, x=x, y=y, line=text[i], font=font, letter_spacing=LETTER_SPACING, fill=FILL, stroke_width=STROKE_WIDTH, stroke_fill=STROKE_FILL)

        y += txt_height + LINE_SPACING
        
    img = img.resize((int(BASE_WIDTH / 2), int(float(img.size[1]) * (BASE_WIDTH / 2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img_to_bio(img)

def text_effect(text: str, img: Image):
    LETTER_SPACING = 1
    LINE_SPACING = 3
    STROKE_WIDTH = 1
    STROKE_FILL = (0, 0, 0)
    FONT_BASE = 75
    MARGIN = 10
    LINE_WIDTH = 20
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    
    text = textwrap.wrap(text.strip(), width=LINE_WIDTH)
    if text == []:
        return
    n_lines = len(text)
    
    font = ImageFont.truetype(font=ARIAL_FONT_FILE, size=FONT_BASE)
    
    img_width, img_height = img.size
    d = ImageDraw.Draw(img)

    _, _, _, txt_height = d.textbbox((0, 0), text[0], font=font)
    
    max_length = len(text[0])
    choice = 0
    if n_lines > 1:
        for i in range(1, n_lines):
            length = len(text[i])
            if length > max_length:
                choice = i
                max_length = length
            
    max_txt_width = int(font.getlength(text[choice]))
    
    total_height = int((txt_height + LINE_SPACING) * n_lines)
    
    y_inf = 0
    y_sup = max(0, img_height - total_height)
    x_inf = 0
    x_sup = max(0, img_width - max_txt_width)
    
    fill = getrgb(f"hsl({random.randint(0, 359)},100%,{random.randint(60, 75)}%)") # hue [0:359], saturation, lightness
    #print(f"x-> {x_inf}:{x_sup}; y ->{y_inf}:{y_sup}; color: {fill}")

    x = random.randint(x_inf, x_sup)
    y = random.randint(y_inf, y_sup)
    
    for i in range(n_lines):
        
        _draw_line(d=d, x=x, y=y, line=text[i], font=font, letter_spacing=LETTER_SPACING, fill=fill, stroke_width=STROKE_WIDTH, stroke_fill=STROKE_FILL)

        y += txt_height + LINE_SPACING
        
    img = img.resize((int(BASE_WIDTH / 2), int(float(img.size[1]) * (BASE_WIDTH / 2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img_to_bio(img)

def test_multiple(text, effect, modifier=""):

        imgs = os.listdir("test")
        for i in range(len(imgs)):
            image = effect(text, Image.open(os.path.join("test", imgs[i])))
            if image is None:
                return print("Image test failed!")
            
            Image.open(image).save(os.path.join("test_output", f'output{modifier}{i}.jpg'), optimize=True, quality=80)
        return print("Image test successful")

def test(text, effect, modifier=""):

        image = effect(text, Image.open("image.jpg"))
        Image.open(image).save('output.jpg', optimize=True, quality=80)

        print("Image test successful")

def main():
    input_text = '''
    BiRabittoh (@BiRabittoh)
Godo godo godo godo godo godo godo godo godo godo godo
'''
    
    #test(input_text, splash_effect)
    test_multiple(input_text, splash_effect)
    #test_multiple(input_text, splash_effect, "_long")
    
if __name__ ==  "__main__":
    main()