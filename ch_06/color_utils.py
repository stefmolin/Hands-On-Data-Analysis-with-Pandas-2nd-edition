import re

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

def hex_to_rgb_color_list(colors):
    """
    Take color or list of hex code colors and convert them 
    to RGB colors in the range [0,1].
    
    Parameters:
        - colors: Color or list of color strings of the format 
                  '#FFF' or '#FFFFFF'
    
    Returns:
        The color or list of colors in RGB representation.
    """
    if isinstance(colors, str):
        colors = [colors]
    
    for i, color in enumerate(
        [color.replace('#', '') for color in colors]
    ):
        hex_length = len(color)
        
        if hex_length not in [3, 6]:
            raise ValueError(
                'Your colors must be of the form #FFFFFF or #FFFFFF'
            )
        
        regex = '.' * (hex_length // 3)
        colors[i] = [
            int(val * (6 // hex_length), 16)/255 \
            for val in re.findall(regex, color)
        ]
    
    return colors[0] if len(colors) == 1 else colors

def two_color_sequential_cmap(rgb_color_list):
    """
    Created a sequential colormap blending from one color to the other.
    
    Parameters:
        - rgb_color_list: A list of colors represented as [R, G, B] values
                          in the range [0, 1], like [[0, 0, 0], [1, 1, 1]], 
                          for black and white, respectively.
    
    Returns:
        A matplotlib ListedColormap object with your colormap.
    """
    if not isinstance(rgb_color_list, list):
        raise ValueError('Colors must be passed as a list!')
    elif len(rgb_color_list) != 2:
        raise ValueError(
            'Can only specify two colors; '
            'one for each end of the spectrum.'
        )
    elif (
        not isinstance(rgb_color_list[0], list) or not isinstance(rgb_color_list[1], list)
    ) or (
        len(rgb_color_list[0]) != 3 or len(rgb_color_list[1]) != 3
    ):
        raise ValueError('Each color should be represented as a list of size 3.')
    
    N = 256
    entries = 4 # red, green, blue, alpha
    rgbas = np.ones((N, entries))
    for i in range(entries - 1): # we don't alter alphas
        rgbas[:, i] = np.linspace(
            start=rgb_color_list[0][i], 
            stop=rgb_color_list[1][i], 
            num=N
        )
    
    return ListedColormap(rgbas)

def draw_cmap(cmap):
    """
    Draw a colorbar for visualizing a colormap.
    
    Parameters:
        - cmap: A matplotlib colormap
        
    Returns:
        A matplotlib colorbar, which you can save with:
        `plt.savefig(<file_name>, bbox_inches='tight')`
    """
    img = plt.imshow(np.array([[0,1]]), cmap=cmap)
    cbar = plt.colorbar(orientation='horizontal', cmap=cmap)
    img.axes.remove()
    return cbar

def blended_cmap(rgb_color_list):
    """
    Created a colormap blending from one color to the other.
    
    Parameters:
        - rgb_color_list: A list of colors represented as [R, G, B] values
                          in the range [0, 1], like [[0, 0, 0], [1, 1, 1]], 
                          for black and white, respectively.
    
    Returns:
        A matplotlib ListedColormap object with your colormap.
    """
    if not isinstance(rgb_color_list, list):
        raise ValueError('Colors must be passed as a list!')
    elif len(rgb_color_list) < 2:
        raise ValueError('Must specify at least 2 colors.')
    elif (
        not isinstance(rgb_color_list[0], list) \
        or not isinstance(rgb_color_list[1], list)
    ) or (
        len(rgb_color_list[0]) != 3 or len(rgb_color_list[1]) != 3
    ):
        raise ValueError(
            'Each color should be represented as a list of size 3.'
        )
    
    N = 256
    entries = 4 # red, green, blue, alpha
    rgbas = np.ones((N, entries))
    
    segment_count = len(rgb_color_list) - 1
    segment_size = N // segment_count
    remainder = N % segment_count # need to add this back later
    
    for i in range(entries - 1): # we don't alter alphas
        updates = []
        for seg in range(1, segment_count + 1):
            # determine how much needs to be added back to account for remainders
            if not remainder or seg > 1:
                offset = 0
            else:
                offset = remainder
                
            updates.append(np.linspace(
                start=rgb_color_list[seg-1][i], 
                stop=rgb_color_list[seg][i], 
                num=segment_size + offset
            ))

        rgbas[:,i] = np.concatenate(updates)
    
    return ListedColormap(rgbas)