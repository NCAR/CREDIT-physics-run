'''
A collection of helper functions for the data visualization of CREDIT forecasts
-------------------------------------------------------
Content:
    - lg_box
    - lg_clean
    - ax_decorate
    - ax_decorate_box
    - precip_cmap
    - string_partial_format
    - cmap_combine
    - xcolor
    
Yingkai Sha
ksha@ucar.edu
'''

import numpy as np

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import transforms

def lg_box(LG):
    '''
    legned block with white background and boundary lines
    '''
    LG.get_frame().set_facecolor('white')
    LG.get_frame().set_edgecolor('k')
    LG.get_frame().set_linewidth(0)
    LG.get_frame().set_alpha(1.0)
    return LG

def lg_clean(LG):
    '''
    transparent legned block without boundary lines
    '''
    LG.get_frame().set_facecolor('none')
    LG.get_frame().set_linewidth(0)
    LG.get_frame().set_alpha(1.0)

def precip_cmap(return_rgb=True, land_map=True):
    '''
    Customized NCL style precipitaiton colormap
    '''
    if land_map:
        rgb_array = np.array([[0.85      , 0.85      , 0.85      , 1.        ],
                              [0.66666667, 1.        , 1.        , 1.        ],
                              [0.33333333, 0.62745098, 1.        , 1.        ],
                              [0.11372549, 0.        , 1.        , 1.        ],
                              [0.37647059, 0.81176471, 0.56862745, 1.        ],
                              [0.10196078, 0.59607843, 0.31372549, 1.        ],
                              [0.56862745, 0.81176471, 0.37647059, 1.        ],
                              [0.85098039, 0.9372549 , 0.54509804, 1.        ],
                              [1.        , 1.        , 0.4       , 1.        ],
                              [1.        , 0.8       , 0.4       , 1.        ],
                              [1.        , 0.53333333, 0.29803922, 1.        ],
                              [1.        , 0.09803922, 0.09803922, 1.        ],
                              [0.8       , 0.23921569, 0.23921569, 1.        ],
                              [0.64705882, 0.19215686, 0.19215686, 1.        ],
                              [0.55      , 0.        , 0.        , 1.        ]])
    else:
        rgb_array = np.array([[1         , 1         , 1         , 1.        ],
                              [0.66666667, 1.        , 1.        , 1.        ],
                              [0.33333333, 0.62745098, 1.        , 1.        ],
                              [0.11372549, 0.        , 1.        , 1.        ],
                              [0.37647059, 0.81176471, 0.56862745, 1.        ],
                              [0.10196078, 0.59607843, 0.31372549, 1.        ],
                              [0.56862745, 0.81176471, 0.37647059, 1.        ],
                              [0.85098039, 0.9372549 , 0.54509804, 1.        ],
                              [1.        , 1.        , 0.4       , 1.        ],
                              [1.        , 0.8       , 0.4       , 1.        ],
                              [1.        , 0.53333333, 0.29803922, 1.        ],
                              [1.        , 0.09803922, 0.09803922, 1.        ],
                              [0.8       , 0.23921569, 0.23921569, 1.        ],
                              [0.64705882, 0.19215686, 0.19215686, 1.        ],
                              [0.55      , 0.        , 0.        , 1.        ]])
    cmap_ = mcolors.ListedColormap(rgb_array, 'precip_cmap')
    cmap_.set_over(rgb_array[-1, :])
    cmap_.set_under('0.85')
    if return_rgb:
        return cmap_, rgb_array
    else:
        return cmap_

def string_partial_format(fig, ax, x_start, y_start, ha, va, string_list, color_list, fontsize_list, fontweight_list):
    '''
    String partial formatting (experimental).
    
    handles = string_partial_format(fig, ax, 0., 0.5, 'left', 'bottom',
                                    string_list=['word ', 'word ', 'word'], 
                                    color_list=['r', 'g', 'b'], 
                                    fontsize_list=[12, 24, 48], 
                                    fontweight_list=['normal', 'bold', 'normal'])
    Input
    ----------
        fig: Matplotlib Figure instance. Must contain a `canvas` subclass. e.g., `fig.canvas.get_renderer()`
        ax: Matplotlib Axis instance.
        x_start: horizonal location of the text, scaled in [0, 1] 
        y_start: vertical location of the text, scale in [0, 1]
        ha: horizonal alignment of the text, expected to be either "left" or "right" ("center" may not work correctly).
        va: vertical alignment of the text
        string_list: a list substrings, each element can have a different format.
        color_list: a list of colors that matches `string_list`
        fontsize_list: a list of fontsizes that matches `string_list`
        fontweight_list: a list of fontweights that matches `string_list`
    
    Output
    ----------
        A list of Matplotlib.Text instance.
    
    * If `fig` is saved, then the `dpi` keyword must be fixed (becuase of canvas). 
      For example, if `fig=plt.figure(dpi=100)`, then `fig.savefig(dpi=100)`.
      
    '''
    L = len(string_list)
    Handles = []
    relative_loc = ax.transAxes
    renderer = fig.canvas.get_renderer()
    
    for i in range(L):
        handle_temp = ax.text(x_start, y_start, '{}'.format(string_list[i]), ha=ha, va=va,
                              color=color_list[i], fontsize=fontsize_list[i], 
                              fontweight=fontweight_list[i], transform=relative_loc)
        loc_shift = handle_temp.get_window_extent(renderer=renderer)
        relative_loc = transforms.offset_copy(handle_temp._transform, x=loc_shift.width, units='dots')
        Handles.append(handle_temp)
        
    return Handles

def ax_decorate(ax, left_flag, bottom_flag, bottom_spline=False):
    '''
    "L" style panel axis format
    '''
    ax.grid(linestyle=':'); ax.xaxis.grid(False)
    ax.spines["top"].set_visible(False)
    ax.spines["bottom"].set_visible(bottom_spline)
    ax.spines["right"].set_visible(False)
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)
    [j.set_linewidth(2.5) for j in ax.spines.values()]
    ax.tick_params(axis="both", which="both", bottom=False, top=False, \
               labelbottom=bottom_flag, left=False, right=False, labelleft=left_flag)
    return ax

def ax_decorate_box(ax):
    '''
    "Box" style panel axis format
    '''
    ax.xaxis.set_tick_params(labelsize=14)
    ax.yaxis.set_tick_params(labelsize=14)
    [j.set_linewidth(2.5) for j in ax.spines.values()]
    ax.tick_params(axis="both", which="both", bottom=False, top=False, \
               labelbottom=False, left=False, right=False, labelleft=False)
    return ax

def cmap_combine(cmap1, cmap2):
    '''
    Combine two colormaps as one
    '''
    colors1 = cmap1(np.linspace(0., 1, 256))
    colors2 = cmap2(np.linspace(0, 1, 256))
    colors = np.vstack((colors1, colors2))
    return mcolors.LinearSegmentedColormap.from_list('temp_cmap', colors)


def ksha_color_set_summon(color_set=0):
    if color_set == 0:
        rgb_array = np.array([[0.85      , 0.85      , 0.85      , 1.        ],
                              [0.66666667, 1.        , 1.        , 1.        ],
                              [0.33333333, 0.62745098, 1.        , 1.        ],
                              [0.11372549, 0.        , 1.        , 1.        ],
                              [0.37647059, 0.81176471, 0.56862745, 1.        ],
                              [0.10196078, 0.59607843, 0.31372549, 1.        ],
                              [0.56862745, 0.81176471, 0.37647059, 1.        ],
                              [0.85098039, 0.9372549 , 0.54509804, 1.        ],
                              [1.        , 1.        , 0.4       , 1.        ],
                              [1.        , 0.8       , 0.4       , 1.        ],
                              [1.        , 0.53333333, 0.29803922, 1.        ],
                              [1.        , 0.09803922, 0.09803922, 1.        ],
                              [0.8       , 0.23921569, 0.23921569, 1.        ],
                              [0.64705882, 0.19215686, 0.19215686, 1.        ],
                              [0.55      , 0.        , 0.        , 1.        ]])
        SET0 = {'blue': rgb_array[3, :],
                'cyan': rgb_array[2, :],
                'lgreen': rgb_array[4, :],
                'green': rgb_array[5, :],
                'yellow': rgb_array[8, :],
                'orange': rgb_array[-6, :],
                'red': rgb_array[-3, :]}
        return SET0
        
    elif color_set == 1:
        SET1 = {
            'reds': ['#DB444B', '#A81829', '#C7303C', '#E64E53', '#FF6B6C', '#FF8785', '#FFA39F'],
            'blues': ['#006BA2', '#00588D', '#1270A8', '#3D89C3', '#5DA4DF', '#7BBFFC', '#98DAFF'],
            'cyans': ['#3EBCD2', '#005F73', '#00788D', '#0092A7', '#25ADC2', '#4EC8DE', '#6FE4FB'],
            'greens': ['#379A8B', '#005F52', '#00786B', '#2E9284', '#4DAD9E', '#69C9B9', '#86E5D4'],
            'oranges': ['#EBB434', '#714C00', '#8D6300', '#AA7C00', '#C89608', '#E7B030', '#FFCB4D'],
            'browns': ['#B4BA39', '#4C5900', '#667100', '#818A00', '#9DA521', '#BAC03F', '#D7DB5A'],
            'purples': ['#9A607F', '#78405F', '#925977', '#AD7291', '#C98CAC', '#E6A6C7', '#FFC2E3'],
            'yellows': ['#D1B07C', '#674E1F', '#826636', '#9D7F4E', '#B99966', '#D5B480', '#F2CF9A'],
            'grays': ['#758D99', '#3F5661', '#576E79', '#6F8793', '#89A2AE', '#A4BDC9', '#BFD8E5']
        }
        
        return SET1
    
    

def xcolor(key):
    '''
    Get LaTeX xcolor values based on names
    '''
    xcolor = {
    "maroon":"#800000", "dark red":"#8B0000", "brown":"#A52A2A", "firebrick":"#B22222", "crimson":"#DC143C", "red":"#FF0000",
    "tomato":"#FF6347", "coral":"#FF7F50", "indian red":"#CD5C5C", "light coral":"#F08080", "dark salmon":"#E9967A", "salmon":"#FA8072",
    "light salmon":"#FFA07A", "orange red":"#FF4500", "dark orange":"#FF8C00", "orange":"#FFA500", "gold":"#FFD700", "dark golden rod":"#B8860B",
    "golden rod":"#DAA520", "pale golden rod":"#EEE8AA", "dark khaki":"#BDB76B", "khaki":"#F0E68C", "olive":"#808000", "yellow":"#FFFF00",
    "yellow green":"#9ACD32", "dark olive green":"#556B2F", "olive drab":"#6B8E23", "lawn green":"#7CFC00", "chart reuse":"#7FFF00", "green yellow":"#ADFF2F",
    "dark green":"#006400", "green":"#008000", "forest green":"#228B22", "lime":"#00FF00", "lime green":"#32CD32", "light green":"#90EE90",
    "pale green":"#98FB98", "dark sea green":"#8FBC8F", "medium spring green":"#00FA9A", "spring green":"#00FF7F", "sea green":"#2E8B57", "medium aqua marine":"#66CDAA",
    "medium sea green":"#3CB371", "light sea green":"#20B2AA", "dark slate gray":"#2F4F4F", "teal":"#008080", "dark cyan":"#008B8B", "aqua":"#00FFFF",
    "cyan":"#00FFFF", "light cyan":"#E0FFFF", "dark turquoise":"#00CED1", "turquoise":"#40E0D0", "medium turquoise":"#48D1CC", "pale turquoise":"#AFEEEE",
    "aqua marine":"#7FFFD4", "powder blue":"#B0E0E6", "cadet blue":"#5F9EA0", "steel blue":"#4682B4", "corn flower blue":"#6495ED", "deep sky blue":"#00BFFF",
    "dodger blue":"#1E90FF", "light blue":"#ADD8E6", "sky blue":"#87CEEB", "light sky blue":"#87CEFA", "midnight blue":"#191970",
    "navy":"#000080", "dark blue":"#00008B", "medium blue":"#0000CD", "blue":"#0000FF", "royal blue":"#4169E1", "blue violet":"#8A2BE2",
    "indigo":"#4B0082", "dark slate blue":"#483D8B", "slate blue":"#6A5ACD", "medium slate blue":"#7B68EE", "medium purple":"#9370DB", "dark magenta":"#8B008B",
    "dark violet":"#9400D3", "dark orchid":"#9932CC", "medium orchid":"#BA55D3", "purple":"#800080", "thistle":"#D8BFD8", "plum":"#DDA0DD",
    "violet":"#EE82EE", "magenta":"#FF00FF", "orchid":"#DA70D6", "medium violet red":"#C71585", "pale violet red":"#DB7093", "deep pink":"#FF1493",
    "hot pink":"#FF69B4","light pink":"#FFB6C1","pink":"#FFC0CB","antique white":"#FAEBD7","beige":"#F5F5DC","bisque":"#FFE4C4",
    "blanched almond":"#FFEBCD","wheat":"#F5DEB3","corn silk":"#FFF8DC","lemon chiffon":"#FFFACD","light golden rod yellow":"#FAFAD2","light yellow":"#FFFFE0",
    "saddle brown":"#8B4513","sienna":"#A0522D","chocolate":"#D2691E","peru":"#CD853F","sandy brown":"#F4A460","burly wood":"#DEB887",
    "tan":"#D2B48C","rosy brown":"#BC8F8F","moccasin":"#FFE4B5","navajo white":"#FFDEAD","peach puff":"#FFDAB9","misty rose":"#FFE4E1",
    "lavender blush":"#FFF0F5","linen":"#FAF0E6","old lace":"#FDF5E6","papaya whip":"#FFEFD5","sea shell":"#FFF5EE","mint cream":"#F5FFFA",
    "slate gray":"#708090","light slate gray":"#778899", "light steel blue":"#B0C4DE","lavender":"#E6E6FA","floral white":"#FFFAF0","alice blue":"#F0F8FF",
    "ghost white":"#F8F8FF","honeydew":"#F0FFF0","ivory":"#FFFFF0","azure":"#F0FFFF","snow":"#FFFAFA","black":"#000000",
    "dim gray":"#696969","gray":"#808080","dark gray":"#A9A9A9","silver":"#C0C0C0","light gray":"#D3D3D3","gainsboro":"#DCDCDC",
    "white smoke":"#F5F5F5","white":"#FFFFFF"}
    return xcolor[key]




