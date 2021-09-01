# code copied from https://stackoverflow.com/a/48030307/7962707

from ctypes import wintypes, windll
from functools import cmp_to_key

def winsort(data):
    _StrCmpLogicalW = windll.Shlwapi.StrCmpLogicalW
    _StrCmpLogicalW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR]
    _StrCmpLogicalW.restype  = wintypes.INT

    cmp_fnc = lambda psz1, psz2: _StrCmpLogicalW(psz1.name, psz2.name)
    return sorted(data, key=cmp_to_key(cmp_fnc))