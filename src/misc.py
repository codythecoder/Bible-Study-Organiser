import os

__all__ = [
    'split_path',
    'mkdirpath',
]


def split_path(path):
    """split a path into a list. The inverse of os.path.join"""
    folders = []
    while True:
        # os.path.split gets the first element off the front, so do that
        #   until we've split the entire path
        path, folder = os.path.split(path)
        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
            break
    folders.reverse()
    return folders

def mkdirpath(folderpath):
    """make a directory, and any parent directories that don't exist"""
    if os.path.isdir(folderpath):
        return
    folder = split_path(folderpath)
    if os.path.isfile(folderpath):
        folder = folder[:-1]
    for i in range(1, len(folder)+1):
        if not os.path.isdir(os.path.join(*folder[:i])):
            os.mkdir(os.path.join(*folder[:i]))
