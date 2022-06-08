#!/usr/bin/env python

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from config import TAGS, BGDIR, QUOTEFILE, FONT, OPACITY
from utils import (
    convert_img_insta,
    recommend_font_size,
    wrap_text,
    get_random_quote,
    get_random_bg,
)


def main():
    # quoteobj = get_random_quote(QUOTEFILE, TAGS)
    # quote, author = quoteobj["text"], quoteobj["author"]
    quote = "being rude to someone will only satisfy your ego not solve your problem"
    author = "dhruv"
    text = quote
    font_size = recommend_font_size(text)
    text = wrap_text(text)

    background_img_file = get_random_bg(BGDIR)
    bgimg = convert_img_insta(background_img_file, "RGBA")
    IMAGE_WIDTH, IMAGE_HEIGHT = bgimg.size

    padding = int((IMAGE_WIDTH / 100) * 5)

    # draw opaque square
    overlay = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    draw.rectangle(
        (
            (padding, padding),
            (
                IMAGE_WIDTH - padding,
                IMAGE_HEIGHT - padding,
            ),
        ),
        fill=(62, 59, 56, OPACITY),
    )
    bgimg = Image.alpha_composite(bgimg, overlay)

    img = Image.new(
        "RGBA",
        (IMAGE_WIDTH, IMAGE_HEIGHT),
        (0, 0, 0, 0),
    )
    img.paste(bgimg, (0, 0))

    # draw quote
    font = ImageFont.truetype(FONT, font_size)
    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size
    x = img_w / 2
    y = img_h / 2
    IF = ImageFont.truetype(FONT, font_size)
    COLOR = (255, 255, 255)
    SPACING = 6
    textsize = draw.multiline_textsize(text, font=IF, spacing=SPACING)
    text_w, text_h = textsize
    x -= text_w / 2
    y -= text_h / 2
    draw.multiline_text(
        align="center",
        xy=(x, y),
        text=text,
        fill=COLOR,
        font=font,
        spacing=SPACING,
    )

    # draw author
    authortextsize = draw.multiline_textsize(author, font=IF, spacing=SPACING)
    authortext_w, authortext_h = authortextsize
    authortextoffset = (
        int((IMAGE_WIDTH - authortext_w) / 2),
        IMAGE_HEIGHT - 4 * padding,
    )
    draw.multiline_text(
        align="center",
        xy=authortextoffset,
        text=author,
        fill=COLOR,
        font=font,
        spacing=SPACING,
    )

    img.save("quote.png", "PNG")


main()
