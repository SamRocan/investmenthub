# util/charts.py
from calendar import monthrange
from datetime import date, datetime, timedelta

months = [
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]
colorPalette = ['rgba(130, 235, 198, 0.2)', 'rgba(129, 236, 236, 0.2)', 'rgba(162, 155, 254, 0.2)', 'rgba(255, 234, 167, 0.2)', 'rgba(250, 177, 160, 0.2)', 'rgba(255, 118, 117, 0.2)', 'rgba(253, 121, 168, 0.2)']
colorPaletteBorder = ['rgba(130, 235, 198, 1)', 'rgba(129, 236, 236, 1)', 'rgba(162, 155, 254, 1)', 'rgba(255, 234, 167, 1)', 'rgba(250, 177, 160, 1)', 'rgba(255, 118, 117, 1)', 'rgba(253, 121, 168, 1)']
colorPrimary, colorSuccess, colorDanger = '#79aec8', colorPalette[0], colorPalette[5]


def get_year_dict():
    '''
    fill a dictionary with month of the year
    :return: year_dict: dict
    '''
    year_dict = dict()

    for month in months:
        year_dict[month] = 0

    return year_dict

def yearDict(year, month, day):
    '''
    Creates a dictionary containing the current days of the year so far
    :param year: int
    :param month: int
    :param day: int
    :return: calender: dict
    '''
    calender = dict()
    x=1
    i=1
    while(x<=month):
        info = monthrange(year, x)
        for i in range(1,info[1]+1):
            if(len(str(i))==1):
                calender[str(year)+"-"+str(x)+"-0"+str(i)] = 0
            else:
                calender[str(year)+"-"+str(x)+"-"+str(i)] = 0
            if(x==month and i==day):
                break
        x+=1
    return calender

def currentDaysOfYear():
    '''
    creates a calender up to the current date
    :return: calender : dict
    '''
    today = date.today()
    d = today.timetuple()

    calender = yearDict(d.tm_year, d.tm_mon, d.tm_mday)
    return calender

def getDateRange(dRange):
    '''
    creates a list of dates in a selected date range
    :param dRange: int
    :return: dates : list
    '''
    tod = date.today()
    d = timedelta(days = dRange)
    a = tod - d
    delta = tod - a       # as timedelta
    dates = []
    for i in range(delta.days + 1):
        day = a + timedelta(days=i)
        dates.append(day)
    return dates

def getSoldCountAndRevenue(orders, rng):
    '''
    calculates number of products sold and total revenue in a period of time
    :param orders: List of OrderItems Model Instances
    :param rng: int
    :return: list : list containing sold count and revenue count
    '''
    sCount = 0
    rCount = 0
    for i in orders:
        if(i.created_at.date() in rng):
            sCount+=1
            rCount+=i.paid_amount
    return [sCount, rCount]

def getProductAddedCount(products, rng):
    '''
    finds the total number of products added by user over a period of timie
    :param products: list of Product Model Instances
    :param rng: int
    :return: pAddedCount : int
    '''
    pAddedCount = 0
    for i in products:
        if(i.date_added.date() in rng):
            pAddedCount+=1
    return pAddedCount

def generate_color_palette(amount):
    '''
    generates a color pallet depending on the size of items in the chart
    :param amount: int
    :return: palette : list of strings (hex colors)
    '''
    palette = []

    i = 0
    while i < len(colorPalette) and len(palette) < amount:
        palette.append(colorPalette[i])
        i += 1
        if i == len(colorPalette) and len(palette) < amount:
            i = 0

    return palette

def generate_color_palette_boarder(amount):
    '''
    generates a color pallet for borders depending on the size of items in the chart
    :param amount: int
    :return: palette : list of strings (hex colors)
    '''
    palette = []

    i = 0
    while i < len(colorPaletteBorder) and len(palette) < amount:
        palette.append(colorPaletteBorder[i])
        i += 1
        if i == len(colorPaletteBorder) and len(palette) < amount:
            i = 0

    return palette