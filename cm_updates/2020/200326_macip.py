#! /usr/bin/env python
"""Add wr and arduinos."""
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)


used_pk = []
with open('macip_partinfo.txt', 'r') as fp:
    for line in fp:
        pn, note = line.strip().split('$')
        cda = '2020/03/26'
        pk = '{}{}'.format(pn, cda)
        ipk = 0
        if pk in used_pk:
            for x in used_pk:
                if x == pk:
                    ipk += 1
        used_pk.append(pk)
        cti = "10:{:02d}".format(ipk)
        hera.add_part_info(pn, 'A', note, cdate=cda, ctime=cti)
hera.done()
