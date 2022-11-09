import os


def CACHE_PATH():
    cache_path = './.cache/'
    if not os.path.isdir(cache_path):
        os.mkdir(cache_path)
    return cache_path
