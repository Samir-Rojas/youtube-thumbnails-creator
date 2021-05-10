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
    _add_text(SIZE, logo, matchup)

    # export final image
    _export(matchup, show)


def _export(matchup, show):
    matchup.save(data.export_filename, quality=95)
    if show:
        matchup.show()


def _add_text(SIZE, logo, matchup):
    fontpath = settings.fontpath
    font = ImageFont.truetype(fontpath, settings.fontsize)
    draw = ImageDraw.Draw(matchup)
    fulltext = data.fulltext
    fulltext_width, fulltext_height = draw.textsize(fulltext, font=font)
    words = fulltext.split()
    
    # if you need to change the separation between words and lines, change "sep" var in settings.py
    start_pos = _calculate_text_start(SIZE, fulltext_width, logo, matchup)

    # if logo was resized, check if text is outside image boundary
    start_pos = _set_text_from_image_boundary(start_pos)

    _draw_text_and_lines(draw, font, start_pos, words)


def _calculate_text_start(SIZE, fulltext_width, logo, matchup):
    start_x = SIZE[0] // 2 - fulltext_width // 2 - settings.sep // 2
    start_y = matchup.size[1] // 2 - logo.size[1]
    start_pos = (start_x, start_y)
    return start_pos


def _draw_text_and_lines(draw, font, start_pos, words):
    start_x = start_pos[0]
    next_pos = ()
    
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


def _set_text_from_image_boundary(start_pos):
    # if logo was resized, check if text is outside image boundary
    if start_pos[1] < 0:
        # set text to top margin of image
        start_pos = (start_pos[0], settings.padding)
        return start_pos
