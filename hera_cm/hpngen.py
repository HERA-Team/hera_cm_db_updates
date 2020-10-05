def wr(pn):
    if int(pn) < 150:
        p = 'A'
    else:
        p = 'C'
    return 'WR{}{:06d}'.format(p, int(pn)), 'A'


def rd(pn):
    return 'RD{:02d}'.format(int(pn)), 'A'


def ncm(pn):
    return 'NCM{:02d}'.format(int(pn)), 'A'
