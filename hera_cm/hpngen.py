def wr(pn, p=None):
    """
    Return wr part number and version.

    Parameters
    ==========
    pn : int or str
         (see logic below...)
    p : str
        Currently 'A' or 'C'.  If none, assumes pn is str with value.
    """
    try:
        if int(pn) < 202:
            pn = int(pn)
        else:
            raise ValueError('pn too large')
    except ValueError:
        if pn.startswith('WR'):
            return pn, 'A'
        else:
            return 'WR{}'.format(pn), 'A'
    if p is None:
        raise ValueError('must specify A or C')
    return 'WR{}{:06d}'.format(p, int(pn)), 'A'


def rd(pn):
    return 'RD{:02d}'.format(int(pn)), 'A'


def ncm(pn):
    if isinstance(pn, str) and pn[0] == 'P':
        return 'NCM{}'.format(pn), 'A'
    return 'NCM{:02d}'.format(int(pn)), 'A'
