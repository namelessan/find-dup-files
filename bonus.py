import os
import stat
from core import scan_files


_cache = {}
BUFSIZE = 8*1024


def file_cmp(f1, f2, shallow=True):
    """Compare two files.

    Arguments:

    f1 -- First file name

    f2 -- Second file name

    shallow -- Just check stat signature (do not read the files).
               defaults to True.

    Return value:

    True if the files are the same, False otherwise.

    This function uses a cache for past comparisons and the results,
    with cache entries invalidated if their stat information
    changes.  The cache may be cleared by calling clear_cache().

    """

    s1 = _sig(os.stat(f1))
    s2 = _sig(os.stat(f2))
    if s1[0] != stat.S_IFREG or s2[0] != stat.S_IFREG:
        return False
    if shallow and s1 == s2:
        return True
    if s1[1] != s2[1]:
        return False

    outcome = _cache.get((f1, f2, s1, s2))
    if outcome is None:
        outcome = _do_cmp(f1, f2)
        if len(_cache) > 100:      # limit the maximum size of the cache
            clear_cache()
        _cache[f1, f2, s1, s2] = outcome
    return outcome


def _sig(st):
    return (stat.S_IFMT(st.st_mode),
            st.st_size,
            st.st_mtime)


def _do_cmp(f1, f2):
    bufsize = BUFSIZE
    with open(f1, 'rb') as fp1, open(f2, 'rb') as fp2:
        while True:
            b1 = fp1.read(bufsize)
            b2 = fp2.read(bufsize)
            if b1 != b2:
                return False
            if not b1:
                return True


def remove_file(file, files):
    try:
        files.remove(file)
    except ValueError:
        pass


def get_same_file(f1, files):
    same_files = [f1]
    remove_file(f1, files)
    for f2 in files:
        if file_cmp(f1, f2):
            same_files.append(f2)
    return same_files


def group_file_by_cmp(files):
    dup_files = []
    for file in files:
        same_files = get_same_file(file, files)
        if len(same_files) >= 2:
            dup_files.append(same_files)
        files = [f for f in files if f not in same_files]
    return dup_files


def find_duplicate_files_by_cmp(dir):
    file_paths = scan_files(dir)
    dup_files = group_file_by_cmp(file_paths)
    return dup_files
