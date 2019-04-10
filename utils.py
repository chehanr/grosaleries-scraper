
def get_datetime_str():
    """ Returns datetime string for console usage. """
    import time

    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
