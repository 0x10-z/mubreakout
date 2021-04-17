import os

import pygame

try:
    main_dir = os.path.split(os.path.abspath(__file__))[0]
except NameError:  # We are the main py2exe script, not a module
    import sys
    main_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

pygame.font.init()

FONTRENDER = pygame.font.SysFont("monospace", 25, bold=True)
SCREENRECT = pygame.Rect(0, 0, 640, 480)
screenRECT = pygame.Rect(0, 0, 640, 480)


def load_image(file):
    file = os.path.join(main_dir, 'res', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "{}" {}'.format(file, pygame.get_error()))
    return surface


def load_images(image_names):
    images = []
    for name in image_names:
        images.append(load_image(name))
    return images
