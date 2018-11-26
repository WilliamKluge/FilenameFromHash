import hashlib
import os
import sys


def rename_to_hash(path):
    """
    Renames a file to its MD5 hash with its current extension
    :param path: File to rename
    :return: None
    """
    filename, file_extension = os.path.splitext(path)

    hasher = hashlib.md5()
    with open(path, 'rb') as afile:
        buf = afile.read()
        hasher.update(buf)
    hexdigest = hasher.hexdigest()

    # New path is the directory part of the old path joined with the hash + the extension
    new_path = os.path.join(os.path.split(path)[0], hexdigest + file_extension)

    try:
        os.rename(path, new_path)
    except OSError:
        print('Permission not available to rename object.')


def main():
    if len(sys.argv) > 2:
        print('Unknown parameters. Expected filefromhash.py path')
        return

    # Path is the only argument we need
    path = sys.argv[1]

    if os.path.isdir(path):
        # If we got a directory then rename all valid files in the directory
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            # Don't try to rename directories or hidden files
            if filename[0] != '.' and os.path.isfile(file_path):
                rename_to_hash(file_path)
    else:
        rename_to_hash(path)


if __name__ == '__main__':
    main()
