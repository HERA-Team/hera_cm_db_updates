#! /usr/bin/env python
"""Add wr and arduinos."""
import sys
from hera_cm import signal_chain

hera = signal_chain.Update(sys.argv[0], chmod=True)

wr_hpn = ['A000028', 'A000086', 'A000083', 'A000084', 'A000087', 'A000089',
          'A000093', 'A000091', 'A000094', 'A000006', 'A000097', 'A000079',
          'A000080', 'A000096', 'A000085', 'A000090']
wr_mfg = ['8.312', '9.402', '9.396', '9.398', '9.403', '9.394', '10.497', '8.314',
          '10.491', '_.UNK', '10.494', '9.399', '9.397', '10.496', '9.395', '9.392']
rd_hpn = [31, 45, 46, 41, 42, 6, 20, 15, 19, 40, 43, 11, 17, 18, 4, 7]
# wr_mac = ['b1:81:75', '50:e0:56', 'b2:18:d1', 'b1:81:75', 'b2:17:8a', 'b2:2e:07',
#           'b2:55:3b', '6e:cd:b1', '50:8b:44', '6e:b9:a5', 'UNK', '6f:18:98',
#           'b2:74:88', 'b2:17:81', '6e:6c:b1', 'b1:81:7e', 'b1:e9:92']
# rd_mac_top = ['ca', 'e7', 'f5', 'f6', 'f2', 'f1', 'ce', 'dc', 'd7', 'db', 'f0',
#               'f3', 'd3', 'd9', 'da', 'cc', 'cf']
# rd_mac_bot = ['UNK', '09:9b', '07:bc', '0b:2b', '0b:4c', '0b:5b', '09:d9', '0a:3a',
#               '0a:27', '08:71', '08:66', '07:ba', '0a:35', '0a:e9', '08:6c',
#               '08:ab', '0a:c0']
ncm_hpn = ['P2', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10',
           '11', '12', '13', '15', '16']
cdate = ['2019/08/02', '2019/08/02', '2019/05/14', '2019/10/31', '2019/10/31',
         '2019/11/13', '2019/11/13', '2020/01/31', '2020/01/31', '2020/01/28',
         '2020/01/31', '2020/03/01', '2020/03/01', '2020/02/15', '2020/03/20', '2020/03/20']

part_times = {}
for i in range(len(wr_hpn)):
    wr = 'WR{}'.format(wr_hpn[i])
    wrm = 'S{}'.format(wr_mfg[i])
    rd = 'RD{:02d}'.format(rd_hpn[i])
    cda = cdate[i]
    part_times[wr] = cda
    part_times[rd] = cda
    ncm = 'NCM{}'.format(ncm_hpn[i])
    hera.update_part('add', [wr, 'A', 'white-rabbit', wrm],
                     cdate=cda, ctime='10:00')
    hera.update_part('add', [rd, 'A', 'arduino', rd],
                     cdate=cda, ctime='10:00')
    hera.update_connection('add', [wr, 'A', 'mnt'], [ncm, 'A', 'mnt'], cdate=cda, ctime='11:00')
    hera.update_connection('add', [rd, 'A', 'mnt'], [ncm, 'A', 'mnt'], cdate=cda, ctime='11:00')

used_pk = []
with open('macip_partinfo.txt', 'r') as fp:
    for line in fp:
        pn, note = line.strip().split('$')
        try:
            cda = part_times[pn]
        except KeyError:
            continue
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
