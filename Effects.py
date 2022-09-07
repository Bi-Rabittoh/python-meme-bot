from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import textwrap, os, random, time

random.seed(time.time())

BASE_WIDTH = 1200
IMPACT_FONT_FILE = os.path.join("fonts", "impact.ttf")
ARIAL_FONT_FILE = os.path.join("fonts", "opensans.ttf")

def _darken_image(image: Image, amount=0.5):
    return ImageEnhance.Brightness(image).enhance(amount)

def _draw_line(d: ImageDraw, x: int, y: int, line: str, font: ImageFont, letter_spacing: int = 9, fill = (255, 255, 255), stroke_width: int = 9, stroke_fill = (0, 0, 0)):
    
    for i in range(len(line)):
                d.text((x, y), line[i], fill=fill, stroke_width=stroke_width, font=font, stroke_fill=stroke_fill)
                x += font.getlength(line[i]) + letter_spacing

def tt_bt_effect(text: str, img: Image):
    LETTER_SPACING = 9
    LINE_SPACING = 10  
    FILL = (255, 255, 255)
    STROKE_WIDTH = 9
    STROKE_FILL = (0, 0, 0)
    FONT_BASE = 100
    MARGIN = 10
    
    def _draw_tt_bt(text, img, bottom=False):
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

            x = (img_width - txt_width - (len(line) * LETTER_SPACING))/2

            _draw_line(d, x, y, line, font, LETTER_SPACING, FILL, STROKE_WIDTH, STROKE_FILL)

            y += (txt_height + LINE_SPACING) * factor
    
    lines = [x for x in text.split("\n") if x]
    
    tt = lines[0] if len(lines) > 0 else None
    bt = lines[1] if len(lines) > 1 else None
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    
    if tt is None and bt is None:
        return img
    
    if (tt is not None):
        _draw_tt_bt(tt, img)
    if (bt is not None):
        _draw_tt_bt(bt, img, bottom=True)
        
    img = img.resize((int(BASE_WIDTH/2), int(float(img.size[1]) * (BASE_WIDTH/2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img

def splash_effect(text: str, img: Image):
    LETTER_SPACING = 1
    LINE_SPACING = 3  
    FILL = (255, 255, 255)
    STROKE_WIDTH = 1
    STROKE_FILL = (0, 0, 0)
    FONT_FIRST = 50
    FONT_BASE = 75
    MARGIN = 10
    LINE_WIDTH = 20
    
    lines = [x for x in text.split("\n") if x]
    first_line = lines.pop(0)
    text = "\n".join(lines)
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    
    img = _darken_image(img)
    
    text = textwrap.wrap(text.upper(), width=LINE_WIDTH)
    if text == []:
        return
    text.insert(0, first_line)
    
    font_first = ImageFont.truetype(font=ARIAL_FONT_FILE, size=FONT_FIRST)
    font_base = ImageFont.truetype(font=ARIAL_FONT_FILE, size=FONT_BASE)
        
    img_width, img_height = img.size
    d = ImageDraw.Draw(img)
        
    _, _, first_txt_width, first_txt_height = d.textbbox((0, 0), text[0], font=font_first)
    _, _, max_txt_width, txt_height = d.textbbox((0, 0), text[1], font=font_base)

    total_height = (txt_height + LINE_SPACING) * (len(text) - 1) + LINE_SPACING + first_txt_height
    y = (img_height - total_height) / 2
        
    for i in range(1, len(text)):
        temp = int(font_base.getlength(text[i]))
        if temp > max_txt_width:
            max_txt_width = temp

    max_txt_width = max_txt_width if max_txt_width > first_txt_width else first_txt_width
    x_start = (img_width - max_txt_width) / 2
        
    for i in range(len(text)):
        '''
        if align == "center":
            txt_width = d.textbbox((0, 0), line, font=font)[2]
            x = (img_width - txt_width - (len(line) * LETTER_SPACING))/2
        '''
        font = font_base if i > 0 else font_first
        _draw_line(d=d, x=x_start, y=y, line=text[i], font=font, letter_spacing=LETTER_SPACING, fill=FILL, stroke_width=STROKE_WIDTH, stroke_fill=STROKE_FILL)

        y += (txt_height if i > 0 else first_txt_height) + LINE_SPACING
        
    img = img.resize((int(BASE_WIDTH/2), int(float(img.size[1]) * (BASE_WIDTH/2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img

def wot_effect(text: str, img: Image):
    LETTER_SPACING = 1
    LINE_SPACING = 3  
    FILL = (255, 255, 255)
    STROKE_WIDTH = 1
    STROKE_FILL = (0, 0, 0)
    FONT_BASE = 50
    MARGIN = 10
    LINE_WIDTH = 44
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    img = _darken_image(img)
    
    text = textwrap.wrap(text, width=LINE_WIDTH)
    if text == []:
        return
    
    font = ImageFont.truetype(font=ARIAL_FONT_FILE, size=FONT_BASE)
        
    img_width, img_height = img.size
    d = ImageDraw.Draw(img)
        
    _, _, txt_width, txt_height = d.textbbox((0, 0), text[0], font=font)

    total_height = (txt_height + LINE_SPACING) * len(text)
    y = (img_height - total_height) / 2
        
    for i in range(len(text)):
        txt_width = d.textbbox((0, 0), text[i], font=font)[2]
        x = (img_width - txt_width - (len(text[i]) * LETTER_SPACING))/2

        _draw_line(d=d, x=x, y=y, line=text[i], font=font, letter_spacing=LETTER_SPACING, fill=FILL, stroke_width=STROKE_WIDTH, stroke_fill=STROKE_FILL)

        y += txt_height + LINE_SPACING
        
    img = img.resize((int(BASE_WIDTH/2), int(float(img.size[1]) * (BASE_WIDTH/2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img

def text_effect(text: str, img: Image):
    LETTER_SPACING = 1
    LINE_SPACING = 3
    STROKE_WIDTH = 1
    STROKE_FILL = (0, 0, 0)
    FONT_BASE = 75
    MARGIN = 10
    LINE_WIDTH = 20
    
    img = img.resize((BASE_WIDTH, int(img.size[1] * float(BASE_WIDTH / img.size[0]))))
    
    text = textwrap.wrap(text, width=LINE_WIDTH)
    if text == []:
        return

    font = ImageFont.truetype(font=ARIAL_FONT_FILE, size=FONT_BASE)
    
    img_width, img_height = img.size
    d = ImageDraw.Draw(img)
    
    _, _, max_txt_width, txt_height = d.textbbox((0, 0), text[0], font=font)
    
    for line in text:
        temp = int(font.getlength(line))
        if temp > max_txt_width:
            max_txt_width = temp
    
    
    total_height = (txt_height + LINE_SPACING) * len(text)
    
    y_inf = 0
    y_sup = img_height - total_height
    x_inf = 0
    x_sup = img_width - max_txt_width - 5
    
    fill = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    x = random.randint(x_inf, x_sup)
    y = random.randint(y_inf, y_sup)
    for i in range(len(text)):
        _draw_line(d=d, x=x, y=y, line=text[i], font=font, letter_spacing=LETTER_SPACING, fill=fill, stroke_width=STROKE_WIDTH, stroke_fill=STROKE_FILL)

        y += txt_height + LINE_SPACING
        
    img = img.resize((int(BASE_WIDTH/2), int(float(img.size[1]) * (BASE_WIDTH/2) / img.size[0])))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img

def test_multiple(text, effect, modifier=""):
        imgs = os.listdir("test")
        for i in range(len(imgs)):
            image = effect(text, Image.open(os.path.join("test", imgs[i])))
            image.save(os.path.join("test_output", f'output{modifier}{i}.jpg'), optimize=True, quality=80)

        print("Image test successful")

def test(text, effect, modifier=""):
        image = effect(text, Image.open("image.jpg"))
        image.save('output.jpg', optimize=True, quality=80)

        print("Image test successful")

def main():
    test("Autore più lungo del solito per vedere se va a capo\ntesto un po' più lungo ma non troppo eh\nquesto verrà scartato\npure questo lorem ipsum prova ", text_effect)
    #test_multiple("top text\nbottom text", splash_effect)
    #test_multiple("top text top text top text top text top text\nbottom text bottom text bottom text bottom text bottom text", splash_effect, "_long")
    
if __name__ ==  "__main__":
    main()