from functools import wraps


def to_console(indentations, message):
    """For clean console output"""
    text = ''
    for i in range(indentations):
        text += '    '
    text += message
    print(text)


def logger(func):
    """Decorator that prints out function name before function call"""
    @wraps(func)
    def log(*args, **kwargs):
        to_console(0, 'Running function ' + func.__name__ + '()')
        func(*args, **kwargs)
    return log



