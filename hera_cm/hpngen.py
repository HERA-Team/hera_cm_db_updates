def wr(pn):
    try:
        if int(pn) < 150:
            p = 'A'
        else:
            p = 'C'
    except ValueError:
        return 'WR{}'.format(pn)
    return 'WR{}{:06d}'.format(p, int(pn)), 'A'


def rd(pn):
    return 'RD{:02d}'.format(int(pn)), 'A'


def ncm(pn):
    if isinstance(pn, str) and pn[0] == 'P':
        return 'NCM{}'.format(pn), 'A'
    return 'NCM{:02d}'.format(int(pn)), 'A'
