"""Utility functions for creating visual aids."""

from PIL import Image
import matplotlib.pyplot as plt


def make_grayscale(filepath, save=False):
    """Convert image file to grayscale and optionally save it to `save`."""
    img = Image.open(filepath).convert('LA')
    if save:
        img.save(save)
    return img


def edit_image(filepath, replacements, save=False):
    """
    Replace colors in the specified image pixel by pixel.

    Parameters:
        - filepath: The filepath to the image
        - replacements: A dictionary where the keys are
                        RGBA color tuples to replace and
                        the values are the replacements
        - save: Whether to save the file back to the filepath.

    Returns:
        Modified image.

    Example usage:
        edit_image('netflix_after_hours_trading.png', {(179, 0, 0, 255): (255, 0, 0, 255)})
    """
    im = Image.open(filepath)

    modified_pixels = [
        replacements.get(color, color) for color in im.getdata()
    ]

    modified_im = Image.new(im.mode, im.size)
    modified_im.putdata(modified_pixels)

    if save:
        modified_im.save(filepath)

    return modified_im

def save_plot(file):
    """Save the current figure."""
    plt.savefig(file, dpi=300, bbox_inches='tight')
