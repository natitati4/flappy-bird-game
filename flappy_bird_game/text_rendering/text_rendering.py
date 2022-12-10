import pygame as pg


def draw_text(x, y, msg, color, size, font_name, scrn, center_or_top_left="top left"):
    font = pg.font.SysFont(font_name, size)
    text = font.render(msg, True, color)
    text_box = text.get_rect()

    text_box.center = ((x + text_box.width) // 2, (y + text_box.height) // 2)
    # if requested that x and y to be center, make them the center.
    if center_or_top_left == "center":
        text_box.center = (x, y)

    scrn.blit(text, text_box)


def outline_text(x, y, msg, color, size, font_name, scrn, center_or_top_left="top left"):
    # with outline_color

    # top left
    draw_text(x - 2, y - 2, msg, color, size, font_name, scrn, center_or_top_left)
    # top right
    draw_text(x + 2, y - 2, msg, color, size, font_name, scrn, center_or_top_left)
    # btm left
    draw_text(x - 2, y + 2, msg, color, size, font_name, scrn, center_or_top_left)
    # btm right
    draw_text(x + 2, y + 2, msg, color, size, font_name, scrn, center_or_top_left)


def draw_regular_text(x, y, msg, color, size, font_name, scrn, center_or_top_left="top left"):
    draw_text(x, y, msg, color, size, font_name, scrn, center_or_top_left)  # with inside_color


def draw_all_text(x, y, msg, inside_color, outline_color, size, font_name, scrn, center_or_top_left="top left"):
    outline_text(x, y, msg, inside_color, size, font_name, scrn, center_or_top_left)  # draw the outline
    draw_regular_text(x, y, msg, outline_color, size, font_name, scrn, center_or_top_left)  # draw the inside