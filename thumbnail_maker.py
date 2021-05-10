from PIL import Image, ImageFont, ImageDraw
import settings, data


def make_thumbnail(show=False):
    # standard youtube size for thumbnails
    SIZE = (1280, 720)

    # gray bg
    bg = Image.new('RGB', SIZE, color=settings.bg_color)
    # python logo
    logo = Image.open('python_logo.png')

    # if you need to resize the logo image, change the "scale_factor" var in settings.py
    logo = logo.resize((round(logo.size[0] * settings.scale_factor), round(logo.size[1] * settings.scale_factor)))

    # add logo centered
    bg = bg.copy()
    bg.paste(logo, (SIZE[0]//2 - logo.size[0]//2, SIZE[1]//2 - logo.size[1]//2), logo)

    # joint bg image
    bg.save('temp.jpg', quality=95)
    matchup = Image.open('temp.jpg')

    # add text
    fontpath = settings.fontpath
    font = ImageFont.truetype(fontpath, settings.fontsize)
    draw = ImageDraw.Draw(matchup)
    fulltext = data.fulltext
    fulltext_width, fulltext_height = draw.textsize(fulltext, font=font)
    words = fulltext.split()
    # if you need to change the separation between words and lines, change "sep" var in settings.py
    start_x = SIZE[0]//2 - fulltext_width//2 - settings.sep//2
    start_y = matchup.size[1]//2 - logo.size[1]
    start_pos = (start_x, start_y)
    next_pos = ()

    # if logo was resized, check if text is outside image boundary
    if start_y < 0:
        # set text to top margin of image
        start_pos = (start_x, settings.padding)

    for i in range(len(words)):
        textwidth, textheight = draw.textsize(words[i], font=font)
        if i == 0:
            next_pos = start_pos
        # draw a word
        draw.text((next_pos[0], next_pos[1]), words[i], font=font, fill=settings.text_color)
        # move to end of word
        start_x += textwidth + (settings.sep // 2)
        # draw line
        linewidth = settings.fontsize // 10
        # remove the if statement if you want to draw a line after the last word
        if i != len(words) - 1:
            draw.line((start_x, start_pos[1], start_x, start_pos[1] + settings.fontsize),
                      fill=settings.line_color, width=linewidth)
        # add space after line
        start_x += settings.sep // 2
        # update next word's position
        next_pos = (start_x, start_pos[1])

    # export final image
    matchup.save(data.export_filename, quality=95)
    if show:
        matchup.show()
