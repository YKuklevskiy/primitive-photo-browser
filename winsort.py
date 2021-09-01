# code copied from https://stackoverflow.com/a/48030307/7962707

from ctypes import wintypes, windll
from functools import cmp_to_key

# winsort - returns sorted via windows explorer sort iterable of items
# data: Iterable
# Container that needs to be sorted
# attribute: str
# string representation of the name of the data's item attribute, which should be the sort key
def winsort(data, attribute: str = ''):
    _StrCmpLogicalW = windll.Shlwapi.StrCmpLogicalW
    _StrCmpLogicalW.argtypes = [wintypes.LPWSTR, wintypes.LPWSTR]
    _StrCmpLogicalW.restype  = wintypes.INT

    if attribute != '':
        cmp_fnc = lambda psz1, psz2: _StrCmpLogicalW(psz1.__getattribute__(attribute), psz2.__getattribute__(attribute))
    else:
        cmp_fnc = lambda psz1, psz2: _StrCmpLogicalW(psz1, psz2)
    return sorted(data, key=cmp_to_key(cmp_fnc))