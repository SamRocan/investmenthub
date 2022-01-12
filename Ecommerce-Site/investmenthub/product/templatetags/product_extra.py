from django import template
register = template.Library()

@register.filter(name='checkEqual')
def checkEqual(dictionary, arg):
    '''
    tempate tag method to determine category, and therefor color of highlight
    :param dictionary: dictionay
    :param arg:
    :return:
    '''
    if(str(arg) in dictionary.keys()):
        return dictionary[str(arg)]
    else:
        return "rgba(0, 0, 0, 0)"