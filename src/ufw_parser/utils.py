import os
import fnmatch


def find_files(directory, pattern):
    """Search recursively for files matching a given pattern.

    Args:
        directory (str): The root directory from where the search will begin.
        pattern (str): The pattern to match the filenames against.

    Returns:
        list of str: A list containing the full paths to the files that match the pattern.
    """
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            matches.append(os.path.join(root, filename))
    return matches

