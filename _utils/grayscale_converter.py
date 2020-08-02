"""Utility function to see how an image will look in grayscale"""

from PIL import Image

def make_grayscale(filepath, save=False):
    """Convert image file to grayscale and optionally save it to `save`."""
    img = Image.open(filepath).convert('LA')
    if save:
        img.save(save)
    return img