from PIL import Image, ImageDraw, ImageFont
import textwrap, os


        


def tt_bt_effect(text, img):
    IMPACT_FONT_FILE = os.path.join("fonts", "impact.ttf")
    BASE_WIDTH = 1200
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
            y = ((img_height / MARGIN)) - (txt_height / 1.5)

        for line in split_caption:
            txt_width = d.textbbox((0, 0), line, font=font)[2]

            x = (img_width - txt_width - (len(line) * LETTER_SPACING))/2

            for i in range(len(line)):
                char = line[i]
                width = font.getlength(char)
                d.text((x, y), char, fill=FILL, stroke_width=STROKE_WIDTH, font=font, stroke_fill=STROKE_FILL)
                x += width + LETTER_SPACING

            y = y + (txt_height + LINE_SPACING) * factor
    
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
        
    h_size = int(float(img.size[1]) * (BASE_WIDTH/2) / img.size[0])
    img = img.resize((int(BASE_WIDTH/2), h_size))
    
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    
    return img

def test(text, effect, modifier=""):
        imgs = os.listdir("test")
        for i in range(len(imgs)):
            image = effect(text, Image.open(os.path.join("test", imgs[i])))
            image.save(os.path.join("test_output", f'output{modifier}{i}.jpg'), optimize=True, quality=80)

        print("Image test successful")

def main():
    test("top text\nbottom text", tt_bt_effect)
    test("top text top text top text top text top text\nbottom text bottom text bottom text bottom text bottom text", tt_bt_effect, "_long")
    
if __name__ ==  "__main__":
    main()