# util/charts.py

months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]
colorPalette = ['rgba(130, 235, 198, 0.2)', 'rgba(129, 236, 236, 0.2)', 'rgba(162, 155, 254, 0.2)', 'rgba(255, 234, 167, 0.2)', 'rgba(250, 177, 160, 0.2)', 'rgba(255, 118, 117, 0.2)', 'rgba(253, 121, 168, 0.2)']
colorPaletteBorder = ['rgba(130, 235, 198, 1)', 'rgba(129, 236, 236, 1)', 'rgba(162, 155, 254, 1)', 'rgba(255, 234, 167, 1)', 'rgba(250, 177, 160, 1)', 'rgba(255, 118, 117, 1)', 'rgba(253, 121, 168, 1)']
colorPrimary, colorSuccess, colorDanger = '#79aec8', colorPalette[0], colorPalette[5]


def get_year_dict():
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict


def generate_color_palette(amount):
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette

def generate_color_palette_boarder(amount):
    palette = []

    i = 0
    while i < len(colorPaletteBorder) and len(palette) < amount:
        palette.append(colorPaletteBorder[i])
        i += 1
        if i == len(colorPaletteBorder) and len(palette) < amount:
            i = 0

    return palette